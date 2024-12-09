import aoc
from collections import deque
import operator


def parse_equation(line: str) -> tuple[int, tuple[int]]:
    test_value, operators = line.split(':')
    return int(test_value), tuple(map(int, operators.split()))

def concentration(x: int, y: int) -> int:
    return int(f'{x}{y}')

def try_equation(ops, test_value, operators) -> int:
    state = (0, 0, operators[0], ops[0])
    queue = deque([state])
    values = set()

    while queue:
        value, idx, op_value, op = queue.pop()

        value = op(value, op_value)
        if value > test_value:
            continue

        next_idx = idx + 1
        try:
            next_operator = operators[next_idx]
        except IndexError:
            values.add(value)
            continue

        for _op in ops:
            queue.append((value, next_idx, next_operator, _op))

    return test_value if test_value in values else 0


@aoc.register(__file__)
def answers():
    equations = [parse_equation(x) for x in aoc.read_lines()]

    # Part One
    ops = (operator.add, operator.mul)
    yield sum(try_equation(ops, *x) for x in equations)

    # Part Two
    ops += (concentration, )
    yield sum(try_equation(ops, *x) for x in equations)

if __name__ == '__main__':
    aoc.run()
