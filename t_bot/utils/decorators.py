import time
from loky import ProcessPoolExecutor

import asyncio
from functools import wraps, partial
from typing import Callable, Any, Coroutine, TypeVar

from config.logger import logger

_T = TypeVar('_T')
F = Callable[..., _T]
C = Callable[..., Coroutine[Any, Any, _T]]


class TimeCounter:
    MESSAGE = "func <{name}> execute for {time} seconds"

    @classmethod
    def sync(cls, func: F) -> F:
        @wraps(func)
        def inner(*args, **kwargs):
            start = time.time()
            res = func(*args, **kwargs)
            logger.info(cls.MESSAGE.format(name=func.__name__, time=round(time.time() - start, 2)))
            return res

        return inner

    @classmethod
    def a_sync(cls, cor: F) -> C:
        @wraps(cor)
        async def inner(*args, **kwargs):
            start = time.time()
            res = await cor(*args, **kwargs)
            logger.info(cls.MESSAGE.format(name=cor.__name__, time=round(time.time() - start, 2)))
            return res

        return inner


def set_async(func: F, *_, **__) -> C:
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, partial(func, *args, **kwargs)
        )

    return wrapper


def set_process_async(func: F, *_, **__) -> C:
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any):
        loop = asyncio.get_event_loop()
        with ProcessPoolExecutor() as pool:
            res = await loop.run_in_executor(
                pool, partial(func, *args, **kwargs)
            )
        return res

    return wrapper
