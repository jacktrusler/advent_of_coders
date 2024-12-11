def solve(puzzle_input: str):
    disk_map = [int(x) for x in puzzle_input]
    a = solve_a(disk_map)
    b = solve_b(disk_map)
    return a, b

def solve_a(disk_map):
    files = [x for x in disk_map[::2]]
    blocks_from_end = iter_blocks_from_end(files)
    max_block_position = sum(files)
    isfile = True
    checksum = 0
    block_position = 0
    file_id = 0
    for x in disk_map:
        if isfile:
            for _ in range(x):
                checksum += block_position * file_id
                block_position += 1
                if block_position >= max_block_position:
                    break
            file_id += 1
        else:
            for _ in range(x):
                checksum += block_position * next(blocks_from_end)
                block_position += 1
                if block_position >= max_block_position:
                    break
        if block_position >= max_block_position:
            break
        isfile = not isfile
    return checksum

def solve_b(disk_map):
    files, spaces = parse_disk_map(disk_map)
    output_files = list()
    for file_id, file_block, file_size in reversed(files):
        for i, (space_block, space_size) in enumerate(spaces):
            if space_block > file_block:
                break
            if file_size == space_size:
                file_block = space_block
                spaces.pop(i)
            elif file_size < space_size:
                file_block = space_block
                spaces[i] = (space_block + file_size, space_size - file_size)
        output_files.append((file_id, file_block, file_size))
    checksum = 0
    for file_id, file_block, file_size in output_files:
        for i in range(file_block, file_block + file_size):
            checksum += file_id * i
    return checksum

def parse_disk_map(disk_map) -> tuple[list]:
    files = []
    spaces = []
    isfile = True
    block = 0
    file_id = 0
    for x in disk_map:
        if isfile:
            files.append((file_id, block, x))
            file_id += 1
        else:
            if x > 0:
                spaces.append((block, x))
        isfile = not isfile
        block += x
    return files, spaces

def iter_blocks_from_end(files: list[int]):
    file_id = len(files) - 1
    for file in files[::-1]:
        for _ in range(file):
            yield file_id
        file_id -= 1

if __name__ == '__main__':
    from pathlib import Path
    import aoc_util
    input_path = Path(__file__).parent / "input" / "09.txt"
    aoc_util.report(*aoc_util.run_solution(solve, input_path))
