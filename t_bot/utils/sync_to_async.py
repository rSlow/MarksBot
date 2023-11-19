import asyncio
from functools import wraps, partial
from typing import Callable, Any, Coroutine, TypeVar

_T = TypeVar('_T')


def set_async(func: Callable[..., _T]) -> Callable[..., Coroutine[Any, Any, _T]]:
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, partial(func, *args, **kwargs)
        )

    return wrapper
