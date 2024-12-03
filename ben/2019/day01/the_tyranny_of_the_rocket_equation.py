import aoc


def fuel(mass: int) -> int:
    return max((mass // 3) - 2, 0)

@aoc.register(__file__)
def answers():
    modules = list(map(int, aoc.read_lines()))

    fuels = [fuel(x) for x in modules]
    total = sum(fuels)
    yield total

    while any(fuels):
        fuels = [fuel(x) for x in fuels]
        total += sum(fuels)
    yield total

if __name__ == '__main__':
    aoc.run()
