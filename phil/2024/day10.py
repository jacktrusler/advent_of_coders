from collections import defaultdict

def climb(heights: dict, path: tuple):
    x, y = path[-1]
    height = heights[x][y]
    if height == 9:
        return {path}
    peak_paths = set()
    for x2, y2 in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
        try:
            height2 = heights[x2][y2]
        except KeyError:
            continue
        if height2 - height == 1:
            peak_paths = peak_paths | climb(heights, path + ((x2, y2),))
    return peak_paths

def solve(puzzle_input: str):
    size = puzzle_input.index('\n')
    heights = defaultdict(dict)
    trailheads = set()
    a = 0
    b = 0
    for i, height in enumerate(puzzle_input):
        if height != '\n':
            x = i // (size + 1)
            y = i % (size + 1)
            heights[x][y] = int(height)
            if height == '0':
                trailheads.add((x, y))
    for x, y in trailheads:
        paths = climb(heights, ((x, y),))
        a += len({path[-1] for path in paths})
        b += len(paths)
    return a, b

if __name__ == '__main__':
    from pathlib import Path
    import aoc_util
    input_path = Path(__file__).parent / "input" / "10.txt"
    aoc_util.report(*aoc_util.run_solution(solve, input_path))
