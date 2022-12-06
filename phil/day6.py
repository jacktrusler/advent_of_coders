from datetime import datetime
from collections import Counter


def problem(raw_input: str, window: int) -> int:
    for i in range(len(raw_input))[window:]:
        sequence = raw_input[i-window:i]
        if len(set(sequence)) == len(sequence):
            return i
    raise ValueError('sequence not detected')


def problem_alternate(raw_input: str, window: int) -> int:
    c = Counter(raw_input[:window])
    for i in range(len(raw_input))[window:]:
        if len(c) == window:
            return i
        c[raw_input[i]] += 1
        removed = raw_input[i-window]
        if c[removed] == 1:
            del c[removed]
        else:
            c[removed] -= 1
    raise ValueError('sequence not detected')


def problem_a(raw_input: str) -> int:
    return problem(raw_input.strip(), 4)


def problem_b(raw_input: str) -> int:
    return problem(raw_input.strip(), 14)


if __name__ == '__main__':
    with open('./day6_input.txt', mode='r') as f:
        problem_input = f.read()
    start_a = datetime.now()
    result_a = problem_a(problem_input)
    end_a = datetime.now()
    print(f'A: {result_a}, time: {(end_a - start_a).total_seconds()} seconds')
    start_b = datetime.now()
    result_b = problem_b(problem_input)
    end_b = datetime.now()
    print(f'B: {result_b}, time: {(end_b - start_b).total_seconds()} seconds')
