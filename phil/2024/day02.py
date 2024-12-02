def solve(puzzle_input: str):
    a = 0
    b = 0
    for line in puzzle_input.splitlines():
        report = [int(x) for x in line.split()]
        if safe(report):
            a += 1
            b += 1
        else:
            for i in range(len(report)):
                if safe(report[:i] + report[i+1:]):
                    b += 1
                    break
    return a, b

def safe(report: list) -> bool:
    diffs = {report[i+1] - report[i] for i in range(len(report) - 1)}
    if diffs <= {1, 2, 3} or diffs <= {-1, -2, -3}:
        return True
    return False

if __name__ == '__main__':
    from pathlib import Path
    import aoc_util
    input_path = Path(__file__).parent / "input" / "02.txt"
    aoc_util.report(*aoc_util.run_solution(solve, input_path))
