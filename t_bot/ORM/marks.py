from datetime import date

from sqlalchemy import String, select, delete
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base, Session
from .schemas import SMarkIn, SMarkOut


class Mark(Base):
    __tablename__ = "marks"

    id: Mapped[int] = mapped_column(primary_key=True)

    fio: Mapped[str]
    date: Mapped[date]
    subject: Mapped[str] = mapped_column(nullable=True)
    pair_number: Mapped[int] = mapped_column(nullable=True)
    mark = mapped_column(String(length=1))
    group = mapped_column(String(length=10))
    course: Mapped[int]

    is_in_last_month: Mapped[bool] = mapped_column(default=False)
    mark_num_index: Mapped[int]

    def __str__(self):
        return f"{self.fio} - {self.subject} - {self.mark} ({self.date})"

    __repr__ = __str__

    @classmethod
    async def gel_all(cls):
        async with Session() as session:
            q = select(cls)
            res = await session.execute(q)
            mark_object_list = res.scalars().all()
            mark_schema_list = [SMarkOut.model_validate(mark_object) for mark_object in mark_object_list]
        return mark_schema_list

    @classmethod
    async def set_data(cls, data: list[SMarkIn]):
        objects = [cls(**schema.model_dump()) for schema in data]
        if objects:
            async with Session() as session:
                async with session.begin():
                    session.add_all(objects)

    @classmethod
    async def clear_id_list(cls, ids: list[int]):
        if ids:
            async with Session() as session:
                async with session.begin():
                    q = delete(cls).filter(
                        cls.id.in_(ids)
                    )
                    await session.execute(q)
