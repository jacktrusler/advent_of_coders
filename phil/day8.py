from time import perf_counter_ns
from itertools import product


def problem_a(raw_input: str) -> int:
    arr = [[int(x) for x in row] for row in raw_input.splitlines()]
    num_rows = len(arr)
    num_cols = len(arr[0])
    visible = set()
    for i in range(num_rows):
        row = arr[i]
        x = -1
        for j in range(num_cols):
            height = row[j]
            if height > x:
                visible.add((i, j))
                x = height
            if height == 9:
                break
        x = -1
        for j in reversed(range(num_cols)):
            height = row[j]
            if height > x:
                visible.add((i, j))
                x = height
            if height == 9:
                break
    for j in range(num_cols):
        x = -1
        for i in range(num_rows):
            height = arr[i][j]
            if height > x:
                visible.add((i, j))
                x = height
            if height == 9:
                break
        x = -1
        for i in reversed(range(num_rows)):
            height = arr[i][j]
            if height > x:
                visible.add((i, j))
                x = height
            if height == 9:
                break
    return len(visible)


def score(a, n, points):
    i = 0
    for x, y in points:
        if a[x][y] >= n:
            return i+1
        i += 1
    else:
        return i


def problem_b(raw_input: str) -> int:
    arr = [[int(x) for x in row] for row in raw_input.splitlines()]
    best_score = 0
    x_size = len(arr)
    y_size = len(arr[0])
    for x, y in product(range(1, x_size - 1), range(1, y_size - 1)):
        height = arr[x][y]
        score_east = score(arr, height, ((x, i) for i in range(y+1, y_size)))
        score_west = score(arr, height, ((x, i) for i in range(y-1, -1, -1)))
        score_north = score(arr, height, ((i, y) for i in range(x-1, -1, -1)))
        score_south = score(arr, height, ((i, y) for i in range(x+1, x_size)))
        best_score = max(best_score, score_east * score_west * score_north * score_south)
    return best_score


if __name__ == '__main__':
    with open('./day8_input.txt', mode='r') as f:
        problem_input = f.read()
    for f in (problem_a, problem_b):
        start_time = perf_counter_ns()
        result = f(problem_input)
        end_time = perf_counter_ns()
        elapsed_ms = round((end_time - start_time) / 1000000, 3)
        print(f'{f.__name__}: {result}, elapsed time: {elapsed_ms} ms')
