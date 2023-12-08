from pathlib import Path
import utils
import math
import itertools
import collections

def solve(raw_input: str):
    instructions, nodes = raw_input.split("\n\n")
    map = dict()
    sources = list()
    for line in nodes.splitlines():
        line_parts=line.split()
        source = line_parts[0]
        map[source] = {"L": line_parts[2][1:-1], 'R': line_parts[3][:-1]}
        if source[2] == 'A':
            sources.append(source)
    results = collections.defaultdict(dict)
    for start_node in sources:
        seen_nodes = dict()
        current_node = start_node
        steps = 0
        for i, direction in itertools.cycle(enumerate(instructions)):
            node_key = (i, current_node)
            if node_key in seen_nodes:
                break
            else:
                seen_nodes[node_key] = steps
                if current_node[2] == 'Z':
                    # assume that any synced end nodes will be found after the start of a
                    # network loop. This is a bad assumption, but if it weren't the case,
                    # B would be trivial to solve, so it's probably an accurate one.
                    results[start_node][current_node] = steps
            current_node = map[current_node][direction]
            steps += 1
    a = results['AAA']['ZZZ']
    b = min(math.lcm(*x) for x in itertools.product(*[x.values() for x in results.values()]))
    return a, b

if __name__ == '__main__':
    input_path = Path(__file__).parent / "input" / "08.txt"
    utils.report(*utils.run_solution(solve, input_path))
