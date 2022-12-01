import aoc


@aoc.register(__file__)
def answers():
    groups = [[set(x) for x in chunk.split('\n')] for chunk in aoc.read_chunks()]
    yield sum((len(set.union(*x)) for x in groups))
    yield sum((len(set.intersection(*x)) for x in groups))

if __name__ == '__main__':
    aoc.run()
