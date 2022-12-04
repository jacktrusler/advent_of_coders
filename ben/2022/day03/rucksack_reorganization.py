import aoc
from string import ascii_lowercase, ascii_uppercase


def check_compartment(items: str) -> int:
    common_item = set(items[len(items)//2:]) & set(items[:len(items)//2])
    return list(common_item)[0]

def check_group(sacks: list[str]) -> int:
    common_item = set.intersection(*map(set, sacks))
    return list(common_item)[0]


@aoc.register(__file__)
def answers():
    rucksacks = [list(x) for x in aoc.read_lines()]
    priorities = {char: i+1 for i, char in enumerate(list(ascii_lowercase) + list(ascii_uppercase))}

    yield sum(priorities[check_compartment(x)] for x in rucksacks)
    yield sum(priorities[check_group(rucksacks[i:i+3])] for i in range(0, len(rucksacks), 3))

if __name__ == '__main__':
    aoc.run()
