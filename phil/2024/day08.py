from collections import defaultdict
from itertools import permutations

def solve(puzzle_input: str):
    size = puzzle_input.index('\n')
    freq = defaultdict(list)
    antinodes_a = set()
    antinodes_b = set()
    for i, v in enumerate(puzzle_input):
        if v not in {'\n', '.'}:
            freq[v].append((i // (size + 1), i % (size + 1)))
    for nodes in freq.values():
        for (x1, y1), (x2, y2) in permutations(nodes, 2):
            antinodes_b.add((x1, y1))
            antinodes_b.add((x2, y2))
            xd = x2 - x1
            yd = y2 - y1
            x3 = x2 + xd
            y3 = y2 + yd
            if 0 <= x3 < size and 0 <= y3 < size:
                antinodes_a.add((x3, y3))
                while 0 <= x3 < size and 0 <= y3 < size:
                    antinodes_b.add((x3, y3))
                    x3 += xd
                    y3 += yd
    return len(antinodes_a), len(antinodes_b)

if __name__ == '__main__':
    from pathlib import Path
    import aoc_util
    input_path = Path(__file__).parent / "input" / "08.txt"
    aoc_util.report(*aoc_util.run_solution(solve, input_path))
