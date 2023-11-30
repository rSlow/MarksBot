from sqlalchemy import select, distinct, func, delete

from sqlalchemy.ext.asyncio import AsyncSession

from ..base import Base, Session, fetch_scalars, fetch_query
from ..marks.base import BaseMark
from ..schemas import SPracticeMarkIn


class PracticeMark(BaseMark, Base):
    pass

    @classmethod
    async def _(cls):
        ...

    @classmethod
    async def set_data(cls, data: list[SPracticeMarkIn]):
        objects = [cls(**schema.model_dump()) for schema in data]
        if objects:
            async with Session() as session:
                async with session.begin():
                    await session.execute(delete(cls))
                    session.add_all(objects)

    @classmethod
    async def get_all(cls, session: AsyncSession):
        q = select(
            cls
        ).order_by(
            cls.date
        )
        return await fetch_scalars(session, q)

    @classmethod
    async def get_info(cls, session: AsyncSession):
        q = select(
            func.count(distinct(cls.fio)),
            func.count(cls.fio)
        )
        return (await fetch_query(session, q))[0]
