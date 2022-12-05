from __future__ import annotations
from collections import Counter
import numpy as np
from dataclasses import dataclass
from typing import Tuple, List, Dict, Counter


@dataclass(eq=True, frozen=True)
class GameState:
    p1_pos: int
    p1_score: int
    p2_pos: int
    p2_score: int

    def __repr__(self):
        return f'GameState({self.p1_pos}, {self.p1_score} | {self.p2_pos}, {self.p2_score})'

    def move_player(self, id:int, spaces:int):
        if id == 1:
            new_pos = (self.p1_pos + spaces - 1) % 10 + 1
            return GameState(new_pos, self.p1_score + new_pos, self.p2_pos, self.p2_score)
        else:
            new_pos = (self.p2_pos + spaces - 1) % 10 + 1
            return GameState(self.p1_pos, self.p1_score, new_pos, self.p2_score + new_pos)

    def outcomes(self, player:int, roll_spread:Counter[int, int]):
        return ScoreCard(Counter({self.move_player(player, k): count for k, count in roll_spread.items()}))

    def win(self):
        return self.p1_score >= 21 or self.p2_score >= 21


class ScoreCard:
    def __init__(self, states:Counter[GameState, int]=None):
        self.states = states if states is not None else Counter({})

    def __repr__(self):
        return f'ScoreCard({repr(dict(self.states))})'

    def __getitem__(self, key):
        return self.states[key]

    def __setitem__(self, key, value):
        self.states[key] = value

    def __delitem__(self, key):
        del self.states[key]

    def items(self):
        return self.states.items()

    def __add__(self, other:ScoreCard):
        return ScoreCard(self.states + other.states)

    def __mul__(self, mod:int):
        new_states = Counter({k: v*mod for k, v in self.states.items()})
        return ScoreCard(new_states)

    def __bool__(self):
        return bool(self.states)

    def pull_wins(self):
        old_len = len(self.states)
        self.states = {state: count for state, count in self.states.items() if not state.win()}
        return old_len - len(self.states)


def roll(player:int, score_card:ScoreCard, outcomes:Counter[int, int]):
    new_score_card = ScoreCard()

    for state, count in score_card.items():
        new_score_card = new_score_card + state.outcomes(player, outcomes) * count

    return new_score_card

    
        


# class Player:
#     def __init__(self, id, start, opponent:Player=None, score=0):
#         self.id:int = id
#         self.position:int = start
#         self.score:int = score
#         self.opponent:Player = opponent
#         self.wins:int = 0

#     def __repr__(self):
#         return f'<{self.position}, {self.score}>'

#     def move(self, spaces):
#         new_pos = (self.position + spaces - 1) % 10 + 1
#         return Player(self.id, new_pos, self.opponent, self.score + new_pos)


# def roll(player_id:int, score_chart, outcomes):
#     new_scores = {}
#     other_player_id = 1 if player_id == 0 else 0
#     for players, count in score_chart.items():
#         player, other_player = players[player_id], players[other_player_id]

#         # temp_scores = {}
#         # for outcome, o_count in outcomes.items():
#         #     _s = (0, 0)
#         #     new_score = (board_pos + outcome - 1) % 10 + 1
#         #     _s[other_player] = other_score
#         #     _s[player.id] = my_score + new_score
#         #     temp_scores[_s] = count * o_count

#         if player.id == 0:
#             temp_scores = {(player.move(outcome), other_player): count * o_count for outcome, o_count in outcomes.items()}
#         else:
#             temp_scores = {(other_player, player.move(outcome)): count * o_count for outcome, o_count in outcomes.items()}

#         for k, v in temp_scores.items():
#             new_scores[k] = new_scores.get(k, 0) + v
#     return new_scores

# def roll(player:int, score_chart, outcomes):
#     new_score_chart = {}
#     other_player = 1 if player == 0 else 0

#     for outcome, o_count in outcomes.items():
#         for positions, score_counts in score_chart.items():
#             new_pos = (positions[player] + outcome - 1) % 10 + 1
#             scores, counts = list(score_counts.keys()), list(score_counts.values())
#             scores = list(map(lambda x: (x[0] + new_pos, x[1]), scores))
#             counts = list(map(lambda x: x * o_count, counts))
#             score_dict = dict(zip(scores, counts))

#             new_pos = (new_pos, positions[other_player]) if player == 0 else (positions[other_player], new_pos)
#             asdf = new_score_chart.get(new_pos, {})
#             for k, v in score_dict.items():
#                 asdf[k] = asdf.get(k, 0) + v
#     return new_score_chart
            




with open('2021/day21/small.txt') as f:
    positions = f.read().splitlines()
    p1_pos, p2_pos = int(positions[0].split(':')[1].strip()), int(positions[1].split(':')[1].strip())

init_state = GameState(p1_pos=p1_pos, p1_score=0, p2_pos=p2_pos, p2_score=0)
score_chart = ScoreCard(Counter({init_state: 1}))
quantum_rolls = sorted([x+y+z+3 for x in range(3) for y in range(3) for z in range(3)])
quantum_rolls = Counter(quantum_rolls)

turn = 1
wins = [0, 0]
while score_chart:
    print('-----------------------------')
    print(turn)
    print(len(score_chart.states))
    score_chart = roll(turn, score_chart, quantum_rolls)
    wins[turn-1] += score_chart.pull_wins()
    turn = turn % 2 + 1

print(wins)
#341960390180808
#822385675458