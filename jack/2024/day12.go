package main

import (
	"fmt"
	u "goutils"
	"strings"
)

var (
	garden []string
)

func day12part1() {
	plantSet := u.NewSet[byte]()
	for _, line := range garden {
		for _, plant := range line {
			plantSet.Add(byte(plant))
		}
	}

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
	fmt.Println(total)
}

func counter(y, x int, garden []string, visited map[u.Coord]bool, target byte) int {
	start := u.Coord{Y: y, X: x}
	rows := len(garden)    // y
	cols := len(garden[0]) // x
	queue := []u.Coord{start}

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
					queue = append(queue, u.Coord{Y: newY, X: newX})
				}
			}
		}
		perimeter += 4 - surroundingPlants
	}
	return perimeter * area
}

func day12part2() {
	fmt.Println(u.Dirs)
}

func Day12() {
	input := u.FileAsString("./input/2024-12-input.txt")
	garden = strings.Split(input, "\n")
	fmt.Println("----- Part 1 -----")
	day12part1()
	fmt.Println("----- Part 2 -----")
	// day12part2()
}
