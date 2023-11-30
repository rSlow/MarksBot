from abc import ABC
from datetime import date as d

import pydantic


class IntIDMixin:
    id: int


class SBaseMark(pydantic.BaseModel, ABC):
    fio: str
    date: d
    group: str = pydantic.Field(max_length=10)
    course: int


class SStudyMarkIn(SBaseMark):
    subject: str | None = None
    pair_number: int | None = None
    mark: str = pydantic.Field(max_length=1)
    is_in_last_month: bool = False
    mark_num_index: int = pydantic.Field(ge=1, le=2)

    class Config:
        from_attributes = True

    __hash: int = None

    @property
    def __get_hash(self):
        if self.__hash is None:
            self.__hash = hash(
                (self.fio,
                 self.date,
                 self.subject,
                 self.pair_number,
                 self.group,
                 self.is_in_last_month,
                 self.mark_num_index)
            )
        return self.__hash

    def __hash__(self):
        return self.__get_hash

    def __eq__(self, other):
        if isinstance(other, SStudyMarkIn):
            if all((
                    hash(self) == hash(other),
                    self.mark == other.mark,
            )):
                return True
        return False


class SStudyMarkOut(IntIDMixin, SStudyMarkIn):
    pass


class SPracticeMarkIn(SBaseMark):
    pass


class SPracticeMarkout(IntIDMixin, SPracticeMarkIn):
    pass


class SMailing(IntIDMixin, pydantic.BaseModel):
    telegram_id: int
    group: str | None = None
    course: int | None = None
    all: bool = False

    class Config:
        from_attributes = True
