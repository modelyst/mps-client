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

from typing import List, Optional

import sqlalchemy as sa
from sqlalchemy.ext import compiler
from sqlalchemy.schema import DDLElement, PrimaryKeyConstraint


class CreateMaterializedView(DDLElement):
    def __init__(self, name, selectable, schema):
        self.name = name
        self.selectable = selectable
        self.schema = schema


@compiler.compiles(CreateMaterializedView)
def compile(element, compiler, **kw):
    # Could use "CREATE OR REPLACE MATERIALIZED VIEW..."
    # but I'd rather have noisy errors
    return "CREATE MATERIALIZED VIEW {}.{} AS {} WITH DATA".format(
        element.schema,
        element.name,
        compiler.sql_compiler.process(element.selectable, literal_binds=True),
    )


def create_mat_view(
    name,
    selectable,
    schema,
    metadata: sa.MetaData,
    columns: Optional[List[sa.Column]] = None,
):
    _mt = sa.MetaData(schema=schema)  # temp metadata just for initial Table object creation
    t = sa.Table(name, _mt)  # the actual mat view class is bound tosa.metadata
    if columns is None and getattr(selectable, "c", None):
        columns = [sa.Column(c.name, c.type, primary_key=c.primary_key) for c in selectable.c]

    assert columns
    for c in columns:
        t.append_column(c)

    if not (any([c.primary_key for c in columns])):
        t.append_constraint(PrimaryKeyConstraint(*[c.name for c in columns]))

    sa.event.listen(metadata, "after_create", CreateMaterializedView(name, selectable, schema))

    @sa.event.listens_for(metadata, "after_create")
    def create_indexes(target, connection, **kw):
        for idx in t.indexes:
            idx.create(connection)

    sa.event.listen(metadata, "before_drop", sa.DDL(f"DROP VIEW IF EXISTS {schema}.{name}"))
    return t
