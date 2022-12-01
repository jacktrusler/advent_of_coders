from __future__ import annotations
import numpy as np
from numpy.typing import NDArray
import regex

try:
    from location import Location, Direction
except ImportError:
    from .location import Location, Direction


#--------------------------#
#                          #
#                     #    #
#   #    ##    ##    ###   #
#    #  #  #  #  #  #      #
#                          #
#--------------------------#
class SeaMonster:
    relative_locs = [
        Location(18, 0), Location(0, 1), Location(5, 1), Location(6, 1), Location(11, 1),
        Location(12, 1), Location(17, 1), Location(18, 1), Location(19, 1), Location(1, 2),
        Location(4, 2), Location(7, 2), Location (10, 2), Location(13, 2), Location(16, 2)
    ]

    def __init__(self, start: Location):
        self.start = start
        self.points = {start + loc for loc in SeaMonster.relative_locs}
        
    @staticmethod
    def regex(width: int) -> str:
        retval = rf'.{{{18}}}#{{{1}}}.{{{1}}}[\S\s]{{{width + 1 - 20}}}'
        retval += rf'#{{{1}}}.{{{4}}}#{{{2}}}.{{{4}}}#{{{2}}}.{{{4}}}#{{{3}}}[\S\s]{{{width + 1 - 20}}}'
        retval += rf'.{{{1}}}#{{{1}}}.{{{2}}}#{{{1}}}.{{{2}}}#{{{1}}}.{{{2}}}#{{{1}}}.{{{2}}}#{{{1}}}.{{{2}}}#{{{1}}}.{{{3}}}'
        return retval


class Image:
    def __init__(self, content: NDArray):
        self._content: NDArray = content

    def __str__(self):
        return '\n'.join([''.join([char for char in line]) for line in self._content])

    def rotate(self, n: int=1, clockwise=True) -> Image:
        return Image(np.rot90(self._content, k=-1*n if clockwise else 1*n))
        
    def flip(self) -> Image:
        return Image(np.flip(self._content, axis=1))

    def count_hash(self) -> int:
        return np.count_nonzero(self._content == '#')

    def sea_monsters(self) -> list[SeaMonster]:
        width = self._content.shape[1]
        def find_monsters(image: Image) -> list[SeaMonster]:
            monsters = []
            for match in regex.finditer(SeaMonster.regex(width), str(image), overlapped=True):
                idx = match.start()
                start = Location(x=idx % (width + 1), y=idx // (width + 1))
                monsters.append(SeaMonster(start))
            return monsters

        _image = self
        for _ in range(2):
            for _ in Direction:
                if monsters := find_monsters(_image):
                    return monsters
                _image = self.rotate(1)
            _image = self.flip()
        