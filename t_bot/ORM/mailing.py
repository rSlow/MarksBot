from sqlalchemy import select
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base, Session


class Mailing(Base):
    telegram_id: Mapped[int]
    group: Mapped[str] = mapped_column(nullable=True)
    course: Mapped[int] = mapped_column(nullable=True)
    all: Mapped[bool] = mapped_column(nullable=True, default=False)

    @classmethod
    async def get_all(cls):
        async with Session() as session:
            q = select(cls)
            res = await session.execute(q)
            return res.scalars().all()
