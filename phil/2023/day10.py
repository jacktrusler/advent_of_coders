from pathlib import Path
import utils

DIRECTION_CHANGE = {
    'N': (-1, 0),
    'S': (1, 0),
    'E': (0, 1),
    'W': (0, -1)
}

NEXT_DIRECTION = {
    'N': {'|': 'N', '7': 'W', 'F': 'E'},
    'S': {'|': 'S', 'J': 'W', 'L': 'E'},
    'E': {'-': 'E', 'J': 'N', '7': 'S'},
    'W': {'-': 'W', 'L': 'N', 'F': 'S'},
}

BLOCK = {
    "N": ((0, 0), (0, 1)),
    "S": ((1, 0), (1, 1)),
    "E": ((0, 1), (1, 1)),
    "W": ((0, 0), (1, 0)),
}

def move(x: int, y: int, direction: str) -> tuple[int, int]:
    dx, dy = DIRECTION_CHANGE[direction]
    return x + dx, y + dy

def solve(raw_input: str):
    grid = raw_input.splitlines()
    xmax = len(grid)
    ymax = len(grid[0])
    x, y = divmod(raw_input.index("S"), raw_input.index("\n") + 1)

    # determine initial direction
    direction = None
    for d in DIRECTION_CHANGE:
        x2, y2 = move(x, y, d)
        if 0 <= x2 <= xmax and 0 <= y2 <= ymax:
            if grid[x2][y2] in NEXT_DIRECTION[d]:
                direction = d
    
    # follow path to solve A
    path_tiles = {(x, y)}
    blocked = set()
    while True:
        (x1, y1), (x2, y2) = BLOCK[direction]
        block_path = ((x + x1, y + y1), (x + x2, y + y2))
        blocked.update({block_path, block_path[::-1]}) 
        x, y = move(x, y, direction)
        path_tiles.add((x, y))
        char = grid[x][y]
        if char == 'S':
            break
        direction = NEXT_DIRECTION[direction][char]
    a = len(path_tiles) // 2
    
    # search grid vertices, b is however many grid tiles aren't seen if you don't
    # cross the path (the blocked moves)
    tiles_seen = set()
    searched = {(0, 0)}
    search = {(0, 0)}
    while search:
        x, y = search.pop()
        tiles_seen.update({(x-1, y-1), (x-1, y), (x, y-1), (x, y)})
        for x2, y2 in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            if (x2, y2) in searched:
                continue
            if ((x, y), (x2, y2)) in blocked:
                continue
            if 0 <= x2 <= xmax and 0 <= y2 <= ymax:
                searched.add((x2, y2))
                search.add((x2, y2))
    grid_set = {(x, y) for x in range(xmax) for y in range(ymax)}
    b = len(grid_set - tiles_seen)

    return a, b

if __name__ == '__main__':
    input_path = Path(__file__).parent / "input" / "10.txt"
    utils.report(*utils.run_solution(solve, input_path))
