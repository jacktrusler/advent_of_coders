package main

import (
	"aoc2015/pkg/utils"
	"fmt"
	"strconv"
)

func Day3() {
	fileAsString := utils.FileAsString("./data/day3.txt")
	xIndex, yIndex := 0, 0

	// Part 1
	mapCache := make(map[string]int, 100)
	// Add 1 present at starting location
	mapCache["0 0"] = 1

	for _, v := range fileAsString {
		switch v {
		case '>':
			xIndex++
		case '<':
			xIndex--
		case '^':
			yIndex++
		case 'v':
			yIndex--
		}

		x := strconv.Itoa(xIndex)
		y := strconv.Itoa(yIndex)

		mapCache[x+" "+y] += 1
	}

	fmt.Printf("houses visited: %d\n", len(mapCache))

	// Part 2
	roboCache := make(map[string]int, 100)
	// Add 2 presents at starting location
	roboCache["0 0"] = 2

	santaX, santaY := 0, 0
	roboX, roboY := 0, 0
	for pos, v := range fileAsString {
		if pos%2 == 0 {
			switch v {
			case '>':
				roboX++
			case '<':
				roboX--
			case '^':
				roboY++
			case 'v':
				roboY--
			}
			x := strconv.Itoa(roboX)
			y := strconv.Itoa(roboY)

			roboCache[x+" "+y] += 1
		} else {
			switch v {
			case '>':
				santaX++
			case '<':
				santaX--
			case '^':
				santaY++
			case 'v':
				santaY--
			}
			x := strconv.Itoa(santaX)
			y := strconv.Itoa(santaY)

			roboCache[x+" "+y] += 1
		}
	}
	fmt.Printf("houses visited: %d\n", len(roboCache))
}
