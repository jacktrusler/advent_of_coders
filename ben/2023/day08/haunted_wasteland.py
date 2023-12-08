import aoc
import itertools
import math


def parse_node(node_str: str) -> tuple[str, tuple[str, str]]:
    key, values = node_str.split(' = ')
    values = values[1:-1].split(', ')
    return key, values


@aoc.register(__file__)
def answers():
    right_left, nodes = aoc.read_chunks()
    INSTRUCTIONS = [int(x == 'R') for x in right_left]
    NODE_MAP = {k: v for k, v in map(parse_node, nodes.splitlines())}

    def traverse(start: str, end: set[str]) -> int:
        node = start
        for step, dir in enumerate(itertools.cycle(INSTRUCTIONS), start=1):
            node = NODE_MAP[node][dir]
            if node in end:
                break
        return step
    yield traverse(start='AAA', end={'ZZZ'})

    a_nodes = {x for x in NODE_MAP.keys() if x.endswith('A')}
    z_nodes = {x for x in NODE_MAP.keys() if x.endswith('Z')}
    yield math.lcm(*(traverse(x, z_nodes) for x in a_nodes))

if __name__ == '__main__':
    aoc.run()
