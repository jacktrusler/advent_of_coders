import aoc
import re


def parse_line(line: str) -> tuple:
    data = re.match(r'(?P<min>\d+)-(?P<max>\d+) (?P<letter>[a-z]): (?P<password>[a-z]+)', line).groups()
    return int(data[0]), int(data[1]), data[2], data[3]

def validity_minmax(min: int, max: int, letter: str, password: str) -> bool:
    return min <= password.count(letter) <= max

def validity_position(first: int, second: int, letter: str, password: str) -> bool:
    return (password[first-1] == letter) ^ (password[second-1] == letter)

@aoc.register(__file__)
def answers():
    data = [parse_line(line) for line in aoc.read_lines()]
    yield sum([validity_minmax(*x) for x in data])
    yield sum([validity_position(*x) for x in data])

if __name__ == '__main__':
    aoc.run()
