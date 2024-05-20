package main

import (
	"aoc2015/pkg/utils"
)

func Day1() {
	fileAsString := utils.FileAsString("./data/day1.txt")
	floor := 0

	for pos, char := range fileAsString {
		if char == '(' {
			floor++
		}
		if char == ')' {
			floor--
		}
		if floor == -1 {
			println("basement!", pos+1)
		}
	}

	println(floor)
}
