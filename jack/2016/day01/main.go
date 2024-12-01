package main

import (
	"aoc2016/util"
	"fmt"
	"math"
	"strings"
)

func newDirection(i int, turn string) (int, string) {
	directions := []string{"N", "E", "S", "W"}
	switch turn {
	case "R":
		if i == 3 {
			i = 0
		} else {
			i += 1
		}
	case "L":
		if i == 0 {
			i = 3
		} else {
			i -= 1
		}
	}

	return i, directions[i]
}

func checkCache(cache map[string]bool, part2 *string, amt, x, y int) {
	key := fmt.Sprintf("x%dy%d", x, y)
	if cache[key] && *part2 == "" {
		*part2 = key
	} else {
		cache[key] = true
	}
}

func main() {
	str := util.FileAsString("./input.txt")
	dirs := strings.Split(str, ", ")

	// Current direction
	current := 0
	dir := "N"
	var turn, part2 string
	var x, y, amt int

	// part 2: create a cache
	type Cache map[string]bool
	cache := make(Cache)

	for _, step := range dirs {
		fmt.Sscanf(step, "%1s%d", &turn, &amt)
		current, dir = newDirection(current, turn)
		for i := 0; i < amt; i++ {
			switch dir {
			case "N":
				y++
				checkCache(cache, &part2, amt, x, y)
			case "E":
				x++
				checkCache(cache, &part2, amt, x, y)
			case "S":
				y--
				checkCache(cache, &part2, amt, x, y)
			case "W":
				x--
				checkCache(cache, &part2, amt, x, y)
			}
		}

	}
	var part2x, part2y float64
	fmt.Sscanf(part2, "x%fy%f", &part2x, &part2y)

	fmt.Println("-------- Part 1 ----------")
	fmt.Println(math.Abs(float64(x)) + math.Abs(float64(y)))
	fmt.Println("-------- Part 2 ----------")
	fmt.Println(math.Abs(part2x) + math.Abs(part2y))
}
