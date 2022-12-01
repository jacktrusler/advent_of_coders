import aoc
from collections import deque
from statistics import median


class CorruptionError(Exception):
    score = {None: 0, ')': 3, ']': 57, '}': 1197, '>': 25137}
    def __init__(self, corruption=None):
        super().__init__('')
        self.score = CorruptionError.score[corruption]

class Chunk:
    openers = ['(', '[', '{', '<']
    close_map = {'(': ')', '[': ']', '{': '}', '<': '>'}
    close_score = {')': 1, ']': 2, '}': 3, '>': 4}

    def __init__(self, chunk: deque[str]):
        self.chunks: list[Chunk] = []
        self.opener = self.closer = None

        while (chunk):
            next_char = chunk[0]
            if not self.opener:
                self.opener = chunk.popleft()
            elif Chunk.close_map[self.opener] == next_char:
                self.closer = chunk.popleft()
                break
            elif next_char in Chunk.openers:
                self.chunks.append(Chunk(chunk))
            else:
                raise CorruptionError(chunk.popleft())

    def closed(self) -> bool:
        return self.closer is not None and all([x.closed() for x in self.chunks])

    def close(self) -> int:
        if self.closed():
            return 0

        self.closer = Chunk.close_map[self.opener]
        if not self.chunks:
            return Chunk.close_score[self.closer]
        return 5 * self.chunks[-1].close() + Chunk.close_score[self.closer]

class Sequence:
    def __init__(self, _str: str):
        self.chunks: list[Chunk] = []
        self.corruption = 0

        queue = deque(list(_str))
        while queue:
            try:
                self.chunks.append(Chunk(queue))
            except CorruptionError as e:
                self.corruption = e.score
                break

    def close(self) -> int:
        if self.corruption > 0:
            return 0
        return self.chunks[-1].close()


@aoc.register(__file__)
def answers():
    sequences = [Sequence(line) for line in aoc.read_lines()]
    yield sum(x.corruption for x in sequences)
    yield median(filter(lambda x: x != 0, (x.close() for x in sequences)))

if __name__ == '__main__':
    aoc.run()
