package main

import (
	"fmt"
	"goutils"
	"math"
	"strings"
)

var (
	city []string
	// antennae mapping
	aM = make(AntennaMap)
	// part 2 antenna are also antinodes ig
	antiNodes2 = make(map[Coord]bool)
)

type Coord struct {
	y int
	x int
}

type AntennaMap map[rune][]Coord

func day8part1() {
	for y, line := range city {
		for x, rune := range line {
			// some antennae found
			if rune != '.' {
				aM[rune] = append(aM[rune], Coord{y, x})
				antiNodes2[Coord{y, x}] = true
			}
		}
	}

	antiNodeMap := make(map[Coord]bool)
	for _, v := range aM {
		for i := 0; i < len(v); i++ {
			for j := i + 1; j < len(v); j++ {
				var a1, a2 Coord
				a1.x, a1.y = v[i].x, v[i].y
				a2.x, a2.y = v[j].x, v[j].y
				dy := int(math.Abs(float64(a1.y - a2.y)))
				dx := int(math.Abs(float64(a1.x - a2.x)))

				if a1.x < a2.x {
					dx = dx * -1
				}
				if a1.y < a2.y {
					dy = dy * -1
				}
				createAntiNodes(a1, dy, dx, antiNodeMap, 1)
				createAntiNodes(a2, -dy, -dx, antiNodeMap, 1)
			}
		}
	}

	fmt.Println(len(antiNodeMap))

}

func createAntiNodes(a Coord, dy, dx int, aNM map[Coord]bool, part int) {
	anti := Coord{}
	anti.x = a.x + dx
	anti.y = a.y + dy
	// exit condition
	if anti.x < 0 || anti.y < 0 || anti.x >= len(city[0]) || anti.y >= len(city) {
		return
	}
	aNM[anti] = true
	if part == 2 {
		createAntiNodes(anti, dy, dx, aNM, 2)
	}
}

func day8part2() {
	for _, v := range aM {
		for i := 0; i < len(v); i++ {
			for j := i + 1; j < len(v); j++ {
				var a1, a2 Coord
				a1.x, a1.y = v[i].x, v[i].y
				a2.x, a2.y = v[j].x, v[j].y
				dy := int(math.Abs(float64(a1.y - a2.y)))
				dx := int(math.Abs(float64(a1.x - a2.x)))

				if a1.y < a2.y {
					dy = dy * -1
				}
				if a1.x < a2.x {
					dx = dx * -1
				}
				createAntiNodes(a1, dy, dx, antiNodes2, 2)
				createAntiNodes(a2, -dy, -dx, antiNodes2, 2)
			}
		}
	}
	fmt.Println(len(antiNodes2))
}

func Day8() {
	input := goutils.FileAsString("./input/2024-08-input.txt")
	city = strings.Split(input, "\n")
	fmt.Println("----- Part 1 -----")
	day8part1()
	fmt.Println("----- Part 2 -----")
	day8part2()
}
