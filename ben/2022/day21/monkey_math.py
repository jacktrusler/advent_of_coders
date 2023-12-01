from __future__ import annotations
import aoc
from dataclasses import dataclass
import math
import operator
import re


@dataclass
class Algebraic:
    multiplier: int = 1
    linear: int = 0
    divisor: int = 1

    def __add__(self, v: int):
        return Algebraic(multiplier=self.multiplier, linear=self.linear + (self.divisor * v), divisor=self.divisor).reduce()

    def __radd__(self, v: int):
        return self.__add__(v)
    
    def __sub__(self, v: int):
        return Algebraic(multiplier=self.multiplier, linear=self.linear - (self.divisor * v), divisor=self.divisor).reduce()

    def __rsub__(self, v: int):
        return Algebraic(multiplier=-self.multiplier, linear=(self.divisor * v) - self.linear, divisor=self.divisor).reduce()

    def __mul__(self, v: int):
        return Algebraic(multiplier=(self.multiplier * v), linear=(self.linear * v), divisor=self.divisor).reduce()

    def __rmul__(self, v: int):
        return self.__mul__(v)

    def __floordiv__(self, v: int):
        return Algebraic(multiplier=self.multiplier, linear=self.linear, divisor=(self.divisor * v)).reduce()

    def reduce(self) -> Algebraic:
        gcd = math.gcd(self.multiplier, self.linear, self.divisor)
        return Algebraic(multiplier=self.multiplier // gcd, linear=self.linear // gcd, divisor = self.divisor // gcd)

    @staticmethod
    def solve_for_x(left: int | Algebraic, right: int | Algebraic):
        alg = left if isinstance(left, Algebraic) else right
        lin = left if isinstance(left, int) else right

        lin *= alg.divisor
        lin -= alg.linear
        return lin // alg.multiplier

def value(monkeys: dict[str, str], name: str) -> int:
    eq = monkeys[name]
    try:
        return int(eq)
    except (TypeError, ValueError):
        if isinstance(eq, Algebraic):
            return eq
        pass
        
    m1, op, m2 = eq.split()
    match op:
        case '+': op = operator.add
        case '-': op = operator.sub
        case '*': op = operator.mul
        case '/': op = operator.floordiv
        case '=': op = Algebraic.solve_for_x
    return op(value(monkeys, m1), value(monkeys, m2))


@aoc.register(__file__)
def answers():
    monkeys = (line.split(':') for line in aoc.read_lines('small'))
    monkeys = {name: value.strip() for name, value in monkeys}
    yield value(monkeys, 'root')

    monkeys['root'] = re.sub(r'(\*|\+|\/|\-)', '=', monkeys['root'])
    monkeys['humn'] = Algebraic()
    yield value(monkeys, 'root')

if __name__ == '__main__':
    aoc.run()
