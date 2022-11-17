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
from pathlib import Path
from typing import Optional
from uuid import UUID

import typer

import mps_client.cli.styles as styles
from mps_client._enums import EntityType
from mps_client._exceptions import (
    ConnectionTimeoutError,
    DeadUrlError,
    DOINotFound,
    MPSClientException,
    RequestLimitation,
)
from mps_client.core.download import async_download_doi, get_redirect_link_from_doi, get_zip_links_from_doi
from mps_client.core.queries import get_doi

download_app = typer.Typer(
    name='download', no_args_is_help=True, help="Download Zip files from sample and process information."
)


@download_app.command(name="doi")
def download_doi_command(
    doi: str = typer.Option(..., '--doi', help='Doi to download'),
    path: Path = typer.Option(..., '--path', help='Path to download the doi to'),
):
    """
    Download a doi from Caltech Data.
    """
    with styles.console.status('Downloading DOI zip...'):
        try:
            asyncio.run(async_download_doi(doi, path))
        except DOINotFound:
            styles.bad_typer_print(f'DOI provided is invalid, see https://doi.org/{doi} for details')
            raise typer.Exit(code=1)
    styles.delimiter()
    styles.console.print(f'Finished downloading, files extracted to {str(path)!r}')


@download_app.command(name="entity")
def download_entity(
    entity_type: EntityType = typer.Option(..., '--entity', help='Path to sql file to run query from'),
    entity_id: Optional[UUID] = typer.Option(None, '--id', help='Path to sql file to run query from'),
    entity_label: Optional[str] = typer.Option(None, '--label', help='Path to sql file to run query from'),
    path: Path = typer.Option(None, '--path', help='Path to download the doi to'),
):
    """
    Download a doi from Caltech Data using an entity type and label/uuid.
    """
    with styles.console.status('Getting doi...'):
        doi = get_doi(entity_type=entity_type, entity_id=entity_id, entity_label=entity_label)
        lable_str = f'id={entity_id}' if entity_id else f'label={entity_label}'
        if doi is None:
            styles.bad_typer_print(f'No doi found for entity {entity_type}({lable_str})')
            raise typer.Exit(code=1)

    # Default path is created from entity label and path
    if path is None:
        path = Path.cwd() / f'results/{entity_type}/{(entity_id or entity_label)}/'
    with styles.console.status(f'Downloading DOI zip to \'{path}\'...'):
        try:
            asyncio.run(async_download_doi(doi, path))
        except DOINotFound:
            styles.bad_typer_print(
                f'DOI found for entity {entity_type}({lable_str}) is invalid, see https://doi.org/{doi} for details'
            )
            raise typer.Exit(code=1)
        except ConnectionTimeoutError:
            styles.bad_typer_print(f'Download request timed out, see https://doi.org/{doi} for details')
            raise typer.Exit(code=1)
        except DeadUrlError as exc:
            styles.bad_typer_print(
                f'DOI redirects to a dead url {exc.dead_url}, https://doi.org/{doi} for details'
            )
            raise typer.Exit(code=1)

    styles.delimiter()
    styles.console.print(f'Finished downloading, files extracted to {str(path)!r}')


@download_app.command(name="check")
def check_doi(
    doi: str = typer.Option(..., '--doi', help='Doi to download'),
):
    """
    Download a doi from Caltech Data.
    """
    with styles.console.status('Downloading DOI zip...'):
        try:
            link = asyncio.run(get_redirect_link_from_doi(doi))
            if link is None:
                styles.bad_typer_print(f'DOI webpage did not redirect, see https://doi.org/{doi} for details')
                return
            elif link.startswith('https://www.mpsjcap.org'):
                styles.bad_typer_print(f'Found bad redirect url, {link}, connection will likely fail.')
            else:
                styles.console.print(f'Redirect link {link} found for doi {doi}')
            zip_links = asyncio.run(get_zip_links_from_doi(doi))
            if zip_links:
                styles.console.print(f'Zip links found for doi {doi}, {(", ".join(zip_links))}')
        except RequestLimitation:
            styles.bad_typer_print(f'You have made too many requests, please wait and try again.')
            raise typer.Exit(code=1)
        except MPSClientException:
            styles.bad_typer_print(f'DOI is invalid, see https://doi.org/{doi} for details')
            raise typer.Exit(code=1)
    styles.delimiter()
