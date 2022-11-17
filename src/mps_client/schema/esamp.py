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

from datetime import datetime
from typing import List, Optional

from dbgen import IDType
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship

from mps_client.schema.base import BaseTable, sa_registry

indexed_col = Field(..., sa_column_kwargs={'index': True})


class Collection(BaseTable, table=True, registry=sa_registry):
    __identifying__ = {'label', 'type'}
    label: str = indexed_col
    type: str = indexed_col
    release_name: str
    details: Optional[dict] = Field(None, sa_column=Column(JSONB))
    updated_on: Optional[datetime]
    screening_map_id: Optional[int]
    doi: Optional[str]


class Sample(BaseTable, table=True, registry=sa_registry):
    __identifying__ = {'label', 'type'}
    label: str = indexed_col
    type: str = indexed_col
    details: Optional[dict]
    initial_composition: Optional[dict]
    final_composition: Optional[dict]
    inkjet_composition: Optional[dict]
    xrfs_composition: Optional[dict]
    interpolated_xrfs_composition: Optional[dict]

    # Relationship
    sample_processes: List['SampleProcess'] = Relationship(back_populates="sample")


class CollectionSample(BaseTable, table=True, registry=sa_registry):
    __tablename__ = 'collection__sample'
    __identifying__ = {'sample_id', 'collection_id'}
    sample_id: IDType = Sample.foreign_key()
    collection_id: IDType = Collection.foreign_key()


class SampleParent(BaseTable, table=True, registry=sa_registry):
    __tablename__ = 'sample_parent'
    __identifying__ = {'parent_id', 'child_id'}
    parent_id: IDType = Sample.foreign_key()
    child_id: IDType = Sample.foreign_key()


class ProcessDetail(BaseTable, table=True, registry=sa_registry):
    __tablename__ = 'process_detail'
    __identifying__ = {'type', 'technique', 'parameters'}
    type: str = indexed_col
    technique: str = indexed_col
    parameters: Optional[dict]
    mapped_parameters: Optional[dict]


class Process(BaseTable, table=True, registry=sa_registry):
    __identifying__ = {'machine_name', 'timestamp', 'ordering'}
    machine_name: str
    timestamp: datetime
    ordering: int
    process_detail_id: IDType = ProcessDetail.foreign_key()

    # Relationship
    sample_processes: List['SampleProcess'] = Relationship(back_populates="process")


class SampleProcess(BaseTable, table=True, registry=sa_registry):
    __tablename__ = 'sample_process'
    __identifying__ = {'sample_id', 'process_id', 'relationship'}
    sample_id: IDType = Sample.foreign_key()
    process_id: IDType = Process.foreign_key()
    relationship: Optional[str]
    inheritance: Optional[str]
    rank: Optional[int]
    leaf: Optional[bool]

    # Relationship
    sample: Optional[Sample] = Relationship(back_populates="sample_processes")
    process: Optional[Process] = Relationship(back_populates="sample_processes")


class ProcessData(BaseTable, table=True, registry=sa_registry):
    __tablename__ = 'process_data'
    __identifying__ = {'release_name', 'path', 'file_name', 'begin_line', 'end_line', 'bucket_name'}
    bucket_name: Optional[str]
    release_name: str
    path: str
    file_name: str
    file_type: str
    begin_line: Optional[int]
    end_line: Optional[int]
    raw_data_json: Optional[dict]
    extracted_path: Optional[str]


class SampleProcessProcessData(BaseTable, table=True, registry=sa_registry):
    __tablename__ = 'sample_process_process_data'
    __identifying__ = {'sample_process_id', 'process_data_id'}
    sample_process_id: IDType = SampleProcess.foreign_key()
    process_data_id: IDType = ProcessData.foreign_key()


class AnalysisDetail(BaseTable, table=True, registry=sa_registry):
    __tablename__ = 'analysis_details'
    __identifying__ = {'name', 'details'}
    name: str
    details: dict


class Analysis(BaseTable, table=True, registry=sa_registry):
    __tablename__ = 'analysis'
    __identifying__ = {'name', 'input', 'output', 'analysis_detail_id'}
    name: str
    input: dict
    output: dict
    analysis_detail_id: IDType = AnalysisDetail.foreign_key()


class ProcessDataAnalysis(BaseTable, table=True, registry=sa_registry):
    __tablename__ = 'process_data_analysis'
    __identifying__ = {'keyword', 'process_data_id', 'analysis_id'}
    keyword: str
    process_data_id: IDType = ProcessData.foreign_key()
    analysis_id: IDType = Analysis.foreign_key()
