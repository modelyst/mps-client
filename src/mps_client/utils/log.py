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

from rich.console import Console
from rich.logging import RichHandler

from mps_client.configuration import settings

_ROOT_LOGGER_NAME = "mps_client"
console = Console()


def setup_logger():
    logger = logging.getLogger(_ROOT_LOGGER_NAME)
    logger.setLevel(settings.LOG_LEVEL.get_log_level())
    logger.addHandler(RichHandler(console=console))
    return logger


def get_logger():
    return logging.getLogger(_ROOT_LOGGER_NAME)
