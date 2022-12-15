from time import perf_counter_ns


def get_rocks(raw_input: str) -> set:
    rocks = set()
    for line in raw_input.splitlines():
        point = line.split(' -> ')
        x1, y1 = (int(n) for n in point[0].split(','))
        for pair_str in point[1:]:
            x2, y2 = (int(n) for n in pair_str.split(','))
            if x1 != x2:
                rocks.update({(x, y1) for x in (range(x1, x2 + 1) if x2 > x1 else range(x2, x1 + 1))})
            else:
                rocks.update({(x1, y) for y in (range(y1, y2 + 1) if y2 > y1 else range(y2, y1 + 1))})
            x1, y1 = x2, y2
    return rocks


def solve_a(rocks: set, rock_max: int) -> int:
    settled = 0
    filled = set(rocks)
    while True:
        x = 500
        for y in range(1, rock_max):
            if (x, y + 1) not in filled:
                continue
            elif (x - 1, y + 1) not in filled:
                x -= 1
            elif (x + 1, y + 1) not in filled:
                x += 1
            else:
                filled.add((x, y))
                break
        else:
            return settled
        settled += 1


def solve_b(rocks: set, rock_max: int) -> int:
    s = {500}
    total = 1
    for y in range(1, rock_max + 2):
        s = {x for x in range(500 - y, 500 + y + 1) if (x - 1 in s or x in s or x + 1 in s) and (x, y) not in rocks}
        total += len(s)
    return total


def solve(raw_input: str) -> tuple:
    rocks = get_rocks(raw_input)
    rock_max = max((r[1] for r in rocks))
    a = solve_a(rocks, rock_max)
    b = solve_b(rocks, rock_max)
    return a, b


def main():
    with open('./day14_input.txt', mode='r') as f:
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
