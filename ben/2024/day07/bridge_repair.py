import aoc
from collections import deque


def parse_equation(line: str) -> tuple[int, tuple[int]]:
    test_value, operators = line.split(':')
    return int(test_value), tuple(map(int, operators.split()))

def try_equation(ops: list[str], test_value: int, numbers: tuple[int]) -> int:
    queue = deque([(test_value, numbers)])

    while queue:
        value, numbers = queue.pop()
        
        if len(numbers) == 0:
            if (value == 0):
                return test_value
            continue

        _next = numbers[-1]
        _remaining = numbers[:-1]

        if '+' in ops and value >= _next:
            queue.append((value - _next, _remaining))
        if '*' in ops and value % _next == 0:
            queue.append((value // _next, _remaining))
        if '||' in ops and str(value).endswith(str(_next)):
            new_val = 0 if value == _next else int(str(value)[:-len(str(_next))])
            queue.append((int(new_val), _remaining))
    return 0

@aoc.register(__file__)
def answers():
    equations = [parse_equation(x) for x in aoc.read_lines()]

    # Part One
    ops = ('+', '*')
    yield sum(try_equation(ops, *x) for x in equations)

    # Part Two
    ops += ('||',)
    yield sum(try_equation(ops, *x) for x in equations)

if __name__ == '__main__':
    aoc.run()
