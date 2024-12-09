package main

import (
	"fmt"
	"goutils"
	"strings"
)

var (
	// This is like pokemon ice cave low key
	ice       []string
	loop      int
	rockLoops int
)

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
		thisStr[x] = 'X'
		ice[y] = string(thisStr)
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

func dropRock(y, x int) {
	// out of bounds, therefore no rock dropped
	if x == -1 || y == -1 || y >= len(ice) || x >= len(ice[y]) {
		return
	}
	// for every step, drop a rock in front of the guard
	thisStr := []rune(ice[y])
	thisStr[x] = '0'
	ice[y] = string(thisStr)
	return
}

func day6part1() {
	for y, line := range ice {
		for x, rune := range line {
			if rune == '^' {
				guardStep(y, x, 'N')
			}
		}
	}

	// Print it out for fun :>
	for _, line := range ice {
		fmt.Println(line)
	}

	// count where guard step occurred
	path := 0
	for _, line := range ice {
		for _, rune := range line {
			if rune == 'X' {
				path++
			}
		}
	}

	fmt.Println(path)

}

func day6part2() {
	for y, line := range ice {
		for x, rune := range line {
			if rune == '^' {
				// not the foggiest idea how to do this
				guardStep(y, x, 'N')
			}
		}
	}

	fmt.Println(rockLoops)

}

func Day6() {
	input := goutils.FileAsString("./input/06-example.txt")
	ice = strings.Split(input, "\n")
	fmt.Println("----- Part 1 -----")
	// day6part1()
	fmt.Println("----- Part 2 -----")
	day6part2()
}
