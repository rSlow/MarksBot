from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from datetime import date

from .base import Base, Session
from .schemas import SMarkIn


class Mark(Base):
    __tablename__ = "marks"

    id: Mapped[int] = mapped_column(primary_key=True)

    fio: Mapped[str]
    date: Mapped[date]
    subject: Mapped[str] = mapped_column(nullable=True)
    pair_number: Mapped[int] = mapped_column(nullable=True)
    mark = mapped_column(String(length=1), nullable=True)
    group: Mapped[str] = mapped_column(String(length=10))
    course: Mapped[int]

    def __str__(self):
        return f"{self.fio} - {self.subject} - {self.mark} ({self.date})"

    __repr__ = __str__

    @classmethod
    async def set_data(cls, data: list[SMarkIn]):
        objects = [cls(**schema.model_dump()) for schema in data]
        async with Session() as session:
            async with session.begin():
                session.add_all(objects)
