from __future__ import annotations
import aoc
from collections import Counter
from enum import Enum, auto


class Position(Enum):
    TOP = auto()
    TOP_RIGHT = auto()
    BOT_RIGHT = auto()
    BOTTOM = auto()
    BOT_LEFT = auto()
    TOP_LEFT = auto()
    MIDDLE = auto()

class Display:
    def __init__(self, patterns: list[str], output: list[str]):
        self.positions = self._determine_pos(patterns)
        self.output = output

    def count_output_segments(self) -> dict[int,int]:
        return Counter([len(x) for x in self.output])

    @staticmethod
    def _determine_pos(inputs: list[str]) -> dict[Position, str]:
        inputs = list(map(set, sorted(inputs, key=len)))

        (top,) = inputs[1] - inputs[0]   # The two shortest are 1 and 7
        mid_tLeft = inputs[2] - inputs[0]   # The diff between 1 and 4
        mid_bot = (inputs[3] & inputs[4] & inputs[5]) - set(top)   # Top, middle, bottom are common between 2, 3, and 5
        (mid,) = mid_tLeft & mid_bot
        (tLeft,) = mid_tLeft - set(mid)
        (bot,) = mid_bot - set(mid)
        five = [x for x in inputs[3:6] if tLeft in x][0]   # Five is only of 2, 3, 5 with the top left
        (bRight,) = five - {top, tLeft, mid, bot}
        (tRight,) = inputs[0] - set(bRight)
        (bLeft,) = inputs[-1] - {top, tLeft, mid, bot, bRight, tRight}

        return {
            Position.TOP: top,
            Position.TOP_RIGHT: tRight,
            Position.BOT_RIGHT: bRight,
            Position.BOTTOM: bot,
            Position.BOT_LEFT: bLeft,
            Position.TOP_LEFT: tLeft,
            Position.MIDDLE: mid
        }

    def _determine_digit(self, output: str) -> int:
        match len(output):
            case 2: return 1
            case 3: return 7
            case 4: return 4
            case 5:
                if self.positions[Position.TOP_LEFT] in output: return 5
                if self.positions[Position.BOT_LEFT] in output: return 2
                return 3
            case 6:
                if self.positions[Position.MIDDLE] not in output: return 0
                if self.positions[Position.BOT_LEFT] in output: return 6
                return 9
            case _: return 8

    def display_value(self) -> int:
        digits = [str(self._determine_digit(x)) for x in self.output]
        return int(''.join(digits))

    @staticmethod
    def from_string(display_str: str) -> Display:
        patterns, output = map(str.split, map(str.strip, display_str.split('|')))
        return Display(patterns, output)


@aoc.register(__file__)
def answers():
    displays = [Display.from_string(line) for line in aoc.read_lines()]

    count = sum((disp.count_output_segments() for disp in displays), Counter())
    yield count[2] + count[3] + count[4] + count[7]
    yield sum(disp.display_value() for disp in displays)

if __name__ == '__main__':
    aoc.run()
