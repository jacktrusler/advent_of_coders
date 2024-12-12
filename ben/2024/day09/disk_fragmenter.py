import aoc
from collections import deque
from typing import Iterator


Node = tuple[int, int, int]

def parse_disk(disk_map: str) -> Iterator[Node]:
    index, id = 0, 0
    for i, block in enumerate(disk_map):
        length = int(block)
        if i % 2 == 0:
            yield (index, length, id)
            id += 1
        else:
            yield (index, length, -1)
        index += length

def compact(disk: list[Node]) -> Iterator[Node]:
    queue = deque(disk)
    front_idx, front_len, front_val = queue.popleft()
    back_idx, back_len, back_val = queue.pop()

    while queue and front_idx < back_idx:
        if front_val != -1:
            yield front_idx, front_len, front_val
        if front_len == 0 or front_val != -1:
            front_idx, front_len, front_val = queue.popleft()
            continue
        if back_len == 0 or back_val == -1:
            back_idx, back_len, back_val = queue.pop()
            continue

        write_len = min(front_len, back_len)
        yield front_idx, write_len, back_val

        front_idx += write_len
        front_len -= write_len
        back_len -= write_len
    yield front_idx, back_len, back_val

def defragment(disk: list[Node]) -> Iterator[Node]:
    occupied = [x for x in disk if x[2] != -1]
    empty = [x for x in disk if x[2] == -1]

    def __first_empty_block(occ: Node) -> int:
        for i, empty_block in enumerate(empty):
            if empty_block[0] > occ[0]:
                return -1
            if empty_block[1] >= occ[1]:
                return i
        return -1
    
    for occupied_block in reversed(occupied):
        if (target_idx := __first_empty_block(occupied_block)) == -1:
            yield occupied_block
            continue

        _, occ_len, occ_val = occupied_block
        empty_idx, empty_len, _ = empty[target_idx]
        yield (empty_idx, occ_len, occ_val)

        if occ_len == empty_len:
            empty.pop(target_idx)
        else:
            empty[target_idx] = (empty_idx + occ_len, empty_len - occ_len, -1)

def checksum(node: Node) -> int:
    return (node[0] * node[1] + sum(range(node[1]))) * node[2]

@aoc.register(__file__)
def answers():
    disk_map = tuple(x for x in parse_disk(aoc.read_data()))
    yield sum(checksum(b) for b in compact(disk_map))
    yield sum(checksum(b) for b in defragment(disk_map))

if __name__ == '__main__':
    aoc.run()