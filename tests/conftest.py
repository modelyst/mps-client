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

import os

import pytest
from sqlalchemy import MetaData
from sqlmodel import Session, create_engine

from mps_client.configuration import settings
from mps_client.schema.base import sa_registry


@pytest.fixture(scope="session", autouse=True)
def database_engine():
    """Produce a database engine"""
    engine = create_engine(os.environ.get('TEST_DSN') or settings.POSTGRES_DSN)
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture(scope='session')
def build_database_session(database_engine):
    metadata = MetaData(database_engine)
    metadata.reflect()
    metadata.drop_all()
    sa_registry.metadata.create_all(database_engine)
    yield
    sa_registry.metadata.drop_all(database_engine)


@pytest.fixture(scope='function')
def build_database(database_engine):
    metadata = MetaData(database_engine)
    metadata.reflect()
    metadata.drop_all()
    sa_registry.metadata.create_all(database_engine)
    yield
    sa_registry.metadata.drop_all(database_engine)


@pytest.fixture
def session(database_engine, build_database):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = database_engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()
