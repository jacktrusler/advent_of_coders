package main

import (
	"fmt"
	"os"
	"strings"
	"time"
)

type Point struct {
	x int
	y int
}

func preprocessInput(raw []byte) (map[rune][]Point, Point) {
	split := strings.Split(string(raw), "\r\n")
	antennas := make(map[rune][]Point)
	maxPosition := Point{x: len(split[0]), y: len(split)}
	for rIdx, row := range split {
		for cIdx, cell := range row {
			if cell == '.' {
				continue
			}
			coordinate := Point{x: cIdx, y: rIdx}
			antennaList := antennas[cell]
			if antennaList == nil {
				antennaList = []Point{coordinate}
			} else {
				antennaList = append(antennaList, coordinate)
			}
			antennas[cell] = antennaList
		}
	}
	return antennas, maxPosition
}
func calculateSlope(p1 Point, p2 Point) (int, int) {
	rise := p2.y - p1.y
	run := p2.x - p1.x
	return max(run, -run), max(rise, -rise)
}

func e1(antennas map[rune][]Point, boundary Point) int {
	calculateAntinodes := func(p1 Point, p2 Point) (Point, Point) {
		dx, dy := calculateSlope(p1, p2)
		var an1x, an1y, an2x, an2y int
		if p1.x < p2.x {
			an1x = p1.x - dx
			an2x = p2.x + dx
		} else {
			an1x = p1.x + dx
			an2x = p2.x - dx
		}
		if p1.y < p2.y {
			an1y = p1.y - dy
			an2y = p2.y + dy
		} else {
			an1y = p1.y + dy
			an2y = p2.y - dy
		}
		return Point{x: an1x, y: an1y}, Point{x: an2x, y: an2y}
	}
	antiNodes := make(map[Point]bool)
	for freq, antennaList := range antennas {
		if freq == '#' {
			continue
		}
		for a1Iter := 0; a1Iter < len(antennaList)-1; a1Iter++ {
			for a2Iter := a1Iter + 1; a2Iter < len(antennaList); a2Iter++ {
				anti1, anti2 := calculateAntinodes(antennaList[a1Iter], antennaList[a2Iter])
				if anti1.x >= 0 && anti1.y >= 0 && anti1.x < boundary.x && anti1.y < boundary.y {
					antiNodes[anti1] = true
				}
				if anti2.x >= 0 && anti2.y >= 0 && anti2.x < boundary.x && anti2.y < boundary.y {
					antiNodes[anti2] = true
				}
			}
		}
	}
	return len(antiNodes)
}
func e2(antennas map[rune][]Point, boundary Point) int {
	total := 0
	antiNodes := make(map[Point]bool)
	oob := func(p, b Point) bool {
		return !(p.x >= 0 && p.y >= 0 && p.x < b.x && p.y < b.y)
	}
	calculateAntinodes := func(p1, p2 Point) {
		dx, dy := calculateSlope(p1, p2)
		antiNodes[p1] = true
		antiNodes[p2] = true
		curAn1 := p1
		curAn2 := p2
		ascX := false
		ascY := false
		if p1.x < p2.x {
			ascX = true
		}
		if p1.y < p2.y {
			ascY = true
		}
		for !oob(curAn1, boundary) || !oob(curAn2, boundary) {
			an1 := Point{}
			an2 := Point{}
			if ascX {
				an1.x = curAn1.x - dx
				an2.x = curAn2.x + dx
			} else {
				an1.x = curAn1.x + dx
				an2.x = curAn2.x - dx
			}
			if ascY {
				an1.y = curAn1.y - dy
				an2.y = curAn2.y + dy
			} else {
				an1.y = curAn1.y + dy
				an2.y = curAn2.y - dy
			}
			if !oob(an1, boundary) {
				antiNodes[an1] = true
			}
			if !oob(an2, boundary) {
				antiNodes[an2] = true
			}
			curAn1 = an1
			curAn2 = an2
		}
	}
	for freq, antennaList := range antennas {
		if freq == '#' {
			continue
		}
		for a1Iter := 0; a1Iter < len(antennaList)-1; a1Iter++ {
			for a2Iter := a1Iter + 1; a2Iter < len(antennaList); a2Iter++ {
				calculateAntinodes(antennaList[a1Iter], antennaList[a2Iter])
			}
		}
	}
	total = len(antiNodes)
	return total
}

func main() {
	raw, err := os.ReadFile("input.txt")
	if err != nil {
		panic("Failed to open file ./input.txt")
	}
	antennas, boundary := preprocessInput(raw)
	start := time.Now()
	total := e1(antennas, boundary)
	duration := time.Since(start)
	fmt.Printf("On Exercise 1: %d\t(%s)\n", total, duration)
	start = time.Now()
	total = e2(antennas, boundary)
	duration = time.Since(start)
	fmt.Printf("On Exercise 2: %d\t(%s)\n", total, duration)
}
