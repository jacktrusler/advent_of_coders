import re

def solve(puzzle_input: str):
    size = puzzle_input.index('\n')
    a_patterns = [
        'XMAS', # right
        'SAMX', # left
        f'(?=X.{{{size}}}M.{{{size}}}A.{{{size}}}S)', # down
        f'(?=S.{{{size}}}A.{{{size}}}M.{{{size}}}X)', # up
        f'(?=X(?!.{{0,2}}\s).{{{size+1}}}M.{{{size+1}}}A.{{{size+1}}}S)', # down right
        f'(?=S(?!.{{0,2}}\s).{{{size+1}}}A.{{{size+1}}}M.{{{size+1}}}X)', # up left
        f'(?=\S{{3}}X.{{{size-1}}}M.{{{size-1}}}A.{{{size-1}}}S)', # down left
        f'(?=\S{{3}}S.{{{size-1}}}A.{{{size-1}}}M.{{{size-1}}}X)', # up right
    ]
    b_patterns = [
        f'(?=M\SS.{{{size-1}}}A.{{{size-1}}}M\SS)',
        f'(?=M\SM.{{{size-1}}}A.{{{size-1}}}S\SS)',
        f'(?=S\SM.{{{size-1}}}A.{{{size-1}}}S\SM)',
        f'(?=S\SS.{{{size-1}}}A.{{{size-1}}}M\SM)',
    ]
    text = ' '.join(puzzle_input.split()) # replace newlines with spaces to play nicely with regex.
    a = sum(len(re.findall(p, text)) for p in a_patterns)
    b = sum(len(re.findall(p, text)) for p in b_patterns)
    return a, b

if __name__ == '__main__':
    from pathlib import Path
    import aoc_util
    input_path = Path(__file__).parent / "input" / "04.txt"
    aoc_util.report(*aoc_util.run_solution(solve, input_path))
