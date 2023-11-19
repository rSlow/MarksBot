from typing import Callable, Any, Awaitable

from aiogram.types import TelegramObject

HANDLER_TYPE = Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]
