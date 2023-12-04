import aoc


def matches(card_str: str) -> set[int]:
    winning, mine = card_str.split(': ')[1].split(' | ')
    winning = {int(x) for x in winning.strip().split()}
    mine = {int(x) for x in mine.strip().split()}
    return winning & mine


@aoc.register(__file__)
def answers():
    cards = aoc.read_lines()

    score = 0
    copies = {x: 1 for x in range(1, len(cards) + 1)}
    for i, card in enumerate(cards, start=1):
        if num_matches := len(matches(card)):
            score += 2 ** (num_matches - 1)

            top_card = min(len(cards), i + num_matches)
            for new_copy in range(i + 1, top_card + 1):
                copies[new_copy] += copies[i]
    yield int(score)
    yield sum(copies.values())

if __name__ == '__main__':
    aoc.run()
