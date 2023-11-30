from datetime import date, timedelta

from sqlalchemy import String, select, delete, func, Integer, distinct, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import mapped_column, Mapped

from config import settings
from .base import BaseMark
from ..base import Base, Session, fetch_query, fetch_scalars
from ..schemas import SStudyMarkIn, SStudyMarkOut


class StudyMark(BaseMark, Base):
    subject: Mapped[str] = mapped_column(nullable=True)
    pair_number: Mapped[int] = mapped_column(nullable=True)
    mark = mapped_column(String(length=1))

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
            mark_schema_list = [SStudyMarkOut.model_validate(mark_object) for mark_object in mark_object_list]
        return mark_schema_list

    @classmethod
    async def set_data(cls, data: list[SStudyMarkIn]):
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

    @classmethod
    async def get_two_faculty_info(cls,
                                   session: AsyncSession):
        courses = settings.COURSES

        series = select(
            func.generate_series(
                min(courses),
                max(courses),
                1
            ).label('crs')
        ).subquery()

        values = select(
            cls.course,
            func.count(distinct(cls.fio)).label('twos'),
            func.count(cls.mark).label('marks'),
        ).filter(
            cls.mark == "2"
        ).group_by(
            cls.course
        ).subquery()

        q = select(
            series.c.crs,
            func.coalesce(values.c.twos, 0),
            func.coalesce(values.c.marks, 0),
        ).outerjoin(
            values,
            values.c.course == series.c.crs,
        ).order_by(
            series.c.crs
        )

        return await fetch_query(session, q)

    @classmethod
    async def get_faculty_average(cls,
                                  session: AsyncSession):
        q = select(
            cls.course,
            func.round(func.avg(cls.mark.cast(Integer)), 2).label("avg")
        ).filter(
            cls.mark.in_(["2", "3", "4", "5"])
        ).filter_by(
            is_in_last_month=False
        ).group_by(
            cls.course
        ).order_by(
            cls.course
        )
        return await fetch_query(session, q)

    @classmethod
    async def get_two_today_info(cls,
                                 session: AsyncSession):
        q = select(
            cls
        ).filter(
            cls.date == date.today()
        ).filter(
            cls.mark == "2"
        ).order_by(
            cls.course,
            cls.group,
            cls.fio
        )
        return await fetch_scalars(session, q)

    @classmethod
    async def get_twos_long_two_weeks(cls,
                                      session: AsyncSession):
        q = select(
            cls
        ).filter(
            cls.date <= date.today() - timedelta(weeks=2)
        ).filter(
            cls.mark == "2"
        ).order_by(
            cls.course,
            cls.group,
            cls.fio
        )
        return await fetch_scalars(session, q)


def add_query(model: StudyMark, q: Select):
    return q.filter(
        model.mark == "2"
    ).order_by(
        model.course,
        model.group,
        model.fio
    )
