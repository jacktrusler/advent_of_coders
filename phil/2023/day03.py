from pathlib import Path
import utils
import re
import itertools
import collections

@utils.solver(Path(__file__).parent / "input" / "03.txt")
def solve(raw_input: str):
    line_length = raw_input.index('\n') + 1
    grid = raw_input.splitlines()
    non_symbols = {str(n) for n in range(10)} | {"."}
    symbol_scores = collections.defaultdict(list)
    a = 0
    b = 0
    for m in re.finditer(r'\d+', raw_input):
        x, y = divmod(m.start(), line_length)
        n = int(m.group())
        xmin, xmax, ymin, ymax = x-1, x+1, y-1, y+len(m.group())
        for x2, y2 in itertools.product(range(xmin, xmax+1), range(ymin, ymax+1)):
            try:
                char = grid[x2][y2]
            except IndexError:
                continue
            if char not in non_symbols:
                a += n
                if char == "*":
                    symbol_scores[(x2, y2)].append(n)
    for items in symbol_scores.values():
        if len(items) == 2:
            b += items[0] * items[1]
    return a, b

if __name__ == '__main__':
    utils.report(*solve())
