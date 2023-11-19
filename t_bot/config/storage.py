from typing import Any, Union, Type

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage

from config.settings import ENV

redis_storage = RedisStorage.from_url(ENV.str("REDIS_URL"))

ValueType = Union[int, str, float, bool, Type[None]]


async def get_category_data(
        state: FSMContext,
        category_key: str,
        category_default: Any,
):
    data = await state.get_data()
    category_data: dict[str, Any] = data.get(category_key, category_default)
    return category_data


async def set_category_value(
        state: FSMContext,
        category_key: str,
        category_default: Any,
        param: str,
        value: ValueType
):
    data = await state.get_data()
    category_data: dict[str, Any] = data.get(category_key, category_default)
    category_data[param] = value
    await state.update_data({category_key: category_data})
