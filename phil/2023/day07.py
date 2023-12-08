from pathlib import Path
import functools
import collections
import utils


CARD_VALUES = {str(x): x for x in range(2, 10)} | {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
CARD_VALUES_B = CARD_VALUES.copy()
CARD_VALUES_B['J'] = 1
HAND_VALUES = {
    (5,): 7,
    (4, 1): 6,
    (3, 2): 5,
    (3, 1, 1): 4,
    (2, 2, 1): 3,
    (2, 1, 1, 1): 2,
}

@functools.cache
def hand_value(hand_tuple: tuple) -> int:
    try:
        return HAND_VALUES[hand_tuple]
    except KeyError:
        for k, v in HAND_VALUES.items():
            if len(hand_tuple) > len(k):
                continue
            for i in range(len(hand_tuple)):
                if hand_tuple[i] > k[i]:
                    break
            else:
                return v
    return 1

def hand_tuple(counter: collections.Counter) -> tuple:
    return tuple(sorted(counter.values(), reverse=True))

def winnings(hand_scores: list) -> int:
    return sum([x[1] * (i + 1) for i, x in enumerate(sorted(hand_scores))])

def solve(raw_input: str):
    hand_scores_a = list()
    hand_scores_b = list()
    for line in raw_input.splitlines():
        hand_counter = collections.defaultdict(int)
        values_a = list()
        values_b = list()
        hand, bid_string = line.split()
        for card in hand:
            hand_counter[card] += 1
            values_a.append(CARD_VALUES[card])
            values_b.append(CARD_VALUES_B[card])
        a_value = (hand_value(hand_tuple(hand_counter)), *values_a)
        hand_counter.pop('J', None)
        b_value = (hand_value(hand_tuple(hand_counter)), *values_b)
        bid = int(bid_string)
        hand_scores_a.append((a_value, bid))
        hand_scores_b.append((b_value, bid))
    a = winnings(hand_scores_a)
    b = winnings(hand_scores_b)
    return a, b

if __name__ == '__main__':
    input_path = Path(__file__).parent / "input" / "07.txt"
    utils.report(*utils.run_solution(solve, input_path))
