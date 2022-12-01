import aoc


@aoc.register(__file__)
def answers():
    per_elf = sorted(sum(map(int, x.splitlines())) for x in aoc.read_chunks())
    yield per_elf[-1]
    yield sum(per_elf[-3:])

if __name__ == '__main__':
    aoc.run()
