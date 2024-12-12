from __future__ import annotations
import aoc
from collections import defaultdict
import itertools
import re


@aoc.register(__file__)
def answers():
    schematic = aoc.read_data()
    schematic_grid = schematic.splitlines()
    line_length = len(schematic_grid[0]) + 1

    non_symbols = {str(n) for n in range(10)} | {"."}
    gear_values = defaultdict(list)
    part_total = 0
    
    for _match in re.finditer(r'(\d+)', schematic):
        y, x = divmod(_match.start(), line_length)
        val = _match.group()
        for adj_y, adj_x in itertools.product(range(y-1, y+2), range(x-1, x+len(val)+1)):
            try:
                adj_val = schematic_grid[adj_y][adj_x]
            except IndexError:
                continue

            if adj_val not in non_symbols:
                val = int(val)
                part_total += val
                if adj_val == '*':
                    gear_values[(adj_y, adj_x)].append(val)
    yield part_total
    yield sum(v[0] * v[1] for v in gear_values.values() if len(v) == 2)

if __name__ == '__main__':
    aoc.run()
