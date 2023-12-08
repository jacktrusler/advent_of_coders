from pathlib import Path
import utils


class Map:
    def __init__(self, ranges: list[tuple[int, int, int]]) -> None:
        self.ranges = ranges
    
    def map(self, value: int) -> int:
        for dest, source, length in self.ranges:
            if source <= value <= source + length:
                return value + dest - source
        return value
    
    def reverse(self, value: int) -> int:
        for source, dest, length in self.ranges:
            if source <= value <= source + length:
                return value + dest - source
        return value

def apply_maps(seed: int, maps: list[Map]):
    for map in maps:
        seed = map.map(seed)
    return seed

def solve(raw_input: str):
    maps = list()
    chunks = raw_input.split("\n\n")
    seeds = [int(x) for x in chunks[0][7:].split()]

    # Create seed maps
    for chunk in chunks[1:]:
        _, map_text = chunk.split(":")
        ranges = [[int(x) for x in line.split()] for line in map_text.strip().split("\n")]
        maps.append(Map(ranges))

    # Apply to seed list for A
    a = min([apply_maps(seed, maps) for seed in seeds])

    # Determine relevant seed indices for B
    check_indices = set()
    for map in reversed(maps):
        map_indices = set()
        for range in map.ranges:
            # add indices at the borders of stuff happening, might be overkill idk
            map_indices.add(range[0])
            map_indices.add(range[0] + range[2])
            map_indices.add(range[1] + range[2])
        for i in check_indices:
            # convert exising indices to coordinates on the new earlier map.
            map_indices.add(map.reverse(i))
        check_indices = map_indices

    # Find the list of seed indices that intersect with the relevant indices.
    b_seeds = list()
    iter_seeds = iter(seeds)
    while True:
        try:
            seed_start, seed_length = next(iter_seeds), next(iter_seeds)
        except StopIteration:
            break
        for location in check_indices | {seed_start, seed_start+seed_length-1}:
            if seed_start <= location < seed_start + seed_length:
                # only check the seeds at the important locations
                b_seeds.append(location)

    # Apply the seed list for B
    b = min([apply_maps(seed, maps) for seed in b_seeds])
    return a, b

if __name__ == '__main__':
    input_path = Path(__file__).parent / "input" / "05.txt"
    utils.report(*utils.run_solution(solve, input_path))
