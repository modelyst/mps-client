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

"""Utilities for converting and coercing types."""

import inspect
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from json import dumps
from typing import Any, Callable
from uuid import UUID


def get_function_signature(function: Callable[..., Any]) -> inspect.Signature:
    # Adapted from fastapi
    # https://github.com/tiangolo/fastapi/blob/master/fastapi/dependencies/utils.py
    sig = inspect.signature(function)
    typed_params = [
        inspect.Parameter(
            name=param.name,
            kind=param.kind,
            default=param.default,
            annotation=param.annotation,
        )
        for param in sig.parameters.values()
    ]
    typed_signature = inspect.Signature(typed_params)
    return typed_signature


# Utilities for converting types
def escape_str_replace(text: Any) -> str:
    return str(text).replace('\\', '\\\\').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')


datetime_types = (datetime, time, date)
datetime_to_str = lambda x: x.isoformat() if x is not None else str(x)
timedelta_to_str = lambda x: str(x.total_seconds()) if x is not None else str(x)
basic_to_str = lambda x: escape_str_replace(x)
bytes_to_str = lambda x: escape_str_replace(x.decode('utf-8')) if x is not None else str(x)


def json_dumps(thing):
    def json_default(thing: Any) -> str:
        if isinstance(thing, datetime_types):
            return thing.isoformat()
        elif isinstance(thing, timedelta):
            return timedelta_to_str(thing)
        elif isinstance(thing, bytes):
            return bytes_to_str(thing)
        elif isinstance(thing, (Decimal, UUID)):
            return escape_str_replace(thing)
        elif isinstance(thing, set):
            return str(list(thing))
        raise TypeError(f"Cannot serialize object of type {type(thing)}: {thing}")

    return dumps(thing, default=json_default)
