import aoc
from functools import reduce


Stacks = dict[int, tuple[str]]

def parse_state(state: str) -> Stacks:
    lines = state.splitlines()
    crates, stacks = lines[:-1], lines[-1]
    return {int(stack_no): tuple(row[i] for row in reversed(crates) if row[i] != ' ')
            for i, stack_no in enumerate(stacks) if stack_no != ' '}

def move(stacks: Stacks, movement: str, reverse: bool = True) -> Stacks:
    m = movement.split()
    amount, start, end = int(m[1]), int(m[3]), int(m[5])

    retval = stacks.copy()
    to_move = stacks[start][-amount:]
    retval[start] = stacks[start][:-amount]
    retval[end] = stacks[end] + tuple(reversed(to_move) if reverse else to_move)
    return retval


@aoc.register(__file__)
def answers():
    initial_state, movements = aoc.read_chunks()
    stacks = parse_state(initial_state)
    movements = movements.splitlines()
    
    stacks1 = reduce(lambda x,y: move(x, y), movements, stacks)
    yield ''.join([q[-1] for q in stacks1.values()])

    stacks2 = reduce(lambda x,y: move(x, y, reverse=False), movements, stacks)
    yield ''.join([q[-1] for q in stacks2.values()])

if __name__ == '__main__':
    aoc.run()
