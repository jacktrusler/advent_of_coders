package main

import (
	"fmt"
	"goutils"
	"regexp"
	"strconv"
	"strings"
)

func regexAndMultiply(input string) int {
	// pull out exact match: mul(\d*,\d*)
	re := regexp.MustCompile(`mul\(\d*,\d*\)`)
	matches := re.FindAllString(input, -1)

	var total int
	for _, match := range matches {
		re2 := regexp.MustCompile(`[\d*]+`)
		matches2 := re2.FindAllString(match, -1)

		var num1, num2 int
		var err error
		num1, err = strconv.Atoi(matches2[0])
		num2, err = strconv.Atoi(matches2[1])
		if err != nil {
			panic("Failed string conv")
		}
		total += num1 * num2
	}
	return total
}

func day3part1(input string) {
	ans := regexAndMultiply(input)

	fmt.Println(ans)
}

func day3part2(input string) {

	// Regex can ligma and suggma and zuggma
	bigFatMulSlice := make([]byte, 0)

	// Start parsing from the beginning, toggle off when you hit the first 'don't()'
	toggle := true
	for i := 0; i < len(input)-7; {

		do := make([]byte, 4)
		dont := make([]byte, 7)

		do[0] = input[i]
		do[1] = input[i+1]
		do[2] = input[i+2]
		do[3] = input[i+3]

		dont[0] = input[i]
		dont[1] = input[i+1]
		dont[2] = input[i+2]
		dont[3] = input[i+3]
		dont[4] = input[i+4]
		dont[5] = input[i+5]
		dont[6] = input[i+6]

		if string(do) == "do()" {
			toggle = true
			i += 3
		}
		if string(dont) == "don't()" {
			toggle = false
			i += 6
		}

		if toggle {
			bigFatMulSlice = append(bigFatMulSlice, input[i])
		}

		i++

	}
	ans := regexAndMultiply(string(bigFatMulSlice))
	fmt.Println(ans)

}

func day3part2bad(input string) {
	// 'enabled' until first don't
	re1 := regexp.MustCompile(`^(.*?)don't\(\)`)
	// this has a nasty bug i don't understand
	re2 := regexp.MustCompile(`do\(\)(.*?)don't\(\)`)
	// everything from final do() to the end
	re3 := regexp.MustCompile(`.*do\(\)(.*?)$`)
	e1 := re1.FindAllStringSubmatch(input, -1)
	e2 := re2.FindAllStringSubmatch(input, -1)
	e3 := re3.FindAllStringSubmatch(input, -1)

	finalArr := make([]string, 0)

	for _, s1 := range e1 {
		finalArr = append(finalArr, s1[1])
	}

	for _, s2 := range e2 {
		finalArr = append(finalArr, s2[1])
	}
	// include do() to the end: If it doesn't contain a don't()
	end := e3[len(e3)-1][1]
	if !strings.Contains(end, "don't()") {
		finalArr = append(finalArr, end)
	}

	var totalP2, matches int
	for i, enabled := range finalArr {
		tot := regexAndMultiply(enabled)
		totalP2 = totalP2 + tot
		fmt.Println(i)
	}

	fmt.Println(totalP2, matches)
}

func Day3() {
	input := goutils.FileAsString("./input/day03.txt")
	fmt.Println("----- Part 1 -----")
	day3part1(input)
	fmt.Println("----- Part 2 -----")
	day3part2(input)
}
