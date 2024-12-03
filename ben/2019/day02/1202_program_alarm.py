import aoc
from aoc.vm import IntcodeVM
import itertools


def run(vm: IntcodeVM, noun: int = 0, verb: int = 0):
    vm.reset()
    vm.program[1] = noun
    vm.program[2] = verb
    while vm.running:
        vm.run()
    return vm.program[0]

def detect(vm: IntcodeVM, target: int) -> int:
    for n, v in itertools.product(range(100), range(100)):
        if run(vm, n, v) == target:
            return 100 * n + v

@aoc.register(__file__)
def answers():
    vm = IntcodeVM(list(map(int, aoc.read_data().split(','))))
    yield run(vm, 12, 2)
    yield detect(vm, target=19690720)

if __name__ == '__main__':
    aoc.run()
