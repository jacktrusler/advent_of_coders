from time import perf_counter_ns


def generate_grid(raw_input: str) -> tuple:
    grid = list()
    start_a = set()
    start_b = set()
    goal = None
    for i, row in enumerate(raw_input.splitlines()):
        heights = list()
        for j, letter in enumerate(row):
            if letter == 'S':
                start_a.add((i, j))
                start_b.add((i, j))
                heights.append(0)
            elif letter == 'a':
                start_b.add((i, j))
                heights.append(0)
            elif letter == 'E':
                goal = (i, j)
                heights.append(ord('z') - ord('a'))
            else:
                heights.append(ord(letter) - ord('a'))
        grid.append(heights)
    return grid, start_a, start_b, goal


def path_length(grid, visit_next, goal) -> int:
    visited = set()
    step = 0
    while True:
        visit_now = visit_next - visited
        visit_next = set()
        while visit_now:
            x, y = visit_now.pop()
            if (x, y) == goal:
                return step
            v = grid[x][y]
            for a, b in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                x2, y2 = x + a, y + b
                if (x2, y2) in visited:
                    continue
                try:
                    v2 = grid[x2][y2]
                except IndexError:
                    continue
                if v + 1 >= v2:
                    visit_next.add((x2, y2))
            visited.add((x, y))
        step += 1


def solve(raw_input: str):
    grid, a_start, b_start, goal = generate_grid(raw_input)
    return path_length(grid, a_start, goal), path_length(grid, b_start, goal)


def main():
    with open('./day12_input.txt', mode='r') as f:
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
