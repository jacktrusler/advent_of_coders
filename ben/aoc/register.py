import functools
import re
import time


NUM_WORDS = {1: 'ONE', 2: 'TWO'}
REGISTERED = {}


def registered_functions():
    return REGISTERED

def register(filename):
    def _register(func):
        @functools.wraps(func)
        def wrapper():
            info = re.match(r'.*\\(?P<year>\d+)\\day(?P<day>\d+)\\(?P<filename>.*).py', filename).groupdict()
            print(f'********************************************')
            print(f'** {info["year"]}/day{info["day"]}: {info["filename"].replace("_", " ").title()}')

            start = time.process_time()
            result_gen = func()
            if result_gen is not None:
                yield from result_gen
            else:
                print('NO RESULTS')
            end = time.process_time()

            print(f'Time elapsed: {round((end - start) * 1000, 3)} ms')
        REGISTERED[wrapper] = filename
        return wrapper
    return _register