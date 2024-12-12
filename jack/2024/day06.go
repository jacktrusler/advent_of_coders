package main

import (
	"fmt"
	u "goutils"
	"strings"
)

var (
	// This is like pokemon ice cave low key
	ice         []string
	startPos    u.Coord
	rockSet     u.Set[u.Coord]
	movedSpaces int
)

// Imaginary Rock Cache
type IRC struct {
	Y   int
	X   int
	Dir int
}

// A new genre of music in the AoC-verse
func guardStep(y, x int, dir rune) {
	// out of bounds, therefore finished
	if x == -1 || y == -1 || y >= len(ice) || x >= len(ice[y]) {
		return
	}
	thisStr := []rune(ice[y])
	if thisStr[x] == '#' {
		switch dir {
		// back up a step and change dir
		case 'N':
			dir = 'E'
			guardStep(y+1, x, dir)
		case 'E':
			dir = 'S'
			guardStep(y, x-1, dir)
		case 'S':
			dir = 'W'
			guardStep(y-1, x, dir)
		case 'W':
			dir = 'N'
			guardStep(y, x+1, dir)
		}
		return
	} else {
		// Spot has been moved to
		rockSet.Add(u.Coord{Y: y, X: x})
	}

	switch dir {
	case 'N':
		guardStep(y-1, x, dir)
	case 'E':
		guardStep(y, x+1, dir)
	case 'S':
		guardStep(y+1, x, dir)
	case 'W':
		guardStep(y, x-1, dir)
	}
	return
}

func printIce() {
	// Print it out for fun :>
	for _, line := range ice {
		fmt.Println(line)
	}
}

func day6part1(input string) {
	rockSet = u.NewSet[u.Coord]()
	ice = strings.Split(input, "\n")
	for y, line := range ice {
		for x, rune := range line {
			if rune == '^' {
				startPos = u.Coord{Y: y, X: x}
				guardStep(y, x, 'N')
			}
		}
	}

	fmt.Println(len(rockSet))
}

func isTrapped(y, x, dirI int, iRC u.Coord, hits *[]IRC) bool {
	cache := make(map[string]bool)
	for {
		dy := Dirs[dirI][0]
		dx := Dirs[dirI][1]
		if x+dx < 0 || y+dy < 0 || y+dy >= len(ice) || x+dx >= len(ice[y]) {
			// Freedom
			return false
		}

		hitRock := y+dy == iRC.Y && x+dx == iRC.X
		if ice[y+dy][x+dx] == '#' || hitRock {
			str := fmt.Sprintf("y%dx%ddir%d", y, x, dirI)
			if cache[str] {
				// clapped in the baguss
				*hits = append(*hits, IRC{Y: y + dy, X: x + dx, Dir: dirI})
				return true
			}
			cache[str] = true
			dirI = (dirI + 1) % 4
			continue
		}
		y += dy
		x += dx
	}
}

func day6part2(input string) {
	ice = strings.Split(input, "\n")
	thisStr := []byte(ice[startPos.Y])
	thisStr[startPos.X] = '^'
	ice[startPos.Y] = string(thisStr)
	loops := 0

	hits := make([]IRC, 0)
	for y, line := range ice {
		for x, rune := range line {
			if rune == '^' {
				startY := y
				startX := x
				// Remove starting position from set... Guard will notice!
				rockSet.Remove(u.Coord{Y: startY, X: startX})
				for k := range rockSet {
					imagRock := u.Coord{Y: k.Y, X: k.X}

					inTheClapHouse := isTrapped(startY, startX, 0, imagRock, &hits)

					if inTheClapHouse {
						loops++
					}
				}
			}
		}
	}
	fmt.Println(loops)
}

func Day6() {
	input := u.FileAsString("./input/2024-06-input.txt")
	fmt.Println("----- Part 1 -----")
	day6part1(input)
	fmt.Println("----- Part 2 -----")
	day6part2(input)
}
