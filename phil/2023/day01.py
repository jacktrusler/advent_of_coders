from pathlib import Path
import re
import utils

def solve(raw_input: str):
    a = 0
    b = 0
    digit_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    digit_chars = [str(n+1) for n in range(len(digit_words))]
    digit_map = {x: y for x, y in zip(digit_words, digit_chars)} | {y: y for y in digit_chars} 
    digit_set = set(digit_words)
    pattern = re.compile(f'{"|".join(digit_map.keys())}')
    for line in raw_input.splitlines():
        matches = pattern.findall(line)
        matches_a = list(filter(lambda x: x not in digit_set, matches))
        a += int(matches_a[0] + matches_a[-1])
        b += int(digit_map[matches[0]] + digit_map[matches[-1]])
    return a, b

if __name__ == '__main__':
    input_path = Path(__file__).parent / "input" / "01.txt"
    utils.report(*utils.run_solution(solve, input_path))
    