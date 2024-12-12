import aoc


@aoc.register(__file__)
def answers():
    cards = aoc.read_lines()

    score = 0
    copies = [1] * len(cards)
    for i, card in enumerate(cards, start=1):
        winning, mine = (set(x.split()) for x in card.split(':')[1].split('|'))
        if num_matches := len(winning & mine):
            score += 2 ** (num_matches - 1)
            copies[i:i+num_matches] = [x + copies[i-1] for x in copies[i:i+num_matches]]
    yield int(score)
    yield sum(copies)

if __name__ == '__main__':
    aoc.run()
