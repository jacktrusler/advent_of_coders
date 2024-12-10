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

func hikeDown(y, x, past int, paths map[Coord]int) {
	// if out of bounds
	if x == -1 || y == -1 || y >= len(topog) || x >= len(topog[y]) {
		return
	}
	curr := topog[y][x]
	// if higher height
	if curr >= past {
		return
	}
	// if more than 2 steps down
	if curr < past-1 {
		return
	}

	if curr == 0 {
		findable[Coord{y, x}]++
		paths[Coord{y, x}]++
		return
	}
	//N
	hikeDown(y-1, x, curr, paths)
	//E
	hikeDown(y, x+1, curr, paths)
	//S
	hikeDown(y+1, x, curr, paths)
	//W
	hikeDown(y, x-1, curr, paths)
	return
}

func day10part1() {
	findable = make(map[Coord]int)
	ans1 := 0
	for y, line := range topog {
		for x, h := range line {
			if h == 9 {
				paths := make(map[Coord]int)
				//N
				hikeDown(y-1, x, h, paths)
				//E
				hikeDown(y, x+1, h, paths)
				//S
				hikeDown(y+1, x, h, paths)
				//W
				hikeDown(y, x-1, h, paths)

				ans1 += len(paths)
			}
		}
	}
	total := 0
	for _, v := range findable {
		total += v
	}
	fmt.Println(ans1)
	fmt.Println(total)

}

func day10part2() {
	// for y, line := range topog {
	// 	for x, h := range line {
	// 		if h == 0 {
	// 			//N
	// 			hike(y-1, x, h)
	// 			//E
	// 			hike(y, x+1, h)
	// 			//S
	// 			hike(y+1, x, h)
	// 			//W
	// 			hike(y, x-1, h)
	//
	// 		}
	// 	}
	// }
	// fmt.Println(totalTrails)

}

func Day10() {
	input := goutils.FileAsString("./input/2024-10-input.txt")
	makeTrail(input)
	fmt.Println("----- Part 1 -----")
	day10part1()
	fmt.Println("----- Part 2 -----")
	day10part2()
}
