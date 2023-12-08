import aoc


@aoc.register(__file__)
def answers():
    cards = aoc.read_lines()

    score = 0
    copies = {x: 1 for x in range(1, len(cards) + 1)}
    for i, card in enumerate(cards, start=1):
        winning, mine = card.split(': ')[1].split(' | ')
        matches = set(winning.split()) & set(mine.split())

        if num_matches := len(matches):
            score += 2 ** (num_matches - 1)

            top_card = min(len(cards), i + num_matches)
            for new_copy in range(i + 1, top_card + 1):
                copies[new_copy] += copies[i]
    yield int(score)
    yield sum(copies.values())

if __name__ == '__main__':
    aoc.run()
