from time import perf_counter_ns


DIRECTIONS = {'R': (0, 1), 'L': (0, -1), 'U': (1, 1), 'D': (1, -1)}


def follow(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    if abs(dx) <= 1 and abs(dy) <= 1:
        raise ValueError
    if dx != 0:
        x2 += (1 if dx > 0 else -1)
    if dy != 0:
        y2 += (1 if dy > 0 else -1)
    return x2, y2


def move(knots, direction):
    d = DIRECTIONS[direction]
    knots[0][d[0]] += d[1]
    for i in range(1, len(knots)):
        try:
            knots[i][0], knots[i][1] = follow(knots[i - 1][0], knots[i - 1][1], knots[i][0], knots[i][1])
        except ValueError:
            return


def problem(raw_input: str, length=10) -> int:
    knots = [[0, 0] for _ in range(length)]
    visited = {(knots[-1][0], knots[-1][1])}
    for line in raw_input.splitlines():
        direction, n = line.split()
        for _ in range(int(n)):
            move(knots, direction)
            visited.add((knots[-1][0], knots[-1][1]))
    return len(visited)


def problem_a(raw_input: str) -> int:
    return problem(raw_input, length=2)


def problem_b(raw_input: str) -> int:
    return problem(raw_input, length=10)


if __name__ == '__main__':
    with open('./day9_input.txt', mode='r') as f:
        problem_input = f.read()
    for f in (problem_a, problem_b):
        start_time = perf_counter_ns()
        result = f(problem_input)
        end_time = perf_counter_ns()
        elapsed_ms = round((end_time - start_time) / 1000000, 3)
        print(f'{f.__name__}: {result}, elapsed time: {elapsed_ms} ms')
