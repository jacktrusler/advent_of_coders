import heapq

DIRECTIONS = {'n': (-1, 0), 'e': (0, 1), 's': (1, 0), 'w': (0, -1)}
DIR_SCORE = {
    'nn': 0, 'ne': 1000, 'nw': 1000, 'ns': 2000,
    'ee': 0, 'en': 1000, 'es': 1000, 'ew': 2000,
    'ww': 0, 'wn': 1000, 'ws': 1000, 'we': 2000,
    'ss': 0, 'sw': 1000, 'se': 1000, 'sn': 2000,
}

def solve(puzzle_input: str) -> tuple[int]:
    grid = dict()
    for i, row in enumerate(puzzle_input.splitlines()):
        for j, v in enumerate(row):
            if v == 'S':
                x, y = i, j
                grid[i, j] = '.'
            elif v == 'E':
                ex, ey = i, j
                grid[i, j] = '.'
            else:
                grid[i, j] = v
    unvisited = [(0, x, y, 'e', None)]
    heapq.heapify(unvisited)
    visited = dict()
    while unvisited:
        score, x, y, d, prev = heapq.heappop(unvisited)
        for d2, (dx, dy) in DIRECTIONS.items():
            x2 = x + dx
            y2 = y + dy
            v2 = grid[x2, y2]
            if v2 == '#':
                continue
            s2 = score + DIR_SCORE[d + d2] + 1
            try:
                prev_score = visited[x2, y2, d2]['score']
            except KeyError:
                pass
            else:
                if s2 > prev_score:
                    continue
            heapq.heappush(unvisited, (s2, x2, y2, d2, (x, y, d)))
        try:
            v = visited[x, y, d]
        except KeyError:
            visited[x, y, d] = {'score': score, 'prev': {prev}}
        else:
            if score < v['score']:
                v['score'] = score
                v['prev'] = {prev}
            elif score == v['score']:
                v['prev'].add(prev)
    score = min(v['score'] for (x, y, _), v in visited.items() if x == ex and y == ey)
    visited_tiles = {(ex, ey)}
    for (x, y, d), v in visited.items():
        if x == ex and y == ey and v['score'] == score:
            prevs = set(v['prev'])
            while prevs:
                try:
                    px, py, pd = prevs.pop()
                except TypeError:
                    continue
                visited_tiles.add((px, py))
                prevs = prevs | visited[px, py, pd]['prev']
    return score, len(visited_tiles)

if __name__ == '__main__':
    from pathlib import Path
    import aoc_util
    input_path = Path(__file__).parent / "input" / "16.txt"
    aoc_util.report(*aoc_util.run_solution(solve, input_path))
