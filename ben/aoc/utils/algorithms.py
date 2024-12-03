import math


def quadratic(a: int, b: int, c: int) -> tuple[float, float]:
    _sqrt = math.sqrt(b**2 - 4*a*c)
    _denom = 2*a
    return sorted(((-b + _sqrt) / _denom, (-b - _sqrt) / _denom))