from time import perf_counter
from collections import defaultdict


def parent(path: str) -> str:
    if len(path) == 0:
        raise ValueError
    return path[:path.rfind('/')]


def parents(path: str):
    while True:
        try:
            path = parent(path)
            yield path
        except ValueError:
            break


def get_dir_sizes(raw_input: str) -> dict:
    base_path = ''
    cd = base_path
    scanned_dirs = set()
    dir_sizes = defaultdict(int)
    for group in raw_input.split('$'):
        group = group.strip()
        command = group[:2]
        if command == 'cd':
            destination = group[3:]
            if destination == '..':
                cd = parent(cd)
            elif destination == '/':
                cd = base_path
            else:
                cd = f'{cd}/{destination}'
        elif command == 'ls':
            if cd not in scanned_dirs:
                file_sizes = 0
                for line in group.splitlines()[1:]:
                    description, name = line.split()
                    if description == 'dir':
                        continue
                    file_sizes += int(description)
                dir_sizes[cd] += file_sizes
                for p in parents(cd):
                    dir_sizes[p] += file_sizes
                scanned_dirs.add(cd)
        elif command == '':
            pass
        else:
            raise ValueError(f'Unknown command output: {command}')
    return dir_sizes


def problem_a(raw_input: str) -> int:
    dir_sizes = get_dir_sizes(raw_input)
    return sum([size for size in dir_sizes.values() if size <= 100000])


def problem_b(raw_input: str) -> int:
    dir_sizes = get_dir_sizes(raw_input)
    free_at_least = 30000000 - (70000000 - dir_sizes[''])
    return min(s for s in dir_sizes.values() if s > free_at_least)


if __name__ == '__main__':
    with open('./day7_input.txt', mode='r') as f:
        problem_input = f.read()
    start_a = perf_counter()
    result_a = problem_a(problem_input)
    end_a = perf_counter()
    print(f'A: {result_a}, time: {round((end_a - start_a) * 1000, 5)} ms')
    start_b = perf_counter()
    result_b = problem_b(problem_input)
    end_b = perf_counter()
    print(f'B: {result_b}, time: {round((end_b - start_b) * 1000, 5)} ms')
