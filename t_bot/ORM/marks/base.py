from datetime import date

from sqlalchemy import String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, declared_attr, column_property


class BaseMark:
    fio: Mapped[str]
    date: Mapped[date]
    group = mapped_column(String(length=10))
    course: Mapped[int]
