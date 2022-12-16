import aoc


class VoidException(Exception):
    pass

Point = tuple[int, int]

def rock_points(line: str) -> set[Point]:
    pts = [tuple(map(int, pt.split(','))) for pt in line.split(' -> ')]

    retval = set()
    for ptA, ptB in zip(pts[:-1], pts[1:]):
        if ptA[0] == ptB[0]:
            step = 1 if ptB[1] > ptA[1] else -1
            retval |= {(ptA[0], y) for y in range(ptA[1], ptB[1] + step, step)}
        if ptA[1] == ptB[1]:
            step = 1 if ptB[0] > ptA[0] else -1
            retval |= {(x, ptA[1]) for x in range(ptA[0], ptB[0] + step, step)}
    return retval

def drop_sand(obstructions: set[Point], max_y: int, start: Point, floor: bool = False) -> Point:
    def _free_fall(p: Point) -> Point:
        while True:
            drop = (p[0], p[1]+1)
            if drop in obstructions:
                return p
            if drop[1] == max_y and floor:
                return p
            if drop[1] > max_y:
                raise VoidException
            p = drop
    
    sand = start
    while True:
        sand = _free_fall(sand)
        lower_left, lower_right = (sand[0]-1, sand[1]+1), (sand[0]+1, sand[1]+1)
        if floor and sand[1] + 1 == max_y:
            return sand
        if lower_left not in obstructions:
            sand = lower_left
            continue
        if lower_right not in obstructions:
            sand = lower_right
            continue
        return sand
    


@aoc.register(__file__)
def answers():
    rocks = set.union(*[rock_points(line) for line in aoc.read_lines()])
    max_y = max(p[1] for p in rocks)

    obstructions = rocks.copy()
    while True:
        try:
            obstructions.add(drop_sand(obstructions, max_y, start=(500, 0)))
        except VoidException:
            break
    yield len(obstructions) - len(rocks)


    floor = max_y + 2
    obstructions = rocks.copy()
    while True:
        new_sand = drop_sand(obstructions, floor, start=(500, 0), floor=True)
        obstructions.add(new_sand)

        if new_sand == (500, 0):
            break
    yield len(obstructions) - len(rocks)    

if __name__ == '__main__':
    aoc.run()
