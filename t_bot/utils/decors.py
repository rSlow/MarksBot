import time
from functools import wraps


def time_count(func):
    @wraps(func)
    def inner(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print("----------")
        print(f"func <{func.__name__}> execute for {time.time() - start:.2f} seconds")
        return res

    return inner
