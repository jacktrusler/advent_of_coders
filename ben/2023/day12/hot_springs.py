from __future__ import annotations
import aoc
from dataclasses import dataclass, field, replace
import functools


@dataclass(frozen=True)
class Record:
    data: str
    groups: tuple[int] = field(default_factory=tuple)

    @staticmethod
    def from_string(line: str) -> Record:
        data, groups = line.split()
        return Record(data, tuple(map(int, groups.split(','))))

    def unfold(self, n: int) -> Record:
        return replace(self, data='?'.join([self.data]*n), groups=self.groups*n)
    
    def combinations(self) -> int:
        @functools.cache
        def _combos(r: str, g: tuple[int]) -> int:
            if len(g) == 0:
                return 1 if '#' not in r else 0
            if r == '' or (len(r) < (sum(g) + len(g) - 1)):
                return 0

            match r[0]:
                case '.':
                    return _combos(r[1:], g)
                case '?':
                    return _combos(f'.{r[1:]}', g) + _combos(f'#{r[1:]}', g)
                case '#':
                    try:
                        p, x, r = r[:g[0]], r[g[0]], r[g[0]+1:]
                    except IndexError:
                        p, x, r = r[:g[0]], '', ''
                    if '.' in p or x == '#':
                        return 0
                    return _combos(r, g[1:])
        return _combos(self.data, self.groups)


@aoc.register(__file__)
def answers():
    records = [Record.from_string(x) for x in aoc.read_lines()]
    yield sum(x.combinations() for x in records)
    yield sum(x.unfold(5).combinations() for x in records)

if __name__ == '__main__':
    aoc.run()
