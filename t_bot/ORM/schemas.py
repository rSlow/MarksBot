import pydantic
from datetime import date as d


class SMarkIn(pydantic.BaseModel):
    fio: str
    date: d
    subject: str | None = None
    pair_number: int | None = None
    mark: str | None = pydantic.Field(None, max_length=1)
    group: str = pydantic.Field(max_length=10)
    course: int


class SMarkOut(SMarkIn):
    id: int
