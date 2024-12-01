package main

import (
	"aoc2015/pkg/utils"
	"fmt"
	"regexp"
	"strings"
)

func makeLightArray() [][]int {
	twoDArr := make([][]int, 1000)
	for i := range twoDArr {
		twoDArr[i] = make([]int, 1000)
	}
	return twoDArr
}

func Day6() {
	fmt.Println("Running day 6...")
	fileAsString := utils.FileAsString("./data/day06.txt")
	stringArr := strings.Split(fileAsString, "\n")

	//-------- part 1 --------
	lightArray := makeLightArray()
	for i := range stringArr {
		var x1, x2, y1, y2 int

		// match instruction (string up to first digit)
		re := regexp.MustCompile(`^\D*`)
		match := re.FindString(stringArr[i])

		_, err := fmt.Sscanf(stringArr[i], match+"%d,%d through %d,%d", &x1, &y1, &x2, &y2)
		if err != nil {
			fmt.Println("Error parsing string:", err)
			return
		}
		// apply instructions to light array
		for y := y1; y <= y2; y++ {
			for x := x1; x <= x2; x++ {
				switch match {
				case "turn on ":
					lightArray[y][x] = 1
				case "turn off ":
					lightArray[y][x] = 0
				case "toggle ":
					if lightArray[y][x] == 0 {
						lightArray[y][x] = 1
					} else {
						lightArray[y][x] = 0
					}
				}
			}
		}

	}

	lit := 0

	for _, row := range lightArray {
		for _, light := range row {
			if light == 1 {
				lit++
			}
		}
	}
	fmt.Println("-------- Part 1 ---------")
	fmt.Println(lit)

	//-------- part 2 ---------
	lightArray2 := makeLightArray()
	for i := range stringArr {
		var x1, x2, y1, y2 int

		// match instruction (string up to first digit)
		re := regexp.MustCompile(`^\D*`)
		match := re.FindString(stringArr[i])

		_, err := fmt.Sscanf(stringArr[i], match+"%d,%d through %d,%d", &x1, &y1, &x2, &y2)
		if err != nil {
			fmt.Println("Error parsing string:", err)
			return
		}
		// apply instructions to light array
		for y := y1; y <= y2; y++ {
			for x := x1; x <= x2; x++ {
				switch match {
				case "turn on ":
					lightArray2[y][x]++
				case "turn off ":
					if lightArray2[y][x] > 0 {
						lightArray2[y][x]--
					}
				case "toggle ":
					lightArray2[y][x] += 2
				}
			}
		}
	}

	brightness := 0

	for _, row := range lightArray2 {
		for _, light := range row {
			brightness += light
		}
	}
	fmt.Println("-------- Part 2 ---------")
	fmt.Println(brightness)
}
