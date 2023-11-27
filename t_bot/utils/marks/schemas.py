from typing import Type

import pydantic

from ORM.schemas import SMarkIn, SMarkOut
from .filters import BaseFilter


class SUpdated(pydantic.BaseModel):
    new_schema: SMarkIn
    old_schema: SMarkOut


class SAnalyze(pydantic.BaseModel):
    updated_schemas: list[SUpdated]
    added_schemas: list[SMarkIn]
    unused_schemas: list[SMarkOut]


class SMode(pydantic.BaseModel):
    filter_attr: str
    filter: Type[BaseFilter]
