package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func blink(rocks []int) []int {
	newState := make([]int, len(rocks))
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
	fmt.Println(stones)
}
