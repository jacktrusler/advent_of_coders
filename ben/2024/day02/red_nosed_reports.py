import aoc
from itertools import pairwise


def check_report(report: list[int], tolerate: bool = False) -> bool:
    def _safe(r) -> bool:
        diffs = [y - x for (x, y) in pairwise(r)]
        min_diff, max_diff = min(diffs), max(diffs)
        return (max_diff <= 3 and min_diff >= 1) or (max_diff <= -1 and min_diff >= -3)
    
    if tolerate:
        return any(_safe(report[:i] + report[i+1:]) for i in range(len(report)))
    return _safe(report)

@aoc.register(__file__)
def answers():
    reports = [list(map(int, x.split())) for x in aoc.read_lines()]
    yield sum(check_report(x) for x in reports)
    yield sum(check_report(x, tolerate=True) for x in reports)

if __name__ == '__main__':
    aoc.run()
