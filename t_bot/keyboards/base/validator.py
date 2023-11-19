from abc import ABC, abstractmethod, abstractproperty
from typing import Any

from aiogram.types import KeyboardButton

from config import settings


class BaseButtonValidator(ABC):
    arg_name: str = abstractproperty

    @abstractmethod
    def validate(self, value: Any) -> Any:
        pass


class UserIDValidator(BaseButtonValidator):
    arg_name = "user_id"

    def __init__(self, user_id: int | str | list[str | int]):
        super().__init__()
        if not isinstance(user_id, list):
            self.user_id = [str(user_id)]
        else:
            self.user_id = [str(v) for v in user_id]

    def validate(self, value: str | int) -> Any:
        if str(value) not in str(self.user_id):
            return False
        return True


class IsAdminValidator(UserIDValidator):
    def __init__(self):
        super().__init__(user_id=settings.ADMINS)


class ButtonWithValidator(KeyboardButton):
    def __init__(self, text: str, validator: BaseButtonValidator):
        super().__init__(text=text)
        self.validator = validator
