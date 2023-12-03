from time import perf_counter_ns


def neighbors(x, y, z):
    for n in (-1, 1):
        yield x+n, y, z
        yield x, y+n, z
        yield x, y, z+n


def solve_a(droplets: set):
    droplets = set(droplets)
    num_droplets = len(droplets)
    visited = set()
    count = 0
    while droplets:
        search = {droplets.pop()}
        while search:
            x, y, z = search.pop()
            visited.add((x, y, z))
            for n in neighbors(x, y, z):
                if n in droplets and n not in visited:
                    count += 1
                    search.add(n)
    return (num_droplets * 6) - (count * 2)


def solve_b(droplets: set):
    x_values, y_values, z_values = [n for n in zip(*droplets)]
    x_min, x_max = min(x_values) - 1, max(x_values) + 1
    y_min, y_max = min(y_values) - 1, max(y_values) + 1
    z_min, z_max = min(z_values) - 1, max(z_values) + 1
    visited = set()
    surface_area = 0
    search = {(x_min, y_min, z_min)}
    while search:
        x, y, z = search.pop()
        visited.add((x, y, z))
        for x2, y2, z2 in neighbors(x, y, z):
            if x_min <= x2 <= x_max and y_min <= y2 <= y_max and z_min <= z2 <= z_max and (x2, y2, z2) not in visited:
                if (x2, y2, z2) in droplets:
                    surface_area += 1
                else:
                    search.add((x2, y2, z2))
    return surface_area


def solve(raw_input: str):
    droplets = {tuple(int(x) for x in line.split(',')) for line in raw_input.splitlines()}
    a = solve_a(droplets)
    b = solve_b(droplets)
    return a, b


def main():
    with open('./day18_input.txt', mode='r') as f:
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
