from pathlib import Path
import utils
import functools

@functools.cache
def match_count(string: str, groups: tuple):
    if len(string) < sum(groups) + len(groups) - 1:
        return 0
    test_group = string[:groups[0]]
    if "." in test_group:
        if string[0] == '#':
            return 0
        else:
            return match_count(string[1:], groups)
    elif len(test_group) == len(string):
        return 1
    else:
        count = 0
        if string[len(test_group)] in ".?":
            # recurse, assuming it's a match
            new_string = string[groups[0]+1:].lstrip('.')
            new_groups = groups[1:]
            if len(new_groups) == 0:
                if "#" not in new_string:
                    count += 1
            else:
                count += match_count(new_string, new_groups)
        if string[0] == '?':
            # recurse, assuming it's not a match
            count += match_count(string[1:].lstrip('.'), groups)
        return count

def solve(raw_input: str):
    a = 0
    b = 0
    for line in raw_input.splitlines():
        springs, group_string = line.split()
        groups = tuple(int(x) for x in group_string.split(","))
        a += match_count(springs, groups)
        b += match_count('?'.join([springs] * 5), groups * 5)
    return a, b

if __name__ == '__main__':
    input_path = Path(__file__).parent / "input" / "12.txt"
    utils.report(*utils.run_solution(solve, input_path))
