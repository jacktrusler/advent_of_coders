package main

import (
	"fmt"
	u "goutils"
	"strings"
)

func day16part1(maze []string) {

}

func day16part2(maze []string) {

}

func Day16() {
	input := u.FileAsString("./input/16-example.txt")
	maze := strings.Split(input, "\n")

	fmt.Println("----- Part 1 -----")
	day16part1(maze)
	fmt.Println("----- Part 2 -----")
	day16part2(maze)
}
