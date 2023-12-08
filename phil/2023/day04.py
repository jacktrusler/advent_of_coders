from pathlib import Path
import utils

def solve(raw_input: str):
    a = 0
    lines = raw_input.splitlines()
    num_cards = [1] * len(lines)
    for i, line in enumerate(lines):
        _, card_data = line.split(":")
        winning_numbers, numbers = (set(x.split()) for x in card_data.split("|"))
        num_winners = len(winning_numbers & numbers)
        a += 2 ** (num_winners - 1) if num_winners > 0 else 0
        num_cards[i+1:i+num_winners+1] = [n + num_cards[i] for n in num_cards[i+1:i+num_winners+1]]
    b = sum(num_cards)
    return a, b

if __name__ == '__main__':
    input_path = Path(__file__).parent / "input" / "04.txt"
    utils.report(*utils.run_solution(solve, input_path))
