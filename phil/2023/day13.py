from pathlib import Path
import utils

def differences(a_row: str, b_row: str, max_diff: int) -> int:
    diffs = 0
    for a, b in zip(a_row, b_row):
        if a != b:
            diffs += 1
            if diffs > max_diff:
                break
    return diffs

def find_reflection(lines: list, smudges: int) -> int:
    for i in range(1, len(lines)):
        smudges_left = smudges
        lines_before = iter(lines[:i][::-1])
        lines_after = iter(lines[i:])
        while smudges_left >= 0:
            try:
                smudges_left -= differences(next(lines_before), next(lines_after), smudges_left)
            except StopIteration:
                if smudges_left == 0:
                    return i
                break
    raise RuntimeError("No reflection found")

def summary(x: list, y: list, smudges: int) -> int:
    try:
        return 100 * find_reflection(x, smudges)
    except RuntimeError:
        return find_reflection(y, smudges)

def solve(raw_input: str) -> tuple[int, int]:
    a = 0
    b = 0
    for pattern in raw_input.split("\n\n"):
        lines = pattern.splitlines()
        x = list()
        y = [''] * len(lines[0])
        for line in lines:
            x.append(line)
            for i, char in enumerate(line):
                y[i] += char
        a += summary(x, y, 0)
        b += summary(x, y, 1)
    return a, b

if __name__ == '__main__':
    input_path = Path(__file__).parent / "input" / "13.txt"
    utils.report(*utils.run_solution(solve, input_path))
