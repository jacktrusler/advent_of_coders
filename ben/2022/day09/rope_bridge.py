from __future__ import annotations
import aoc


class Knot:
    def __init__(self, parent: Knot = None):
        self.loc: complex = 0 + 0j
        self.visited = {self.loc}
        self.child: Knot = None
        if parent is not None:
            parent.child = self

    def move(self, value: complex) -> Knot:
        self.loc += value
        self.visited.add(self.loc)
        if self.child is not None:
            self.child.move_relative_to(self)
        return self

    def move_relative_to(self, other: Knot) -> Knot:
        diff = other.loc - self.loc
        if abs(diff.real) > 0 and abs(diff.imag) > 0 and abs(diff) > abs(1+1j):
            r, i = 1 if diff.real > 0 else -1, 1 if diff.imag > 0 else -1
            self.move(complex(r, i))
        elif abs(diff.real) > 1 or abs(diff.imag) > 1:
            m = diff / abs(diff)
            self.move(m)
        return self

class Rope:
    def __init__(self, knots: int):
        _knots, prev = [], None
        for _ in range(knots):
            new_knot = Knot(parent=prev)
            _knots.append(new_knot)
            prev = new_knot
        self.knots = _knots

    def __getitem__(self, i: int) -> Knot:
        return self.knots[i]

    def move(self, d: str, amt: str|int) -> Rope:
        d = direction(d)
        for _ in range(int(amt)):
            self.knots[0].move(d)
        return self

def direction(d: str) -> complex:
    match d:
        case 'U': return 1j
        case 'D': return -1j
        case 'R': return 1
        case 'L': return -1
            

@aoc.register(__file__)
def answers():
    movements = [tuple(line.split()) for line in aoc.read_lines()]

    rope = Rope(knots=2)
    for m in movements:
        rope.move(*m)
    yield len(rope[-1].visited)

    rope = Rope(knots=10)
    for m in movements:
        rope.move(*m)
    yield len(rope[-1].visited)

if __name__ == '__main__':
    aoc.run()
