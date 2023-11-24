from typing import Any, Iterable

from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject

from config import settings

UserIDType = int | str | Iterable[int] | Iterable[str]


class UserIDFilter(BaseFilter):
    def __init__(self, users_id: UserIDType):
        if not isinstance(users_id, (list, set)):
            users_id = [users_id]
        self.users_id = users_id

    async def __call__(self,
                       obj: TelegramObject,
                       raw_state: str | None = None) -> bool | dict[str, Any]:
        if str(obj.from_user.id) not in self.users_id:
            return False
        return True


class AdminFilter(UserIDFilter):
    def __init__(self):
        super().__init__(settings.ADMINS)
