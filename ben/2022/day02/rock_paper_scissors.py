import aoc
from collections import Counter
from enum import IntEnum


class Option(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

class Outcome(IntEnum):
    WIN = 6
    DRAW = 3
    LOSS = 0


def translator1(opponent: str, me: str) -> dict[tuple, int]:
    match me:
        case 'X':
            choice = Option.ROCK
            result = Outcome.DRAW if opponent == 'A' else (Outcome.WIN if opponent == 'C' else Outcome.LOSS)
        case 'Y':
            choice = Option.PAPER
            result = Outcome.DRAW if opponent == 'B' else (Outcome.WIN if opponent == 'A' else Outcome.LOSS)
        case 'Z':
            choice = Option.SCISSORS
            result = Outcome.DRAW if opponent == 'C' else (Outcome.WIN if opponent == 'B' else Outcome.LOSS)
    return choice + result

def translator2(opponent: str, me: str) -> dict[tuple, int]:
    match me:
        case 'X':
            result = Outcome.LOSS
            choice = Option.ROCK if opponent == 'B' else (Option.PAPER if opponent == 'C' else Option.SCISSORS)
        case 'Y':
            result = Outcome.DRAW
            choice = Option.ROCK if opponent == 'A' else (Option.PAPER if opponent == 'B' else Option.SCISSORS)
        case 'Z':
            result = Outcome.WIN
            choice = Option.ROCK if opponent == 'C' else (Option.PAPER if opponent == 'A' else Option.SCISSORS)
    return choice + result


@aoc.register(__file__)
def answers():
    rounds = Counter([tuple(x.split(' ')) for x in aoc.read_lines()])
    yield sum(v * translator1(*k) for k, v in rounds.items())
    yield sum(v * translator2(*k) for k, v in rounds.items())

if __name__ == '__main__':
    aoc.run()
