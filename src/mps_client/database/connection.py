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

import logging
import urllib
from typing import Optional, Union, cast

from pydantic import BaseModel, Field
from pydantic.networks import PostgresDsn
from pydantic.tools import parse_obj_as
from pydantic.types import SecretStr
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from mps_client.utils.type_coercion import json_dumps

logger = logging.getLogger(__name__)


class Connection(BaseModel):
    scheme: str = "postgresql"
    user: str = "postgres"
    password: Optional[SecretStr] = None
    host: str = "localhost"
    port: int = 5432
    database: str = "mpsjcap"
    schema_: str = Field('public', alias="schema")

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.url()

    @classmethod
    def from_uri(
        cls, uri: Union[PostgresDsn, str], schema: str, password: Optional[SecretStr] = None
    ) -> "Connection":
        if isinstance(uri, str):
            uri = parse_obj_as(PostgresDsn, uri)
            uri = cast(PostgresDsn, uri)

        assert uri.path, f"uri is missing database {uri}"
        return cls(
            host=uri.host or "localhost",
            user=uri.user,
            password=urllib.parse.quote(password.get_secret_value()) if password else uri.password,
            port=uri.port or 5432,
            database=uri.path.lstrip("/"),
            schema=schema,
        )

    def url(self, mask_password: bool = True, with_schema: bool = False):
        if mask_password:
            password = "******"
        elif self.password:
            password = self.password.get_secret_value()
        else:
            password = ""
        schema_suffix = f"?options=--search_path%3d{self.schema_}" if with_schema else ""
        return (
            f"{self.scheme}://{self.user}:{password}@{self.host}:{self.port}/{self.database}{schema_suffix}"
        )

    def get_engine(self, echo: bool = False):
        return create_engine(
            url=self.url(mask_password=False),
            connect_args={"options": f"-csearch_path={self.schema_}"},
            json_serializer=json_dumps,
            echo=echo,
        )

    def test(self):
        engine = self.get_engine()
        try:
            with engine.connect() as conn:
                conn.execute("select 1")
        except OperationalError as exc:
            logger.error(f"Trouble connecting to database at {self}.\n{exc}")
            return False
        return True
