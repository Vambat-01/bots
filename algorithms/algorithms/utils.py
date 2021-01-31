from typing import Callable, TypeVar
import time


T = TypeVar('T')


def elapsed_time(f: Callable) -> Callable[[], T]:
    def elapsed_func(*args, **kwargs):
        print("Start elapsed time:")
        t = time.process_time()
        f(*args, **kwargs)
        print("End elapsed time")
        print("---------------------")
    return elapsed_func
