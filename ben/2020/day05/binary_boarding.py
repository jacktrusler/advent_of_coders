import aoc
import numpy as np


def parse_seat(seat: str) -> tuple[int, int]:
    row = seat[:-3].replace('F', '0').replace('B', '1')
    col = seat[-3:].replace('L', '0').replace('R', '1')
    return int(row, base=2), int(col, base=2)

def seat_id(row, col) -> int:
    return row * 8 + col


@aoc.register(__file__)
def answers():
    seats = np.array([parse_seat(line) for line in aoc.read_lines()])
    seats = np.column_stack((seats, seat_id(seats[:,0], seats[:,1])))
    max_seat_id = max(seats[:,2])
    yield max_seat_id

    seat_ids = set(seats[:,2])
    missing = set(range(max_seat_id)) - seat_ids
    missing = [x for x in missing if {x-1, x+1} <= seat_ids][0]
    yield missing

if __name__ == '__main__':
    aoc.run()
