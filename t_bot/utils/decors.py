import asyncio
import inspect
import time
from functools import wraps


def time_count(func):
    if inspect.iscoroutinefunction(func):
        print(True)

    @wraps(func)
    def callable_inner(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)

        print("----------")
        print(f"func <{func.__name__}> execute for {time.time() - start:.2f} seconds")
        return res

    return callable_inner
