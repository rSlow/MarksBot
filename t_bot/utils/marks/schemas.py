from typing import Type

import pydantic

from ORM.schemas import SStudyMarkIn, SStudyMarkOut
from .filters import BaseFilter


class SUpdated(pydantic.BaseModel):
    new_schema: SStudyMarkIn
    old_schema: SStudyMarkOut


class SAnalyze(pydantic.BaseModel):
    updated_schemas: list[SUpdated]
    added_schemas: list[SStudyMarkIn]
    unused_schemas: list[SStudyMarkOut]


class SMode(pydantic.BaseModel):
    filter_attr: str
    filter: Type[BaseFilter]
