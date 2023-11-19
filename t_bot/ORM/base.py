from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config.settings import ENV


class Base(DeclarativeBase):
    pass


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
