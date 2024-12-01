package main

import (
	"aoc2015/pkg/utils"
	"fmt"
	"strings"
)

func Day8() {
	fmt.Println("Running day 8...")
	ans1 := day8Part1(utils.ReadFile("./data/day08.txt"))
	fmt.Println("--- Part 1 ---")
	fmt.Println(ans1)

	ans2 := day8Part2(utils.ReadFile("./data/day08.txt"))
	fmt.Println("--- Part 2 ---")
	fmt.Println(ans2)
}

func day8Part1(input string) int {
	var codeChars, stringChars int
	for _, line := range strings.Split(input, "\n") {
		codeChars += len(line)

		for i := 1; i < len(line)-1; i++ {
			switch line[i] {
			case '\\':
				nextChar := line[i+1]
				if nextChar == '\\' || nextChar == '"' {
					i++ // skip an extra character
				} else if nextChar == 'x' {
					i += 3 // skip 2 extra chars
				}
			}
			stringChars++
		}
	}

	return codeChars - stringChars
}

func day8Part2(input string) int {
	var encodedLen, originalLen int
	for _, line := range strings.Split(input, "\n") {
		originalLen += len(line)
		encodedLen += 2 // outer quotes
		for i := 0; i < len(line); i++ {
			switch line[i] {
			case '"', '\\':
				encodedLen += 2
			default:
				encodedLen++
			}
		}
	}
	return encodedLen - originalLen
}
