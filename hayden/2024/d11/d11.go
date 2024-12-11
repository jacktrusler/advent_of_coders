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
	for i := 0; i < len(newState); i++ {
		newState[i] = -1
	}
	newStateCur := 0
	for _, rock := range rocks {
		if rock == 0 {
			newState[newStateCur] = 1
			newStateCur++
			continue
		}
		digits := digitCount(rock)
		if digitCount(rock)%2 == 0 {
			newState = append(newState, -1)
			leftRock, rightRock := splitRock(rock, digits)
			//fmt.Printf("Split %d, %d & %d\n", rock, leftRock, rightRock)
			newState[newStateCur] = leftRock
			newState[newStateCur+1] = rightRock
			newStateCur += 2
			continue
		}
		if rock == -1 {
			continue
		}
		newState[newStateCur] = rock * 2024
		newStateCur++
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
	for i := 0; i < 25; i++ {
		stones = blink(stones)

	}
	fmt.Printf("after 25 : %d\n", len(stones))
	for i := 0; i < 50; i++ {
		stones = blink(stones)
	}
	fmt.Printf("after 75 : %d\n", len(stones))
}
