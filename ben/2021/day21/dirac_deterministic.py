from numpy.typing import NDArray
from typing import Tuple, List, Dict


class DeterministicDie:
    def __init__(self):
        self.num_rolls:int = 0
        self.next_roll:int = 1

    def __repr__(self):
        return f'DeterministicDie({self.next_roll})'

    def roll(self, count=1):
        result = [(self.next_roll + x - 1) % 100 + 1 for x in range(count)]
        self.num_rolls += count
        self.next_roll = result[-1] + 1
        return result


class Player:
    def __init__(self, id, pos):
        self.id = id
        self.position = pos
        self.score = 0

    def __repr__(self):
        return f'Player({self.id})'

    def move(self, spaces):
        self.position = (self.position + spaces - 1) % 10 + 1
        self.score += self.position
        return self.position

    def win(self):
        return self.score >= 1000


with open('2021/day21/starting_positions.txt') as f:
    positions = f.read().splitlines()
    p1_pos, p2_pos = int(positions[0].split(':')[1].strip()), int(positions[1].split(':')[1].strip())

die = DeterministicDie()
players = [Player(1, p1_pos), Player(2, p2_pos)]

turn = 0
while all([not x.win() for x in players]):
    active_player = players[turn]
    active_player.move(sum(die.roll(count=3)))
    turn = (turn + 1) % len(players)

print(f'Scores:\n\tPlayer 1: {players[0].score}\n\tPlayer 2: {players[1].score}')
loser = players[0] if not players[0].win() else players[1]
print(loser.score * die.num_rolls)