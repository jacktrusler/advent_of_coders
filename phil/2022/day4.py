from datetime import datetime


def range_to_set(s: str) -> set:
    ints = [int(x) for x in s.split('-')]
    return set(range(ints[0], ints[1] + 1))


def problem_a(i: str) -> int:
    count = 0
    for pair in i.splitlines():
        a, b = [range_to_set(s) for s in pair.split(',')]
        if a.issubset(b) or b.issubset(a):
            count += 1
    return count


def problem_b(i: str) -> int:
    count = 0
    for pair in i.splitlines():
        a, b = [range_to_set(s) for s in pair.split(',')]
        if len(a & b) > 0:
            count += 1
    return count


if __name__ == '__main__':
    with open('./day4_input.txt', mode='r') as f:
        problem_input = f.read()
    start_a = datetime.now()
    result_a = problem_a(problem_input)
    end_a = datetime.now()
    print(f'A: {result_a}, time: {(end_a - start_a).total_seconds()} seconds')
    start_b = datetime.now()
    result_b = problem_b(problem_input)
    end_b = datetime.now()
    print(f'B: {result_b}, time: {(end_b - start_b).total_seconds()} seconds')
