from __future__ import annotations
import aoc
from collections import Counter


class Hand:
    translator = str.maketrans('TJQKA', 'ABCDE')

    def __init__(self, cards: str, bid: int|str):
        self.cards = cards
        self.bid = int(bid)
        self._strength = (self._pairs(), cards.translate(self.translator))
    
    def _pairs(self) -> list[int]:
        return sorted(Counter(self.cards).values(), reverse=True)
    
    def __lt__(self, other: Hand) -> bool:
        return self._strength < other._strength
    
    
class JokerHand(Hand):
    translator = str.maketrans('JTQKA', '0ABCD')

    def _pairs(self) -> list[int]:
        counter = Counter(self.cards)
        jokers = counter.pop('J', 0)
        pairs = sorted(counter.values(), reverse=True)
        try:
            pairs[0] += jokers
        except IndexError:
            pairs = [5]
        return pairs


@aoc.register(__file__)
def answers():
    data = [x.split() for x in aoc.read_lines()]

    hands = [Hand(*x) for x in data]
    yield sum(rank * hand.bid for rank, hand in enumerate(sorted(hands), start=1))

    hands = [JokerHand(*x) for x in data]
    yield sum(rank * hand.bid for rank, hand in enumerate(sorted(hands), start=1))

if __name__ == '__main__':
    aoc.run()
