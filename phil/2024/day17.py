import math

def run(a, b, c, program):
    def combo(x):
        if x <= 3:
            return x
        if x == 4:
            return a
        if x == 5:
            return b
        if x == 6:
            return c
    i = 0
    while True:
        try:
            o, v = program[i:i+2]
        except (IndexError, ValueError):
            break
        match o:
            case 0:
                a = int(a // math.pow(2, combo(v)))
            case 1:
                b = b ^ v
            case 2:
                b = combo(v) % 8
            case 3:
                if a != 0:
                    i = v
                    continue
            case 4:
                b = b ^ c
            case 5:
                yield combo(v) % 8
            case 6:
                b = int(a // math.pow(2, combo(v)))
            case 7:
                c = int(a // math.pow(2, combo(v)))
        i += 2

def solve_b(desired_output, a, program):
    try:
        o = desired_output[0]
    except IndexError:
        return a
    # in my input program, a is floor divided by 8 every cycle. So the next a has
    # to be within this range to produce a correct value of a.
    for n in range(a*8, (a*8)+8):
        if o == next(run(n, 0, 0, program)):
            if result := solve_b(desired_output[1:], n, program):
                return result
    return None

def solve(puzzle_input: str) -> tuple[int]:
    register_text, program_text = puzzle_input.split('\n\n')
    a, b, c = [int(register[11:]) for register in register_text.splitlines()]
    program = [int(x) for x in program_text[9:].split(',')]
    answer_a = ','.join(map(str, run(a, b, c, program)))
    answer_b = solve_b(list(reversed(program)), 0, program)
    return answer_a, answer_b

if __name__ == '__main__':
    from pathlib import Path
    import aoc_util
    input_path = Path(__file__).parent / "input" / "17.txt"
    aoc_util.report(*aoc_util.run_solution(solve, input_path))
