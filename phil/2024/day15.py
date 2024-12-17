DIRECTIONS = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}

def move(grid: dict, x: int, y: int, direction: str) -> bool:
    dx, dy = DIRECTIONS[direction]
    move_tiles = set(((x, y),))
    moved_tiles = set()
    while move_tiles:
        x, y = move_tiles.pop()
        if (x, y) in moved_tiles:
            continue
        x2 = x + dx
        y2 = y + dy    
        if (x2, y2) in grid:
            v2 = grid[x2, y2]
            if v2 == 'O':
                move_tiles.add((x2, y2))
            elif v2 == '[':
                move_tiles.add((x2, y2))
                move_tiles.add((x2, y2+1))
            elif v2 == ']':
                move_tiles.add((x2, y2))
                move_tiles.add((x2, y2-1))
            elif v2 == '#':
                return False
        moved_tiles.add((x, y))
    new_tiles = dict()
    for x, y in moved_tiles:
        new_tiles[x + dx, y + dy] = grid[x, y]
        del grid[x, y]
    grid.update(new_tiles)
    return True

def solve(puzzle_input: str) -> tuple[int]:
    grid_text, moves = puzzle_input.split("\n\n")

    grid_a = dict()
    grid_b = dict()
    for i, row in enumerate(grid_text.split()):
        for j, v in enumerate(row):
            match v:
                case 'O':
                    grid_a[i, j] = v
                    grid_b[i, j*2] = '['
                    grid_b[i, j*2+1] = ']'
                case '#':
                    grid_a[i, j] = v
                    grid_b[i, j*2] = v
                    grid_b[i, j*2+1] = v
                case '@':
                    grid_a[i, j] = v
                    grid_b[i, j*2] = v
                    ax, ay = i, j
                    bx, by = i, j*2

    for d in ''.join(moves.split()):
        if move(grid_a, ax, ay, d):
            dx, dy = DIRECTIONS[d]
            ax += dx
            ay += dy
        if move(grid_b, bx, by, d):
            dx, dy = DIRECTIONS[d]
            bx += dx
            by += dy

    gps_a = sum([(100 * x) + y for (x, y), v in grid_a.items() if v == 'O'])
    gps_b = sum([(100 * x) + y for (x, y), v in grid_b.items() if v == '['])
    return gps_a, gps_b

if __name__ == '__main__':
    from pathlib import Path
    import aoc_util
    input_path = Path(__file__).parent / "input" / "15.txt"
    aoc_util.report(*aoc_util.run_solution(solve, input_path))
