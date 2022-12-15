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

from typing import Optional

from mps_client.database.graph import GraphDriver, get_neo4j_driver


def run_raw_graph_query(query: str, graph_driver: Optional[GraphDriver] = None):
    if graph_driver is None:
        graph_driver = get_neo4j_driver()
    return graph_driver.fetch_all(query)
