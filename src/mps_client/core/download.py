#   Copyright 2022 Modelyst LLC
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import asyncio
import io
import json
import logging
import re
import zipfile
from pathlib import Path
from typing import List, Optional

import httpx
import requests
from bs4 import BeautifulSoup

from mps_client._exceptions import (
    CaltechJsonNotFound,
    ConnectionTimeoutError,
    DeadUrlError,
    DOINotFound,
    RequestLimitation,
    UrlConnectionError,
)

logger = logging.getLogger(__name__)
timeout = httpx.Timeout(60)


def download_doi(doi: str, path: Path) -> None:
    logger.info(f'Getting the DOI webpage')
    URL = f"https://doi.org/{doi}"
    page = requests.get(URL)
    logger.info(f'Parsing DOI webpage for links.')
    zip_file_url = parse_webpage_for_zip_links(page.content, doi)
    logger.info(f'Downloading link {zip_file_url} found for doi')
    r = requests.get(zip_file_url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    logger.info(f'Extracting to path {path}')
    z.extractall(path)


async def async_download_doi(doi: str, path: Path) -> None:
    """Asynchronously download a doi to a local path."""
    logger.info(f'Getting download links for doi  at https://doi.org/{doi}')
    zip_links = await get_zip_links_from_doi(doi)
    if len(zip_links) > 1:
        raise ValueError(f'Found two zip links for doi {doi}')
    zip_link = zip_links[0]
    logger.info(f'Downloading link {zip_link} found for doi')
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            r: httpx.Response = await client.get(zip_link, follow_redirects=True)
        except httpx.ConnectTimeout:
            raise TimeoutError(f'HTTP Request for {zip_link} timed out.')
    z = zipfile.ZipFile(io.BytesIO(r.content))
    logger.info(f'Extracting to path {path}')
    z.extractall(path)


async def get_zip_links_from_doi(doi: str) -> List[str]:
    """Get Zip Links From DOI."""
    doi_url = f"https://doi.org/{doi}"
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            page: httpx.Response = await client.get(doi_url, follow_redirects=True, timeout=60)
        except (httpx.TimeoutException):
            raise ConnectionTimeoutError(f'HTTP Request for {doi_url} timed out.')
        except (httpx.ConnectError) as exc:
            redirect_link = await get_redirect_link_from_doi(doi)
            if redirect_link and 'www.mpsjcap.org' in redirect_link:
                raise DeadUrlError(f'DOI {doi} redirects to a dead url at {redirect_link}')
            logger.error(f'Error occurred while trying to connect to {doi_url} for downloading', exc_info=exc)
            raise UrlConnectionError(f'HTTP Request for {doi_url} timed out.')

    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find('title')
    if 'DOI Not Found' in title.string:
        raise DOINotFound(f'DOI does not exist: {doi}')

    logger.info(f'Downloading json from {page.url} found for doi')
    record_json = await get_json(str(page.url))
    zip_files = parse_json(record_json)
    return zip_files


async def get_json(caltech_link: str) -> dict:
    """Get Caltech Record JSON and parse to dict."""
    retries = 5
    async with httpx.AsyncClient(timeout=timeout) as client:
        while retries > 0:
            response = await client.get(f'{caltech_link}/export/json', follow_redirects=True)

            if response.status_code == 429:
                retries -= 1
                await asyncio.sleep(1)
                continue
            else:
                break

    if response.status_code == 429:
        raise RequestLimitation('Too many requests')
    elif response.status_code != 200:
        raise CaltechJsonNotFound(
            f'Getting json failed for url {caltech_link}/export/json, got status code {response.status_code}, {response.text}'
        )

    return json.loads(response.text)


url_pattern = r'href="(https:\/\/.*\.zip)"'
regex = re.compile(url_pattern)


def parse_json(record_json: dict):
    try:
        descriptions = record_json['metadata']['additional_descriptions']
        matches = (regex.search(x['description']) for x in descriptions)
        links = [x.groups()[0] for x in matches if x is not None]
    except KeyError:
        raise ValueError(f'Cannot parse the record json {record_json}')
    if len(links) == 0:
        raise ValueError(f'Issue parsing the page found {len(links)} instead of 1')
    elif len(links) > 1:
        logger.info(f'found more than one link {links}')
    return links


def parse_webpage_for_zip_links(page_contents: bytes, doi: str) -> str:
    soup = BeautifulSoup(page_contents, "html.parser")
    title = soup.find('title')
    if 'DOI Not Found' in title.string:
        raise DOINotFound(f'DOI does not exist: {doi}')
    record_citation = soup.find(id='recordCitation')
    if record_citation is None:
        print(page_contents)
        raise ValueError(f'Cannot find record citation on doi {doi}')
    try:
        record_json = json.loads(record_citation['data-record'])
        descriptions = record_json['metadata']['additional_descriptions']
        matches = (regex.search(x['description']) for x in descriptions)
        links = [x.groups()[0] for x in matches if x is not None]
    except KeyError:
        raise ValueError(f'Cannot parse the record json {record_json}')
    if len(links) == 0:
        raise ValueError(f'Issue parsing the page found {len(links)} instead of 1')
    elif len(links) > 1:
        logger.info(f'found more than one link {links}')
    zip_file_url = links[0]
    return zip_file_url


async def get_redirect_link_from_doi(doi: str) -> Optional[str]:
    doi_url = f"https://doi.org/{doi}"
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.get(doi_url, follow_redirects=False)
        except (httpx.ConnectTimeout, httpx.TimeoutException):
            return None

    if response.status_code != 302:
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all('a')
    return links[0]['href']
