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
from pathlib import Path
from typing import Optional

import typer

from mps_client import __version__
from mps_client.cli import styles
from mps_client.cli.commands.database import database_app
from mps_client.cli.commands.download import download_app
from mps_client.cli.commands.query import query_app
from mps_client.configuration import settings
from mps_client.utils.log import setup_logger

logger = logging.getLogger(__name__)

app = typer.Typer(no_args_is_help=True)
app.add_typer(database_app)
app.add_typer(query_app)
app.add_typer(download_app)


@app.callback()
def setup():
    setup_logger()


@app.command(name='version')
def version(short: bool = typer.Option(False, '-s', help='Print the raw version with no ascii art.')):
    """Display mps-plotting version info"""
    if short:
        styles.console.print(__version__)
    else:
        styles.console.print(styles.LOGO_STYLE)


@app.command(name="config")
def get_config(
    show_password: bool = False,
    show_defaults: bool = False,
    simple: bool = False,
    out_pth: Optional[Path] = typer.Option(
        None,
        '--out',
        '-o',
        help="Location to write parametrized config",
    ),
):
    """
    Prints out the configuration of mps-plotting
    """
    # If out_pth provided write the current config to the path provided and return
    if out_pth:
        with open(out_pth, "w") as f:
            f.write(settings.display(True, True))

    styles.theme_typer_print(settings.display(show_defaults, show_password, simple))
