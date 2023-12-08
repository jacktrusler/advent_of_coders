from pathlib import Path
import utils
import math

def quadratic_roots(a: float, b: float, c: float) -> tuple[float, float]:
    sqrt = math.sqrt(b**2 - (4 * a * c))
    x1 = (-b + sqrt) / (2 * a)
    x2 = (-b - sqrt) / (2 * a)
    return (x1, x2) if x1 < x2 else (x2, x1)

def num_options(distance, time):
    roots = quadratic_roots(a=-1, b=time, c=-distance)
    return math.floor(roots[1]) - math.ceil(roots[0]) + 1

def solve(raw_input: str):
    time_line, distance_line = raw_input.splitlines()
    times = [int(x) for x in time_line.split()[1:]]
    distances = [int(x) for x in distance_line.split()[1:]]
    a = 1
    for time, distance in zip(times, distances):
        a *= num_options(distance, time)
    b_distance = int(''.join([str(x) for x in distances]))
    b_time = int(''.join([str(x) for x in times]))
    b = num_options(b_distance, b_time)
    return a, b

if __name__ == '__main__':
    input_path = Path(__file__).parent / "input" / "06.txt"
    utils.report(*utils.run_solution(solve, input_path))
