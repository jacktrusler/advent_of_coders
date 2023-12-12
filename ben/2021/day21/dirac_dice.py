from __future__ import annotations
import aoc
from collections import deque, Counter
from dataclasses import dataclass, replace
import itertools
import math
import re


@dataclass(frozen=True)
class Player:
    id: int
    position: int
    score: int = 0

    def move(self, spaces: int) -> Player:
        position = (self.position + spaces - 1) % 10 + 1
        return replace(self, position=position, score=self.score + position)

    @staticmethod
    def from_string(data: str) -> Player:
        m = re.match(r'Player (?P<id>\d+) starting position: (?P<position>\d+)', data).groupdict()
        return Player(id=int(m['id']), position=int(m['position']))

class DeterministicDie:
    def __init__(self, rolls_per_turn: int):
        self.rolls = itertools.cycle(range(1, 101))
        self.per = rolls_per_turn

    def __iter__(self):
        while True:
            yield sum(itertools.islice(self.rolls, self.per))

    @staticmethod
    def play_game(p1: Player, p2: Player) -> tuple[int, int]:
        state = deque([p1, p2])
        die = DeterministicDie(3)
        for turn, roll in enumerate(die):
            player = state.popleft().move(roll)
            if player.score >= 1000:
                return die.per * (turn+1), state[-1].score
            state.append(player)

class QuantumDie:
    QUANTUM_ROLLS = Counter(sum(x) for x in itertools.product(range(1, 4), repeat=3))

    @dataclass(frozen=True)
    class State:
        player1: Player
        player2: Player

        def update(self, turn: int, roll: int) -> QuantumDie.State:
            if turn == 1:
                return replace(self, player1=self.player1.move(roll))
            return replace(self, player2=self.player2.move(roll))
        
        @property
        def winner(self) -> int | None:
            if self.player1.score >= 21: return self.player1.id
            if self.player2.score >= 21: return self.player2.id
            return None

    @staticmethod
    def play_game(p1: Player, p2: Player) -> int:
        states = Counter([QuantumDie.State(p1, p2)])
        wins = Counter({p1.id: 0, p2.id: 0})
        
        for turn in itertools.cycle((1, 2)):
            prev, states = states, Counter()
            for (state, universes), (roll, roll_count) in itertools.product(prev.items(), QuantumDie.QUANTUM_ROLLS.items()):
                universes *= roll_count
                state = state.update(turn, roll)
                if winner := state.winner:
                    wins[winner] += universes
                    continue
                states[state] += universes
            if not states:
                break
        return max(wins.values())


@aoc.register(__file__)
def answers():
    players = [Player.from_string(x) for x in aoc.read_lines()]
    yield math.prod(DeterministicDie.play_game(*players))
    yield QuantumDie.play_game(*players)

if __name__ == '__main__':
    aoc.run()
