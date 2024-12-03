import aoc
from aoc.vm import IntcodeVM
import itertools


def thruster_signal(vms: list[IntcodeVM], inputs: tuple[int], feedback: bool = False):
    out = 0
    [x.reset() for x in vms]

    for vm, phase in zip(vms, inputs):
        out = vm.run(phase, out)

    if feedback:
        val = out
        while all(vm.running for vm in vms):
            for vm, phase in zip(vms, inputs):
                val = vm.run(val)
                if not vm.running:
                    return out
            out = val
    
    return out

@aoc.register(__file__)
def answers():
    intcode = list(map(int, aoc.read_data().split(',')))
    vms = [IntcodeVM(intcode) for _ in range(5)]

    # Part One
    results = [thruster_signal(vms, x) for x in itertools.permutations(range(5), r=5)]
    yield max(results)

    # Part Two
    results = (thruster_signal(vms, x, feedback=True) for x in itertools.permutations(range(5, 10), r=5))
    yield max(results)

if __name__ == '__main__':
    aoc.run()
