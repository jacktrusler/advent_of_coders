import argparse
from typing import List


TOTAL_CYCLES = 1_000_000_000


def main():

    with open("2023/day14/data.txt", "r") as file:
        lines = file.read().splitlines()

    print(f"part 1 solution: {part_one(lines)}")
    print(f"part 2 solution: {part_two(lines)}")


def weigh(platform: List[List[str]]) -> int:
    weight = 0
    row_len = len(platform[0])
    for row in platform:
        for i, char in enumerate(row):
            if char == "O":
                weight += row_len - i
    return weight


def tilt_left(platform: List[List[str]]) -> List[List[str]]:
    for row in platform:
        # O(n) version
        empty_pos = 0
        for i, char in enumerate(row):
            if char == "O":
                row[i] = "."
                row[empty_pos] = "O"
                empty_pos += 1
            elif char == "#":
                empty_pos = i + 1

        # initial O(n^2) version
        # for _ in range(row_len - 1):
        #     for i in range(row_len - 1):
        #         if row[i] == "." and row[i + 1] == "O":
        #             row[i] = "O"
        #             row[i + 1] = "."
    return platform


def rotate(platform: List[List[str]], clockwise: bool = True) -> List[List[str]]:
    if clockwise:
        platform = platform[::-1]
        return [[l[i] for l in platform] for i in range(len(platform[0]))]
    return [[l[i] for l in platform] for i in range(len(platform[0]))][::-1]


def run_cycle(platform: List[List[str]]) -> List[List[str]]:
    for _ in range(4):
        platform = tilt_left(platform)
        platform = rotate(platform)
    return platform


def part_one(lines: List[str]) -> int:
    platform = [list(l) for l in lines]
    platform = rotate(platform, False)
    platform = tilt_left(platform)
    return weigh(platform)


def part_two(lines: List[str]) -> int:
    platform = [list(l) for l in lines]
    platform = rotate(platform, False)  # so north is to the left

    cycles = {}  # str(platform): n_cycles
    n_cycles = 0
    while True:
        platform_str = "".join(["".join(l) for l in platform])
        if platform_str in cycles:
            break

        cycles[platform_str] = n_cycles
        platform = run_cycle(platform)
        n_cycles += 1

    # compute the platform after TOTAL_CYCLES cycles and return weight
    cycle_len = n_cycles - cycles[platform_str]
    cycle_pos = (TOTAL_CYCLES - n_cycles) % cycle_len
    end_ix = n_cycles - cycle_len + cycle_pos
    for platform_str, ix in cycles.items():
        if ix == end_ix:
            break

    n = len(platform)
    m = len(platform[0])
    platform = []
    for i in range(n):
        platform.append(list(platform_str[n * i : n * i + m]))

    return weigh(platform)


if __name__ == "__main__":
    main()