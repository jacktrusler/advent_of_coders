import aoc
import itertools


DIRECTION_MAP = {
    'U': aoc.Direction.UP,
    'R': aoc.Direction.RIGHT,
    'D': aoc.Direction.DOWN,
    'L': aoc.Direction.LEFT,
}
Wire = list[aoc.OrthogonalLine]

def parse_wire(data: str) -> Wire:
    point = aoc.Point(0, 0)
    retval = []

    def _parse_instruction(start: aoc.Point, instruction: str) -> aoc.OrthogonalLine:
        direction, distance = instruction[0], int(instruction[1:])
        return aoc.OrthogonalLine(start, start.move(DIRECTION_MAP[direction], distance))

    for i in data.split(','):
        line = _parse_instruction(point, i)
        retval.append(line)
        point = line.end
    return retval

def intersections(a: Wire, b: Wire):
    for x, y in itertools.product(a, b):
        if (p := x & y) is not None:
            yield p
        
def signal_delay(wires: list[Wire], p: aoc.Point) -> int:
    def _trace(wire: Wire) -> int:
        retval = 0
        for line in wire:
            if (p in line):
                return int(retval + line.start.distance(p))
            retval += len(line)
    return sum(_trace(x) for x in wires)

@aoc.register(__file__)
def answers():
    wires = [parse_wire(x) for x in aoc.read_lines()]

    # Part One
    crosses = [x for x in intersections(*wires) if x != aoc.Point(0, 0)]
    yield min(x.manhattan_distance() for x in crosses)
    yield min(signal_delay(wires, x) for x in crosses)

if __name__ == '__main__':
    aoc.run()
