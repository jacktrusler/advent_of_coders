import aoc


def run_commands_1(commands: list[str]) -> tuple[int, int]:
    horizontal, depth = 0, 0
    for cmd, val in commands:
        match cmd:
            case 'forward': horizontal += int(val)
            case 'up': depth -= int(val)
            case 'down': depth += int(val)
    return horizontal, depth

def run_commands_2(commands: list[str]) -> tuple[int, int]:
    horizontal, depth, aim = 0, 0, 0
    for cmd, val in commands:
        match cmd:
            case 'forward':
                horizontal += int(val)
                depth += aim * int(val)
            case 'up': aim -= int(val)
            case 'down': aim += int(val)
    return horizontal, depth


@aoc.register(__file__)
def answers():
    commands = [tuple(x.split()) for x in aoc.read_lines()]
    
    horizontal, depth = run_commands_1(commands)
    yield horizontal * depth

    horizontal, depth = run_commands_2(commands)
    yield horizontal * depth

if __name__ == '__main__':
    aoc.run()
