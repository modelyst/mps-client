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
from pathlib import Path
from typing import List, Optional
from uuid import UUID

import typer
from rich.table import Table

import mps_client.cli.styles as styles
from mps_client._enums import EntityType
from mps_client.core.queries import get_doi, get_process_history, get_sample, run_raw_query

query_app = typer.Typer(name='query', no_args_is_help=True, help="Test connection to the database.")


@query_app.command(name="run")
def run_raw_query_command(
    sql_file: Optional[Path] = typer.Option(None, '--file', help='Path to sql file to run query from'),
    raw_sql: Optional[str] = typer.Option(None, '--raw', help='Raw sql to run.'),
    number_of_rows: int = typer.Option(10, '-n', help='Number of rows to print to the screen.'),
    fields: Optional[List[str]] = typer.Option(
        None, '--field', help='Number of rows to print to the screen.'
    ),
):
    """
    Run raw sql queries against the database
    """
    if sql_file:
        command = sql_file.read_text()
    elif raw_sql:
        command = raw_sql
    else:
        raise typer.BadParameter('Need to provide --file or --raw.')

    with styles.console.status('Running Query...'):
        result = run_raw_query(command)
    if result:
        table = Table(title=str(sql_file) if sql_file else command, width=styles.console.width)
        if fields:
            if len(fields) != len(result[0]):
                raise typer.BadParameter(
                    f'Incorrect number of fields provided for query output. Expected {len(result[0])} but given {len(fields)}',
                    param_hint='fields',
                )
            for field in fields:
                table.add_column(field)
        else:
            for i in range(len(result[0])):
                table.add_column(f'Column {i}')

        styles.console.print(
            f'Query finished. It returned {len(result)} row(s). Showing first {number_of_rows} rows'
        )
        styles.delimiter()
        for row in result[:number_of_rows]:
            table.add_row(*map(str, row))
        styles.console.print(table)
    else:
        styles.bad_typer_print('No data returned.')


@query_app.command(name="get-doi")
def get_doi_command(
    entity_type: EntityType = typer.Option(..., '--entity', help='Path to sql file to run query from'),
    entity_id: Optional[UUID] = typer.Option(None, '--id', help='Path to sql file to run query from'),
    entity_label: Optional[str] = typer.Option(None, '--label', help='Path to sql file to run query from'),
):
    """
    Test connections to the database
    """
    doi = get_doi(entity_type=entity_type, entity_id=entity_id, entity_label=entity_label)
    if doi:
        styles.console.print(f'Entity {entity_type} has doi: {doi}')
        styles.console.print(f'Access it at the url https://doi.org/{doi}')
        styles.console.print(
            f'Download it with command \'mps-client download doi --doi {doi} --path output\''
        )
    else:
        styles.bad_typer_print(f'Entity {entity_type}(id={entity_id}) does not have a doi')


@query_app.command(name="get-process-history")
def get_process_history_command(
    sample_id: Optional[UUID] = typer.Option(None, '--id', help='Path to sql file to run query from'),
    sample_label: Optional[str] = typer.Option(None, '--label', help='Path to sql file to run query from'),
):
    """
    Test connections to the database
    """
    process_history = get_process_history(sample_id, sample_label)
    id_str = f'id={sample_id}' if sample_id else f'label={sample_label}'
    id_str = f'Sample({id_str})'
    process_ids, type_list, tech_list = process_history
    if process_ids:
        history = (f'{proc_type}({tech})' for proc_type, tech in zip(type_list, tech_list))
        styles.console.print(f'{id_str} has history:')
        history_string = ' -> '.join(history)
        styles.console.print(f'{history_string}')
    else:
        sample = get_sample(sample_id, sample_label)
        if sample is None:
            styles.bad_typer_print(f'{id_str} could not be found.')
        else:
            styles.bad_typer_print(f'{id_str} has no process history.')
