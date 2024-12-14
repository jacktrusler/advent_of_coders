package main

import (
	"fmt"
	u "goutils"
	"slices"
	"strings"
)

var (
	garden   []string
	plantSet u.Set[byte]
	plots    = make(map[byte][][]u.Coord)
)

func counter(y, x int, garden []string, visited map[u.Coord]bool, target byte) int {
	start := u.Coord{Y: y, X: x}
	rows := len(garden)    // y
	cols := len(garden[0]) // x
	queue := []u.Coord{start}

	plantLoc := []u.Coord{}
	plantLoc = append(plantLoc, start)

	perimeter := 0
	area := 0

	for len(queue) > 0 {
		current := queue[0]
		queue = queue[1:]
		curr := u.Coord{Y: current.Y, X: current.X}
		if visited[curr] {
			continue
		} else {
			visited[curr] = true
		}
		area++

		// find perimeter of current plant
		// and move to surrounding plants
		surroundingPlants := 0
		for _, dir := range u.Dirs {
			newY, newX := current.Y+dir[0], current.X+dir[1]
			if newY >= 0 && newY < rows && newX >= 0 && newX < cols && garden[newY][newX] == target {
				surroundingPlants++
				if !visited[u.Coord{Y: newY, X: newX}] {
					newCoord := u.Coord{Y: newY, X: newX}
					queue = append(queue, u.Coord{Y: newY, X: newX})
					if !slices.Contains(plantLoc, newCoord) {
						plantLoc = append(plantLoc, u.Coord{Y: newY, X: newX})
					}
				}
			}
		}
		perimeter += 4 - surroundingPlants
	}
	plots[target] = append(plots[target], plantLoc)
	fmt.Printf("%+v\n\n", plantLoc)
	return perimeter * area
}

func makePlantSet(garden []string) u.Set[byte] {
	plantSet = u.NewSet[byte]()
	for _, line := range garden {
		for _, plant := range line {
			plantSet.Add(byte(plant))
		}
	}
	return plantSet
}

func day12part1() {
	plantSet := makePlantSet(garden)

	visited := make(map[u.Coord]bool)

	total := 0
	for plant := range plantSet {
		for y, line := range garden {
			for x, p := range line {
				if byte(p) == plant && !visited[u.Coord{Y: y, X: x}] {
					ans := counter(y, x, garden, visited, byte(p))
					total += ans
				}
			}
		}
	}
	fmt.Printf("%+v\n", plots)
}

func calcArea(arr []u.Coord, p byte) int {
	rows := len(garden)    // y
	cols := len(garden[0]) // x
	dirMap := make(map[string]u.Set[u.Coord])

	if dirMap["North"] == nil {
		dirMap["North"] = make(u.Set[u.Coord])
	}
	if dirMap["East"] == nil {
		dirMap["East"] = make(u.Set[u.Coord])
	}
	if dirMap["South"] == nil {
		dirMap["South"] = make(u.Set[u.Coord])
	}
	if dirMap["West"] == nil {
		dirMap["West"] = make(u.Set[u.Coord])
	}

	for _, coord := range arr {
		for i, dir := range u.Dirs {
			newY, newX := coord.Y+dir[0], coord.X+dir[1]
			if newY < 0 || newY >= rows || newX < 0 || newX >= cols || garden[newY][newX] != p {
				// N
				if i == 0 && (newY < 0 || garden[newY][coord.X] != p) {
					dirMap["North"][coord] = true
				}
				if i == 1 && (newX >= cols || garden[coord.Y][newX] != p) {
					dirMap["East"][coord] = true
				}
				if i == 2 && (newY >= rows || garden[newY][coord.X] != p) {
					dirMap["South"][coord] = true
				}
				if i == 3 && (newX < 0 || garden[coord.Y][newX] != p) {
					dirMap["West"][coord] = true
				}
			}
		}
	}

	sides := 0
	for dir, v := range dirMap {
		// the band
		oneDirection := make([]u.Coord, 0)
		for k2 := range v {
			oneDirection = append(oneDirection, k2)
		}

		if dir == "North" || dir == "South" {
			// North / South Sort
			slices.SortFunc(oneDirection, func(a, b u.Coord) int {
				if a.Y == b.Y {
					return a.X - b.X
				}
				return a.Y - b.Y
			})

			y := -1
			prevX := -1
			for _, coord := range oneDirection {
				if prevX == -1 {
					prevX = coord.X
				}
				if coord.Y != y {
					y = coord.Y
					sides++
					prevX = coord.X
					continue
				}

				if coord.X-prevX > 1 {
					sides++
				}
				prevX = coord.X

			}
		} else {
			// East / West Sort
			slices.SortFunc(oneDirection, func(a, b u.Coord) int {
				if a.X == b.X {
					return a.Y - b.Y
				}
				return a.X - b.X
			})

			x := -1
			prevY := -1
			for _, coord := range oneDirection {
				if prevY == -1 {
					prevY = coord.Y
				}
				if coord.X != x {
					x = coord.X
					sides++
					prevY = coord.Y
					continue
				}

				if coord.Y-prevY > 1 {
					sides++
				}
				prevY = coord.Y

			}
		}
	}
	// len(arr) is total squares a.k.a. area
	return sides * len(arr)
}

// find edges
func day12part2() {
	plantSet := makePlantSet(garden)
	total2 := 0
	for plant := range plantSet {
		// put perimeters into map
		// if out of bounds or doesn't match target... must be a side
		for _, plot := range plots[plant] {
			total2 += calcArea(plot, plant)
		}
	}
	fmt.Println(total2)
}

func Day12() {
	input := u.FileAsString("./input/2024-12-input.txt")
	garden = strings.Split(input, "\n")
	fmt.Println("----- Part 1 -----")
	day12part1()
	fmt.Println("----- Part 2 -----")
	day12part2()
}
