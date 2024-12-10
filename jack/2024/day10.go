package main

import (
	"fmt"
	"goutils"
	"strings"
)

var (
	topog    [][]int
	findable map[Coord]int
)

func makeTrail(input string) {
	mapStr := strings.Split(input, "\n")
	for _, str := range mapStr {
		runes := strings.Split(str, "")
		thing, err := goutils.StringArrAtoI(runes)
		if err != nil {
			fmt.Printf("error converting: %v", err)
		}
		topog = append(topog, thing)
	}
}

func hike(y, x, past int, paths map[Coord]int) {
	// if out of bounds
	if x == -1 || y == -1 || y >= len(topog) || x >= len(topog[y]) {
		return
	}
	curr := topog[y][x]
	// if lower or equal
	if curr <= past {
		return
	}
	// if more than 2 steps down
	if curr > past+1 {
		return
	}

	if curr == 9 {
		findable[Coord{y, x}]++
		paths[Coord{y, x}]++
		return
	}
	//N
	hike(y-1, x, curr, paths)
	//E
	hike(y, x+1, curr, paths)
	//S
	hike(y+1, x, curr, paths)
	//W
	hike(y, x-1, curr, paths)
	return
}

func day10part1and2() {
	findable = make(map[Coord]int)
	ans1 := 0
	for y, line := range topog {
		for x, h := range line {
			if h == 0 {
				paths := make(map[Coord]int)
				//N
				hike(y-1, x, h, paths)
				//E
				hike(y, x+1, h, paths)
				//S
				hike(y+1, x, h, paths)
				//W
				hike(y, x-1, h, paths)

				ans1 += len(paths)
			}
		}
	}
	total := 0
	for _, v := range findable {
		total += v
	}
	fmt.Println(ans1)
	fmt.Println("----- Part 2 -----")
	fmt.Println(total)

}

func Day10() {
	input := goutils.FileAsString("./input/2024-10-input.txt")
	makeTrail(input)
	fmt.Println("----- Part 1 -----")
	day10part1and2()
}
