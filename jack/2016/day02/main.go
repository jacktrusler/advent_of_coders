package main

import (
	"aoc2016/util"
	"fmt"
	"strings"
)

func part1(input string) {
	keypad := [][3]int{
		{1, 2, 3},
		{4, 5, 6},
		{7, 8, 9},
	}

	codes := strings.Split(input, "\n")
	arrLen := 2
	curr := [2]int{1, 1}
	finalInput := make([]int, 0)

	for _, code := range codes {
		for _, dir := range code {
			switch dir {
			case 'U':
				if (curr[0]) > 0 {
					curr[0]--
				}
			case 'R':
				if (curr[1]) < arrLen {
					curr[1]++
				}
			case 'D':
				if (curr[0]) < arrLen {
					curr[0]++
				}
			case 'L':
				if (curr[1]) > 0 {
					curr[1]--
				}
			}
		}
		finalInput = append(finalInput, keypad[curr[0]][curr[1]])
	}

	fmt.Println(finalInput)

}

func part2(input string) {
	// pad empty spaces with zeros
	keypad := [5][5]int{
		{0, 0, 1, 0, 0},
		{0, 2, 3, 4, 0},
		{5, 6, 7, 8, 9},
		{0, 'A', 'B', 'C', 0},
		{0, 0, 'D', 0, 0},
	}

	codes := strings.Split(input, "\n")
	arrLen := 4
	curr := [2]int{2, 0}
	finalInput := make([]int, 0)

	for _, code := range codes {
		for _, dir := range code {
			switch dir {
			case 'U':
				if (curr[0]) > 0 && keypad[curr[0]-1][curr[1]] != 0 {
					curr[0]--
				}
			case 'R':
				if (curr[1]) < arrLen && keypad[curr[0]][curr[1]+1] != 0 {
					curr[1]++
				}
			case 'D':
				if (curr[0]) < arrLen && keypad[curr[0]+1][curr[1]] != 0 {
					curr[0]++
				}
			case 'L':
				if (curr[1]) > 0 && keypad[curr[0]][curr[1]-1] != 0 {
					curr[1]--
				}
			}
		}
		finalInput = append(finalInput, keypad[curr[0]][curr[1]])
	}

	fmt.Println("ASCII table 65 is capital A, 66 is capital B etc...")
	fmt.Println(finalInput)

}

func main() {
	input := util.FileAsString("./input.txt")
	fmt.Println("----- Part 1 -----")
	part1(input)
	fmt.Println("----- Part 2 -----")
	part2(input)
}
