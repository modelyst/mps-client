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
import typer

import mps_client.cli.styles as styles
from mps_client.database.session import get_connection

database_app = typer.Typer(name='database', no_args_is_help=True, help="Test connection to the database.")


@database_app.command(name="test")
def test_connection(
    show_password: bool = typer.Option(
        False, "-p", "--show-password", help="Expose password in printed dsn when testing."
    ),
):
    """
    Test connections to the database
    """

    styles.delimiter()
    failed = False
    styles.good_typer_print(f"Checking Database connection...")
    conn = get_connection()
    check = conn.test()
    if check:
        styles.good_typer_print(f"Connection to Database at {conn.url(not show_password,True)} all good!")
    else:
        styles.bad_typer_print(f"Cannot connect to Database at {conn.url(not show_password,True)}!")
        failed = True
    styles.delimiter()
    raise typer.Exit(code=2 if failed else 0)
