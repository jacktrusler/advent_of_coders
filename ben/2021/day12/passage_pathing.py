from __future__ import annotations
import aoc
from collections import deque, defaultdict


def num_paths2(caves: dict, start: str, end: str, revisits: bool = False) -> int:
    path_stack = deque([(start, {start}, not revisits)])
    count = 0

    while path_stack:
        cave, visited, revisited = path_stack.pop()

        if cave == end:
            count += 1
            continue
        
        for link in caves[cave]:
            if link == start:
                continue

            if link not in visited or link.isupper():
                path_stack.append((link, visited | {link}, revisited))
                continue
            
            if revisited or not revisits:
                continue
            
            path_stack.append((link, visited, True))
    return count


@aoc.register(__file__)
def answers():
    caves = defaultdict(list)

    for edge in aoc.read_lines():
        a, b = edge.rstrip().split('-')

        if b != 'start':
            caves[a].append(b)
        if a != 'start':
            caves[b].append(a)

    yield num_paths2(caves, 'start', 'end')
    yield num_paths2(caves, 'start', 'end', revisits=True)

if __name__ == '__main__':
    aoc.run(profile=True)
