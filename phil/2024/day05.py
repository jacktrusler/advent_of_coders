from collections import defaultdict
from functools import cmp_to_key

def solve(puzzle_input: str):
    pages_after = defaultdict(set)

    def sort_pages(page1: str, page2: str) -> int:
        if page2 in pages_after[page1]:
            return -1
        if page1 in pages_after[page2]:
            return 1
        return 0

    rules_text, updates_text = puzzle_input.split('\n\n')
    for rule in rules_text.split():
        left, right = rule.split('|')
        pages_after[left].add(right)
    a = 0
    b = 0
    for update in updates_text.split():
        page_list = update.split(',')
        working_page_list = page_list.copy()
        while working_page_list:
            page = working_page_list.pop()
            if pages_after[page] & set(working_page_list):
                sorted_page_list = sorted(page_list, key=cmp_to_key(sort_pages))
                b += int(sorted_page_list[len(sorted_page_list) // 2])
                break
        else:
            a += int(page_list[len(page_list) // 2])
    return a, b

if __name__ == '__main__':
    from pathlib import Path
    import aoc_util
    input_path = Path(__file__).parent / "input" / "05.txt"
    aoc_util.report(*aoc_util.run_solution(solve, input_path))
