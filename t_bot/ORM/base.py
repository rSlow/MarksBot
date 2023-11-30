from sqlalchemy import Select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

from config.settings import ENV


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(self) -> str:
        return self.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)


URL = ENV.str("DATABASE_URL")

Engine = create_async_engine(
    url=URL,
    echo=True,
)
Session = async_sessionmaker(
    bind=Engine,
    expire_on_commit=False,
    autoflush=True
)


async def create_database() -> None:
    try:
        from ORM.marks import Mark
        async with Engine.begin() as conn:
            conn.run_sync(Base.metadata.create_all)

    except ImportError:
        raise


async def stop_database() -> None:
    await Engine.dispose()


async def fetch_query(session: AsyncSession, query: Select):
    res = await session.execute(query)
    info = res.fetchall()
    return info


async def fetch_scalars(session: AsyncSession, query: Select):
    res = await session.execute(query)
    info = res.scalars().all()
    return info
