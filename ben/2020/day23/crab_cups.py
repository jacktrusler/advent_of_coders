import aoc
from typing import Iterable


def build_list(init_cups: Iterable[int], num_turns: int, num_cups: int = None) -> list[int]:
    max_cup = num_cups if num_cups is not None else len(init_cups)
    cups = [0] + list(range(max_cup + 2))[2:]
    for cup1, cup2 in zip(init_cups, init_cups[1:]):
        cups[cup1] = cup2

    if num_cups is None:
        cups[init_cups[-1]] = init_cups[0]
    else:
        cups[-1] = init_cups[0]
        cups[init_cups[-1]] = len(init_cups) + 1
    return cups

def play_game(init_cups: Iterable[int], num_turns: int, num_cups: int = None):
    cups = build_list(init_cups, num_turns, num_cups)
    max_cup = len(cups) - 1
    
    current_cup = init_cups[0]
    for _ in range(num_turns):
        first = cups[current_cup]
        second = cups[first]
        third = cups[second]
        moving_cups = first, second, third

        dest = max_cup if current_cup == 1 else current_cup - 1
        while dest in moving_cups:
            dest = max_cup if dest == 1 else dest - 1

        new_next = cups[third]
        cups[current_cup] = new_next
        cups[third] = cups[dest]
        cups[dest] = first
        current_cup = new_next
    return cups

def build_from_one(cups: list[int]) -> str:
    idx = cups[1]
    retval = ''
    while idx != 1:
        retval += str(idx)
        idx = cups[idx]
    return retval


@aoc.register(__file__)
def answers():
    cups = [int(x) for x in aoc.read_data()]

    cups1 = play_game(cups, num_turns=100)
    yield build_from_one(cups1)

    cups2 = play_game(cups, num_turns=10_000_000, num_cups=1_000_000)
    next1 = cups2[1]
    next2 = cups2[next1]
    yield next1 * next2

if __name__ == '__main__':
    aoc.run()
