import aoc


def play_game(starters: list[int], total_turns: int) -> int:
    ages = [0] * total_turns
    for turn, n in enumerate(starters[:-1], 1):
        ages[n] = turn

    prev = starters[-1]
    for turn in range(len(starters), total_turns):
        value = turn - ages[prev]
        if value == turn:
            value = 0
        
        ages[prev] = turn
        prev = value
    return value


@aoc.register(__file__)
def answers():
    starters = list(map(int, aoc.read_data().split(',')))
    yield play_game(starters, 2020)
    yield play_game(starters, 30_000_000)

if __name__ == '__main__':
    aoc.run()
