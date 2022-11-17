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
from typing import Optional, Type, Union
from uuid import UUID

from sqlalchemy.dialects.postgresql import aggregate_order_by
from sqlmodel import Session, func, select, text

from mps_client._enums import EntityType
from mps_client.database.session import get_engine
from mps_client.schema.esamp import Collection, Process, ProcessDetail, Sample, SampleProcess
from mps_client.schema.jcap import JcapAnalysis, JcapRun

logger = logging.getLogger(__name__)
engine = get_engine()


def run_raw_query(query: str):
    with Session(engine) as session:
        result = session.exec(text(query)).all()
    return result


def get_process_history(sample_id: Optional[UUID] = None, sample_label: Optional[str] = None):
    """
    Get the process history of a given sample_id or sample_id.

    Only a sample_id or sample_label should be provided not both

    Args:
        sample_id (Optional[UUID]): The UUID of the sample to get the history for
        sample_label (Optional[str]): The Label of the sample to get the history for

    Returns:
        Tuple[List[str],List[str]]: A tuple of the list of time ordered types, and list of time ordered techniques.
    """
    with Session(engine) as session:
        stmt = (
            select(
                func.ARRAY_AGG(aggregate_order_by(Process.id, Process.timestamp, Process.ordering)).label(
                    'process_id'
                ),
                func.ARRAY_AGG(
                    aggregate_order_by(ProcessDetail.type, Process.timestamp, Process.ordering)
                ).label('process_type'),
                func.ARRAY_AGG(
                    aggregate_order_by(ProcessDetail.technique, Process.timestamp, Process.ordering)
                ).label('process_technique'),
            )
            .select_from(Sample)
            .join(SampleProcess)
            .join(Process)
            .join(ProcessDetail)
        )
        if sample_id:
            stmt = stmt.where(Sample.id == sample_id)
        elif sample_label:
            stmt = stmt.where(Sample.label == sample_label)
        stmt = stmt.group_by(Sample.id)
        result = session.exec(stmt).one_or_none()
        if result is None:
            return [], [], []
    return result


def get_sample(sample_id: Optional[UUID] = None, sample_label: Optional[str] = None) -> Optional[Sample]:
    """
    Get a sample by its ID or Label

    Only a sample_id or sample_label should be provided not both

    Args:
        sample_id (Optional[UUID]): The UUID of the sample to get the history for
        sample_label (Optional[str]): The Label of the sample to get the history for

    Returns:
        Tuple[List[str],List[str]]: A tuple of the list of time ordered types, and list of time ordered techniques.
    """
    if not sample_label and not sample_id:
        raise ValueError('Need to provide sample_label or sample_id.')
    elif sample_label and sample_id:
        raise ValueError('Need to provide sample_label or sample_id, not both.')
    with Session(engine) as session:
        stmt = select(Sample)
        if sample_id:
            stmt = stmt.where(Sample.id == sample_id)
        elif sample_label:
            stmt = stmt.where(Sample.label == sample_label)
        result = session.exec(stmt).one_or_none()
    return result


def get_doi(entity_type: EntityType, entity_id: Optional[UUID], entity_label: Optional[str]) -> Optional[str]:
    table: Union[Type[Collection], Type[JcapRun], Type[JcapAnalysis]]
    if entity_type == EntityType.PLATE:
        table = Collection
    elif entity_type == EntityType.RUN:
        table = JcapRun
    elif entity_type == EntityType.ANALYSIS:
        table = JcapAnalysis
    else:
        raise ValueError(f'Unknown entity_type: {entity_type}')

    # Ensure we have at least an id or label
    if not (entity_label or entity_id):
        raise ValueError('Must provide at least an id or label.')
    # Check that we provided label for the right entity type
    if entity_label and entity_type not in EntityType.PLATE:
        raise ValueError(f'Cannot provide a label for entity: {entity_type}')

    stmt = select(table.doi)
    if entity_id:
        stmt = stmt.where(table.id == entity_id)
    elif entity_label:
        stmt = stmt.where(table.label == entity_label)

    with Session(engine) as session:
        result = session.exec(stmt).one_or_none()
    return result
