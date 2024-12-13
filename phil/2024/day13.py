def tokens(ax, ay, bx, by, px, py) -> int:
    b = (py - (ay * px / ax)) / (by - (ay * bx / ax))
    a = (px - (bx * b)) / ax
    for result in (a, b):
        if abs(result - round(result)) > 0.01:
            return 0
    return (3 * round(a)) + round(b)

def solve(puzzle_input: str) -> tuple[int]:
    a = 0
    b = 0
    b_prize_edit = 10000000000000
    for group in puzzle_input.split('\n\n'):
        a_text, b_text, prize_text = group.splitlines()
        ax, ay = (int(x.split('+')[1]) for x in a_text.split(','))
        bx, by = (int(x.split('+')[1]) for x in b_text.split(','))
        px, py = (int(x.split('=')[1]) for x in prize_text.split(','))
        a += tokens(ax, ay, bx, by, px, py)
        b += tokens(ax, ay, bx, by, px + b_prize_edit, py + b_prize_edit)
    return a, b

if __name__ == '__main__':
    from pathlib import Path
    import aoc_util
    input_path = Path(__file__).parent / "input" / "13.txt"
    aoc_util.report(*aoc_util.run_solution(solve, input_path))
