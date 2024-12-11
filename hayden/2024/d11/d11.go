package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

func splitRock(rock int, digits int) (int, int) {
	splitter := math.Pow10(digits / 2)
	return rock / int(splitter), rock % int(splitter)
}
func digitCount(rock int) int {
	digits := 0
	for digits = 0; rock > 0; rock /= 10 {
		digits++
	}
	return digits
}
func blink(rocks []int) []int {
	newState := make([]int, len(rocks))
	newStateCur := 0
	for _, rock := range rocks {
		if rock == 0 {
			newState[newStateCur] = 1
			continue
		}
		digits := digitCount(rock)
		if digitCount(rock)%2 == 0 {
			leftRock, rightRock := splitRock(rock, digits)
			fmt.Printf("Split %d, %d & %d\n", rock, leftRock, rightRock)
			newState1
		}
	}
	return newState
}

func processInput(raw []byte) []int {
	stoneStrs := strings.Fields(string(raw))
	stones := make([]int, len(stoneStrs))
	for stoneIdx, stoneStr := range stoneStrs {
		stone, err := strconv.Atoi(stoneStr)
		if err != nil {
			panic(err)
		}
		stones[stoneIdx] = stone
	}
	return stones
}

func main() {
	raw, err := os.ReadFile("./input.txt")
	if err != nil {
		panic("Bad File")
	}
	stones := processInput(raw)
	blink(stones)
	fmt.Println(stones)
}
