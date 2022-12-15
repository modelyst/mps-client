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

from mps_client.database.graph import get_neo4j_driver


def test_driver_instantiations():
    driver = get_neo4j_driver()
    driver.verify_connectivity()


def test_driver():
    driver = get_neo4j_driver()
    rows = driver.fetch_all('match (n) return n limit 10 ')
    assert isinstance(rows, list)
