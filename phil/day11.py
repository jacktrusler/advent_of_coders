from time import perf_counter_ns
from collections import deque
from functools import partial
from dataclasses import dataclass
from typing import Callable


class Worry:
    def _add(self, x: int):
        raise NotImplementedError

    def _multiply(self, x: int):
        raise NotImplementedError

    def _square(self):
        raise NotImplementedError

    def divisible(self, by: int):
        raise NotImplementedError

    @staticmethod
    def add(a: 'Worry', b: int):
        a._add(b)

    @staticmethod
    def multiply(a: 'Worry', b: int):
        a._multiply(b)

    @staticmethod
    def square(a: 'Worry'):
        a._square()


class WorryA(Worry):
    def __init__(self, starting):
        self.value = starting

    def _add(self, x: int):
        self.value = (self.value + x) // 3

    def _multiply(self, x: int):
        self.value = (self.value * x) // 3

    def _square(self):
        self.value = self.value**2 // 3

    def divisible(self, by: int):
        return self.value % by == 0


class WorryB(Worry):
    def __init__(self, starting, thresholds):
        self.values = {t: 0 for t in thresholds}
        self._add(starting)

    def _add(self, x: int):
        for k, v in self.values.items():
            self.values[k] = (v + x) % k

    def _multiply(self, x: int):
        for k, v in self.values.items():
            self.values[k] = (v * x) % k

    def _square(self):
        for k, v in self.values.items():
            self.values[k] = (v * v) % k

    def divisible(self, by: int):
        return self.values[by] == 0


@dataclass
class Monkey:
    items: deque
    inspect: Callable
    n: int
    target_a: int
    target_b: int

    def __post_init__(self):
        self.inspected = 0


def run(monkeys, number):
    for _ in range(number):
        for monkey in monkeys:
            while True:
                try:
                    item = monkey.items.popleft()
                except IndexError:
                    break
                monkey.inspect(item)
                monkey.inspected += 1
                target = monkey.target_a if item.divisible(monkey.n) else monkey.target_b
                monkeys[target].items.append(item)


def parse_monkey(s: str) -> tuple:
    lines = s.splitlines()
    worries = [int(x) for x in lines[1][18:].split(', ')]
    func_char = lines[2][23]
    func_val = lines[2][25:]
    try:
        b = int(func_val)
    except ValueError:
        func = Worry.square
    else:
        func = partial(Worry.add, b=b) if func_char == '+' else partial(Worry.multiply, b=b)
    test_val = int(lines[3][21:])
    true_target = int(lines[4][29:])
    false_target = int(lines[5][30:])
    return worries, func, test_val, true_target, false_target


def solve_a(monkey_inputs: list) -> int:
    monkeys = [Monkey(deque(WorryA(item) for item in m[0]), m[1], m[2], m[3], m[4]) for m in monkey_inputs]
    run(monkeys, 20)
    inspected = sorted([monkey.inspected for monkey in monkeys])
    return inspected[-1] * inspected[-2]


def solve_b(monkey_inputs: list) -> int:
    checks = [x[2] for x in monkey_inputs]
    monkeys = [Monkey(deque(WorryB(item, checks) for item in m[0]), m[1], m[2], m[3], m[4]) for m in monkey_inputs]
    run(monkeys, 10000)
    inspected = sorted([monkey.inspected for monkey in monkeys])
    return inspected[-1] * inspected[-2]


def solve(raw_input: str) -> tuple:
    monkey_inputs = [parse_monkey(monkey_input) for monkey_input in raw_input.split('\n\n')]
    return solve_a(monkey_inputs), solve_b(monkey_inputs)


def main():
    with open('./day11_input.txt', mode='r') as f:
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
