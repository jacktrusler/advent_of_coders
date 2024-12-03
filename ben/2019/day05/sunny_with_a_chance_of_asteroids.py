import aoc
from aoc.vm import IntcodeVM


@aoc.register(__file__)
def answers():
    vm = IntcodeVM(list(map(int, aoc.read_data().split(','))))
    while vm.running:
        out = vm.run(1)
    yield out

    vm.reset()
    while vm.running:
        out = vm.run(5)
    yield out

if __name__ == '__main__':
    aoc.run()
