import functools
import re
import time
import timeit


NUM_WORDS = {1: 'ONE', 2: 'TWO'}
REGISTERED = {}


def registered_functions():
    return REGISTERED

def register(filename):
    def _register(func):
        @functools.wraps(func)
        def wrapper():
            result_gen = func()
            if result_gen is not None:
                yield from result_gen
            else:
                print('NO RESULTS')
        REGISTERED[wrapper] = filename
        return wrapper
    return _register