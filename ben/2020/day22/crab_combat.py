from __future__ import annotations
import aoc
from collections import deque
from dataclasses import dataclass, field
import itertools
import re
from typing import Iterable, Generator


class Player:
    def __init__(self, id: int, deck: Iterable[int]):
        self.id = id
        self.deck = deque(deck)

    def __eq__(self, other: Player):
        return self.id == other.id

    @property
    def empty(self) -> bool:
        return len(self.deck) == 0

    def draw(self) -> int:
        return self.deck.popleft()

    def top(self, amt: int) -> tuple[int]:
        return tuple(itertools.islice(self.deck, 0, amt))

    def collect(self, cards: Iterable[int]):
        self.deck.extend(cards)

    def score(self) -> int:
        return sum([(idx+1) * x for idx, x in enumerate(reversed(self.deck))])

    @staticmethod
    def from_string(player_str: str) -> Player:
        lines = player_str.splitlines()
        pid = re.match(r'Player (.*):', lines[0])[1]
        deck = [int(x) for x in lines[1:]]
        return Player(id=int(pid), deck=deck)

@dataclass
class Combat:
    p1: Player
    p2: Player

    def _complete(self) -> bool:
        return self.p1.empty or self.p2.empty

    def _winner(self, card1: int, card2: int) -> Player:
        return self.p1 if card1 > card2 else self.p2

    def _turns(self) -> Generator:
        while True:
            if self._complete():
                return
            yield self.p1.draw(), self.p2.draw()

    def play(self) -> Player:
        for card1, card2 in self._turns():
            if self._winner(card1, card2) == self.p1:
                self.p1.collect((card1, card2))
            else:
                self.p2.collect((card2, card1))
        return self.p1 if self.p2.empty else self.p2


class RecursionError(Exception):
    pass

@dataclass
class RecursiveCombat(Combat):
    _memory: set = field(default_factory=set)
    
    def _complete(self):
        state = tuple(self.p1.deck), tuple(self.p2.deck)
        if state in self._memory:
            raise RecursionError
        self._memory.add(state)
        return super()._complete()

    def _winner(self, card1, card2):
        if card1 <= len(self.p1.deck) and card2 <= len(self.p2.deck):
            p1top, p2top = self.p1.top(card1), self.p2.top(card2)

            if max(p1top) > max(p2top):
                return self.p1
            return RecursiveCombat(p1=Player(1, p1top), p2=Player(2, p2top)).play()
        return super()._winner(card1, card2)

    def play(self):
        try:
            return super().play()
        except RecursionError:
            return self.p1


@aoc.register(__file__)
def answers():
    player_data = aoc.read_chunks()

    p1, p2 = (Player.from_string(block) for block in player_data)
    winner1 = Combat(p1, p2).play()
    yield winner1.score()

    p1, p2 = (Player.from_string(block) for block in player_data)
    winner2 = RecursiveCombat(p1, p2).play()
    yield winner2.score()

if __name__ == '__main__':
    aoc.run()
