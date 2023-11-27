import time

from loky import ProcessPoolExecutor

import asyncio
from functools import wraps, partial
from typing import Callable, Any, Coroutine, TypeVar

_T = TypeVar('_T')
F = Callable[..., _T]
C = Callable[..., Coroutine[Any, Any, _T]]


def time_count(func: F) -> F:
    @wraps(func)
    def callable_inner(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(f"func <{func.__name__}> execute for {time.time() - start:.2f} seconds")
        return res

    return callable_inner


def set_process_async(func: F) -> C:
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any):
        with ProcessPoolExecutor() as pool:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                pool, partial(func, *args, **kwargs)
            )

    return wrapper
