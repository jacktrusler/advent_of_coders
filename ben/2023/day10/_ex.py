"""
Advent of Code 2023
Day 10: Pipe Maze

Daniel Herding
"""

from enum import Enum
import re
import urllib.request

class Dir(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class PipeWalker:
    """
    Follows a path from the start position, and marks its way with pipe characters.
    """
    def __init__(self, maze):
        self.maze = maze
        # The maze width, including the newline
        self._width = self.maze.index("\n") + 1
        self._height = self.maze.count("\n")
        
        self.currentIndex = self.maze.index("S")
        # Whether we have made it back to the start position
        self._hasArrived = False
        self._currentDir = None
        self._replaceStart()
        
    def _replaceStart(self):
        # Check whether adjacent tiles connect to the start position.
        connectsUp = self.currentIndex // self._width > 0 and self.maze[self.currentIndex - self._width] in ("|", "F", "7")
        connectsRight = self.currentIndex % self._width < self._width -1 and self.maze[self.currentIndex + 1] in ("-", "7", "J")
        connectsDown = self.currentIndex // self._width < self._height and self.maze[self.currentIndex + self._width] in ("|", "J", "L")
        connectsLeft = self.currentIndex % self._width > 0 and self.maze[self.currentIndex - 1] in ("-", "L", "F")
        
        # Replace the S character with a pipe that fits.
        if connectsUp:
            self._currentDir = Dir.UP
            if connectsRight:
                self._replaceCurrentTile("╚")
            elif connectsDown:
                self._replaceCurrentTile("║")
            elif connectsLeft:
                self._replaceCurrentTile("╝")
        elif connectsRight:
            self._currentDir = Dir.RIGHT
            if connectsDown:            
                self._replaceCurrentTile("╔")
            elif connectsLeft:            
                self._replaceCurrentTile("═")
        elif connectsDown and connectsLeft:            
            self._currentDir = Dir.DOWN
            self._replaceCurrentTile("╗")

    def _replaceCurrentTile(self, newTile: str) -> None:
        self.maze = self.maze[:self.currentIndex] + newTile + self.maze[self.currentIndex + 1:]

    def walkThroughMaze(self) -> int:
        stepCount = 0
        while not self._hasArrived:
            self._step()
            stepCount += 1
        return stepCount

    def _step(self) -> None:
        # Move one step in the current direction.
        match(self._currentDir):
            case Dir.UP:
                self.currentIndex -= self._width
            case Dir.RIGHT:
                self.currentIndex += 1
            case Dir.DOWN:
                self.currentIndex += self._width
            case Dir.LEFT:
                self.currentIndex -= 1
        
        # Adjust the direction, and mark the visited position with a fitting pipe.
        currentTile = self.maze[self.currentIndex]
        match(currentTile):
            case "J":
                self._currentDir = Dir.UP if self._currentDir == Dir.RIGHT else Dir.LEFT
                self._replaceCurrentTile("╝")
            case "F":
                self._currentDir = Dir.RIGHT if self._currentDir == Dir.UP else Dir.DOWN
                self._replaceCurrentTile("╔")
            case "7":
                self._currentDir = Dir.DOWN if self._currentDir == Dir.RIGHT else Dir.LEFT
                self._replaceCurrentTile("╗")
            case "L":
                self._currentDir = Dir.UP if self._currentDir == Dir.LEFT else Dir.RIGHT
                self._replaceCurrentTile("╚")
            case "|":
                self._currentDir = Dir.UP if self._currentDir == Dir.UP else Dir.DOWN
                self._replaceCurrentTile("║")
            case "-":
                self._currentDir = Dir.RIGHT if self._currentDir == Dir.RIGHT else Dir.LEFT
                self._replaceCurrentTile("═")
            case _:
                self._hasArrived = True

class NestFinder:
    RE_VERTICAL_BORDER = re.compile("╚═*╗|╔═*╝|║")

    def __init__(self, maze):
        self.maze = maze

    def countNestSpots(self):
        nestSpotCount = 0
        for line in self.maze.split("\n"):
            for column, c in enumerate(line):
                if c not in "╚╗╔╝═║":
                    matches = self.RE_VERTICAL_BORDER.findall(line[:column])
                    # The spot is inside the polygon if a beam coming from the left crosses an odd number of pipes.
                    if len(matches) % 2 == 1:
                        nestSpotCount += 1
        return nestSpotCount

with open("2023/day10/large.txt") as f:
    input = f.read()
    walker = PipeWalker(input)
    stepCount = walker.walkThroughMaze()

    print(walker.maze + "\n")
    print(f"Part 1: {stepCount // 2}")

    finder = NestFinder(walker.maze)
    nestSpots = finder.countNestSpots()
    print(f"Part 2: {nestSpots}")