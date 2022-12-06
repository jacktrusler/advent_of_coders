import aoc
from copy import deepcopy
from functools import reduce
import re


Stacks = dict[int, list[str]]

def parse_state(state: str) -> Stacks:
    lines = state.splitlines()
    crates, stacks = lines[:-1], lines[-1]
    return {int(stack_no): [row[i] for row in reversed(crates) if row[i] != ' '] 
            for i, stack_no in enumerate(stacks) if stack_no != ' '}

def move(stacks: Stacks, movement: str, reverse=True) -> Stacks:
    m = re.match(r'move (\d+) from (\d+) to (\d+)', movement).groups()
    amount, start, end = int(m[0]), int(m[1]), int(m[2])
    to_move = stacks[start][-amount:]
    stacks[start] = stacks[start][:-amount]
    stacks[end].extend(reversed(to_move) if reverse else to_move)
    return stacks


@aoc.register(__file__)
def answers():
    initial_state, movements = aoc.read_chunks()
    stacks = parse_state(initial_state)
    movements = movements.splitlines()
    
    stacks1 = deepcopy(stacks)
    stacks1 = reduce(lambda x,y: move(x, y), movements, stacks1)
    yield ''.join([q[-1] for q in stacks1.values()])

    stacks2 = deepcopy(stacks)
    stacks2 = reduce(lambda x,y: move(x, y, reverse=False), movements, stacks2)
    yield ''.join([q[-1] for q in stacks2.values()])

if __name__ == '__main__':
    aoc.run()
