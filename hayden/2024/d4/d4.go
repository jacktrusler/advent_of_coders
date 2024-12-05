package main

import (
	"fmt"
	"os"
	"strings"
)

const FORWARD = 0
const DOWN = 1
const DOWNLEFT = 2
const DOWNRIGHT = 3

func e1(lines []string) int {
	runningTotal := 0
	XMax := len(lines[0]) - 1
	YMax := len(lines) - 1
	for YCur, line := range lines {
		for XCur, ch := range line {
			searchArry := make([]string, 4)
			//Start of search, if the char we land on is an X or an S we need to radiate out
			if ch == 'X' || ch == 'S' {
				if XCur+3 <= XMax {
					//Check Forward
					searchArry[FORWARD] = string(ch) + line[XCur+1:XCur+4]
				}
				if YCur+3 <= YMax {
					searchArry[DOWN] = string(ch) + string(lines[YCur+1][XCur]) + string(lines[YCur+2][XCur]) + string(lines[YCur+3][XCur])
				}
				if XCur+3 <= XMax && YCur+3 <= YMax {
					searchArry[DOWNRIGHT] = string(ch) + string(lines[YCur+1][XCur+1]) + string(lines[YCur+2][XCur+2]) + string(lines[YCur+3][XCur+3])
				}
				if XCur-3 >= 0 && YCur+3 <= YMax {
					searchArry[DOWNLEFT] = string(ch) + string(lines[YCur+1][XCur-1]) + string(lines[YCur+2][XCur-2]) + string(lines[YCur+3][XCur-3])
				}
				for _, wordle := range searchArry {
					if wordle == "XMAS" || wordle == "SAMX" {
						runningTotal++
					}
				}
			}
		}
	}
	return runningTotal
}
func e2(lines []string) int {
	runningTotal := 0
	XMax := len(lines[0]) - 1
	YMax := len(lines) - 1
	for YCur, line := range lines {
		for XCur, ch := range line {
			//Start of search, if the char we land on is an X or an S we need to radiate out
			if ch == 'A' && XCur+1 <= XMax && YCur+1 <= YMax && XCur-1 >= 0 && YCur-1 >= 0 {
				TopRightDownStr := string(lines[YCur-1][XCur-1]) + string(ch) + string(lines[YCur+1][XCur+1])
				BotRightUpStr := string(lines[YCur+1][XCur-1]) + string(ch) + string(lines[YCur-1][XCur+1])
				if (TopRightDownStr == "SAM" || TopRightDownStr == "MAS") && (BotRightUpStr == "SAM" || BotRightUpStr == "MAS") {
					runningTotal++
				}
			}
		}
	}
	return runningTotal
}
func main() {
	raw, err := os.ReadFile("input.txt")
	if err != nil {
		panic("Failed to open file ./input.txt")
	}
	split := strings.Split(string(raw), "\r\n")
	total := e1(split)
	fmt.Printf("On Exercise 1: %d\n", total)
	total = e2(split)
	fmt.Printf("On Exercise 2: %d\n", total)
}
