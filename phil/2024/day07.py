def valid_equation(target_value: int, numbers: list, concatenation: bool = False) ->  bool:
    if len(numbers) == 1:
        if target_value == numbers[0]:
            return True
        return False
    else:
        if target_value < 0:
            return False
        if valid_equation(target_value - numbers[-1], numbers[:-1], concatenation):
            return True
        if target_value % numbers[-1] == 0:
            if valid_equation(target_value // numbers[-1], numbers[:-1], concatenation):
                return True
        if concatenation and str(target_value).endswith(str(numbers[-1])) and target_value != numbers[-1]:
            if valid_equation(int(str(target_value)[:-len(str(numbers[-1]))]), numbers[:-1], concatenation):
                return True
    return False

def solve(puzzle_input: str):
    a = 0
    b = 0
    for line in puzzle_input.splitlines():
        test_value, numbers_string = line.split(':')
        test_value = int(test_value)
        numbers = [int(x) for x in numbers_string.split()]
        if valid_equation(test_value, numbers):
            a += test_value
        if valid_equation(test_value, numbers, concatenation=True):
            b += test_value
    return a, b

if __name__ == '__main__':
    from pathlib import Path
    import aoc_util
    input_path = Path(__file__).parent / "input" / "07.txt"
    aoc_util.report(*aoc_util.run_solution(solve, input_path))
