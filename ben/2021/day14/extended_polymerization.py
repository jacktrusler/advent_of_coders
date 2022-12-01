import aoc
from collections import Counter
from functools import reduce


def step(pairs: Counter, rules: dict) -> Counter:
    retval = Counter()
    for pair, count in pairs.items():
        for rule in rules[pair]:
            retval[rule] += count
    return retval

def count_elements(pairs: Counter, last: str) -> Counter:
    occurrences = Counter({last: 1})
    for (element, _), count in pairs.items():
        occurrences[element] += count
    return max(occurrences.values()) - min(occurrences.values())


@aoc.register(__file__)
def answers():
    template, rules = map(str.strip, aoc.read_chunks())
    rules = list(tuple(x.split(' -> ')) for x in rules.splitlines())
    rules = {(x[0][0], x[0][1]): ((x[0][0], x[1]), (x[1], x[0][1])) for x in rules}

    pairs = Counter(zip(template, template[1:]))
    pairs = reduce(lambda x, _: step(x, rules), range(10), pairs)
    yield count_elements(pairs, last=template[-1])
    
    pairs = reduce(lambda x, _: step(x, rules), range(30), pairs)
    yield count_elements(pairs, last=template[-1])

if __name__ == '__main__':
    aoc.run()
