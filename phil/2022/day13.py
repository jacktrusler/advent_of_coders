from time import perf_counter_ns
import json
import re
from itertools import zip_longest


def iterable(x):
    try:
        return (item for item in x)
    except TypeError:
        return (x for _ in range(1))


def compare(a, b) -> int:
    """Return a negative number if a < b, a positive number if a > b, or 0 if they are equal."""
    try:
        return a - b
    except TypeError:
        for a_item, b_item in zip_longest(iterable(a), iterable(b)):
            if a_item is None:
                return -1
            if b_item is None:
                return 1
            result = compare(a_item, b_item)
            if result != 0:
                return result
        return 0


def solve(raw_input: str) -> tuple:
    right_order = set()
    groups = [0] * 11
    for i, pair in enumerate(raw_input.split('\n\n'), 1):
        group_1, group_2 = pair.splitlines()
        list_1 = json.loads(group_1)
        list_2 = json.loads(group_2)
        for group in (group_1, group_2):
            try:
                first_digit = int(re.search(r"\d+|\[]", group).group(0))
            except ValueError:
                # first digit was a [], just add to the 0 count because it doesn't matter
                first_digit = 0
            groups[first_digit] += 1
        if compare(list_1, list_2) < 0:
            right_order.add(i)
    i2 = sum(groups[:2]) + 1  # index of the first item in the 2s group
    i6 = sum(groups[:6]) + 2  # index of the first item in the 6s group (+1 for the [[2]] divider)
    return sum(right_order), i2 * i6


def main():
    with open('./day13_input.txt', mode='r') as f:
        problem_input = f.read()
    start_time = perf_counter_ns()
    a, b = solve(problem_input)
    end_time = perf_counter_ns()
    elapsed_ms = round((end_time - start_time) / 1000000, 3)
    print(f'A: {a}')
    print(f'B: {b}')
    print(f'Elapsed time: {elapsed_ms} ms')


if __name__ == '__main__':
    main()
