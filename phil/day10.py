from time import perf_counter_ns


def solve(raw_input: str) -> tuple:
    x = 1
    cycle = 0
    pixels = ''
    signal_strength = [0]
    for line in raw_input.splitlines():
        if line.startswith('addx'):
            cycle += 1
            add_x = int(line[5:])
            pixels += '#' if lit(cycle, x) else '.'
            signal_strength.append(x * cycle)
            cycle += 1
            pixels += '#' if lit(cycle, x) else '.'
            signal_strength.append(x * cycle)
            x += add_x
        else:
            cycle += 1
            pixels += '#' if lit(cycle, x) else '.'
            signal_strength.append(x * cycle)
    signal_sum = sum([x for i, x in enumerate(signal_strength) if i in [20, 60, 100, 140, 180, 220]])
    return signal_sum, screen(pixels, line_size=40)


def screen(pixels: str, line_size: int) -> str:
    return ''.join([pixels[i:i + line_size] + '\n' for i in range(0, len(pixels), line_size)])


def lit(cycle: int, x: int) -> bool:
    return True if (cycle - 1) % 40 in sprite(x) else False


def sprite(pos: int) -> range:
    return range(max(0, pos - 1), min(39, pos + 1) + 1)


if __name__ == '__main__':
    with open('./day10_input.txt', mode='r') as f:
        problem_input = f.read()
    start_time = perf_counter_ns()
    a, b = solve(problem_input)
    end_time = perf_counter_ns()
    elapsed_ms = round((end_time - start_time) / 1000000, 3)
    print(f'A: {a}')
    print(f'B:\n{b}')
    print(f'Elapsed time: {elapsed_ms} ms')
