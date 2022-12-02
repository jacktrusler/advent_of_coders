from __future__ import annotations
import aoc
import numpy as np
from numpy.typing import NDArray
from typing import Generator


class BingoBoard:
    def __init__(self, values: NDArray):
        self.values = np.array(values)
        self.marks = np.full(self.values.shape, fill_value=False, dtype=bool)
        self._last_num: int = None

    def mark(self, value: int) -> bool:
        self.marks[self.values == value] = True
        self._last_num = value
        return self.bingo()

    def bingo(self) -> bool:
        row_bingo = any([all(row) for row in self.marks])
        col_bingo = any([all(col) for col in self.marks.T])
        return row_bingo or col_bingo

    def score(self) -> int:
        return self.values[self.marks == False].sum() * self._last_num

    @staticmethod
    def from_string(board_str: str) -> BingoBoard:
        ar = np.array([list(map(int, line.split())) for line in board_str.splitlines()])
        return BingoBoard(ar)

def bingos(boards: list[BingoBoard], numbers: list[int]) -> Generator[BingoBoard,None,None]:
    for number in numbers:
        bingos = [b.mark(number) for b in boards]
        yield from (board for board, bingo in zip(boards, bingos) if bingo)
        boards = [board for board, bingo in zip(boards, bingos) if not bingo]
        if not boards:
            return


@aoc.register(__file__)
def answers():
    numbers, *boards = aoc.read_chunks()
    numbers = list(map(int, numbers.split(',')))
    boards = [BingoBoard.from_string(b) for b in boards]
    gen = bingos(boards, numbers)

    first = next(gen)
    yield first.score()

    all_bingos = [board for board in gen]
    yield all_bingos[-1].score()

if __name__ == '__main__':
    aoc.run()
