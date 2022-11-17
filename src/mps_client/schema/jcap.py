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
from typing import Optional

from dbgen import Entity, IDType

from mps_client.schema.base import BaseTable, sa_registry


class BaseJcapFile(Entity):
    __identifying__ = {'path', 'release_name', 's3_bucket'}
    release_name: str
    s3_bucket: Optional[str]
    full_s3_path: Optional[str]
    path: str
    timestamp: Optional[datetime]
    updated_on: Optional[datetime]
    summary_file: Optional[str]
    yaml_dict: Optional[dict]
    run_type: Optional[str]
    doi: Optional[str]


class JcapRun(BaseJcapFile, table=True, registry=sa_registry):
    __tablename__ = f'jcap_run'
    __identifying__ = {'path', 'release_name'}
    run_exists: Optional[bool]
    jcap_plate_id: Optional[int]


class JcapExperiment(BaseJcapFile, table=True, registry=sa_registry):
    __tablename__ = f'jcap_experiment'
    __identifying__ = {'path', 'release_name'}


class JcapAnalysis(BaseJcapFile, table=True, registry=sa_registry):
    __tablename__ = f'jcap_analysis'
    __identifying__ = {'path', 'release_name'}
    jcap_experiment_id: IDType = JcapExperiment.foreign_key()


class JcapExperimentRun(BaseTable, table=True, registry=sa_registry, all_identifying=True):
    __tablename__ = f'jcap_experiment_run'
    run_int: int
    jcap_experiment_id: IDType = JcapExperiment.foreign_key()
    jcap_run_id: IDType = JcapRun.foreign_key()


class JcapSubAnalysis(BaseTable, table=True, registry=sa_registry):
    __tablename__ = f'jcap_sub_analysis'
    __identifying__ = {'jcap_analysis_id', 'sub_analysis_int'}
    jcap_analysis_id: IDType = JcapAnalysis.foreign_key()
    sub_analysis_int: int
    name: Optional[str]
    technique: Optional[str]
    description: Optional[str]
    analysis_general_type: Optional[str]
    run_use_option: Optional[str]


class JcapFomFile(BaseTable, table=True, registry=sa_registry):
    __tablename__ = f'jcap_fom_file'
    __identifying__ = {'filename', 'jcap_sub_analysis_id'}
    jcap_sub_analysis_id: IDType = JcapSubAnalysis.foreign_key()
    filename: str
    file_type: str
    headers: Optional[str]


class JcapPatternFile(BaseTable, table=True, registry=sa_registry):
    __tablename__ = f'jcap_pattern_file'
    __identifying__ = {'filename', 'jcap_sub_analysis_id'}
    filename: str
    file_type: str
    headers: Optional[str]
    jcap_sample_id: int
    sample_label: str
    runint: int
    jcap_sub_analysis_id: IDType = JcapSubAnalysis.foreign_key()


class JcapLoading(BaseTable, table=True, registry=sa_registry):
    __tablename__ = f'jcap_loading'
    __identifying__ = {'jcap_fom_file_id', 'jcap_sample_id', 'jcap_plate_id', 'runint', 'line_number'}
    jcap_sample_id: int
    jcap_plate_id: int
    sample_label: str
    runint: int
    loading_json: Optional[dict]
    line_number: int
    jcap_fom_file_id: IDType = JcapFomFile.foreign_key()
