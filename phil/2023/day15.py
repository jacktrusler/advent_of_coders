from pathlib import Path
import utils
import functools


@functools.cache
def hash(string: str, current_value: int=0) -> int:
    for character in string:
        current_value = ((current_value + ord(character)) * 17) % 256
    return current_value

def focusing_power(boxes: list) -> int:
    focusing_power = 0
    for box, lenses in enumerate(boxes):
        for lens_position, focal_length in enumerate(lenses.values()):
            focusing_power += (box+1) * (lens_position+1) * int(focal_length)
    return focusing_power

def solve(raw_input: str) -> tuple[int, int]:
    a = 0
    boxes = [dict() for _ in range(256)]
    for step in raw_input.strip().split(","):
        a += hash(step)
        if step[-1] == '-':
            label = step[:-1]
            boxes[hash(label)].pop(label, None)
        else:
            label = step[:-2]
            boxes[hash(label)][label] = step[-1]
    b = focusing_power(boxes)
    return a, b

if __name__ == '__main__':
    input_path = Path(__file__).parent / "input" / "15.txt"
    utils.report(*utils.run_solution(solve, input_path))
