from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

from config import types


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: types.HANDLER_TYPE,
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data["session"] = session
            return await handler(event, data)


class ContextMiddleware(BaseMiddleware):
    def __init__(self, **context):
        super().__init__()
        self.context = context

    async def __call__(
            self,
            handler: types.HANDLER_TYPE,
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        data.update(self.context)
        return await handler(event, data)
