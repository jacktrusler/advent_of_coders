def row_moves(row, size, obstacles):
        moves = dict()
        last_obstacle = row, 0, None
        for col in range(size):
            if (row, col) in obstacles:
                last_obstacle = row, col + 1, 'up'
            else:
                moves[row, col, 'left'] = last_obstacle
        last_obstacle = row, size-1, None
        for col in range(size-1, -1, -1):
            if (row, col) in obstacles:
                last_obstacle = row, col - 1, 'down'
            else:
                moves[row, col, 'right'] = last_obstacle
        return moves

def col_moves(col, size, obstacles):
    moves = dict()
    last_obstacle = 0, col, None
    for row in range(size):
        if (row, col) in obstacles:
            last_obstacle = row + 1, col, 'right'
        else:
            moves[row, col, 'up'] = last_obstacle
    last_obstacle = size - 1, col, None
    for row in range(size-1, -1, -1):
        if (row, col) in obstacles:
            last_obstacle = row - 1, col, 'left'
        else:
            moves[row, col, 'down'] = last_obstacle
    return moves

def move(x, y, direction):
    match direction:
        case 'up':
            return x - 1, y
        case 'down':
            return x + 1, y
        case 'left':
            return x, y - 1
        case 'right':
            return x, y + 1

def solve(puzzle_input: str):
    size = puzzle_input.index('\n')
    obstacles = set()
    for i in range(len(puzzle_input)):
        if puzzle_input[i] == '#':
            obstacles.add((i // (size + 1), i % (size + 1)))
    moves = dict()
    for row in range(size):
        moves.update(row_moves(row, size, obstacles))
    for col in range(size):
        moves.update(col_moves(col, size, obstacles))
    position = puzzle_input.index('^')
    row, col = position // (size + 1), position % (size + 1)
    r, c, d = row, col, 'up'
    positions = list(((r, c, d),))
    while d is not None:
        positions.append((r, c, d))
        r1, c1, d1 = moves[r, c, d]
        while (r, c) != (r1, c1):
            r, c = move(r, c, d)
            positions.append((r, c, d))
        d = d1
    b = 0
    r, c, d = positions[0]
    visited = set(((r, c),))
    visited_with_direction = {(r, c, d)}
    for (orow, ocol, od) in positions[1:]:
        if (orow, ocol) in visited:
            continue
        visited.add((orow, ocol))
        b_obstacles = obstacles | {(orow, ocol)}
        rmoves = row_moves(orow, size, b_obstacles)
        cmoves = col_moves(ocol, size, b_obstacles)
        visited_with_direction_inner = visited_with_direction.copy()
        while d is not None:
            for move_dict in (rmoves, cmoves, moves):
                try:
                    r, c, d = move_dict[r, c, d]
                except KeyError:
                    continue
            if (r, c, d) in visited_with_direction_inner:
                b += 1
                break
            visited_with_direction_inner.add((r, c, d))
        r, c, d = orow, ocol, od
        visited_with_direction.add((r, c, d))
    return len(visited), b

if __name__ == '__main__':
    from pathlib import Path
    import aoc_util
    input_path = Path(__file__).parent / "input" / "06.txt"
    aoc_util.report(*aoc_util.run_solution(solve, input_path))
