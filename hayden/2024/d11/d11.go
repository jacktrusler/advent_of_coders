package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
	"time"
)

type RockMath struct {
	qty int
	res []int
}

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
func blink182(rocks map[int]RockMath) map[int]RockMath {
	updates := make(map[int]int)
	for key, table := range rocks {
		if table.qty == 0 {
			//fmt.Printf("empty qty of %d\n", key)
			continue
		}
		if len(table.res) == 0 {
			//fmt.Printf("Must calculate ")
			updateRes := calcBlinkResult(key)
			table.res = updateRes
		}
		//fmt.Printf("I have precomputed results %v\n", key)
		for _, res := range table.res {
			//fmt.Printf("Adding %d to %d, original quantity %d ", res, table.qty, updates[res])
			updates[res] += table.qty
			//fmt.Printf(" new %d \n", updates[res])
		}
		table.qty = 0
		rocks[key] = table
	}
	//fmt.Println(updates)
	for key, quantity := range updates {
		updateRM := rocks[key]
		updateRM.qty = quantity
		rocks[key] = updateRM
	}
	return rocks
}
func calcBlinkResult(rock int) []int {
	if rock == 0 {
		return []int{1}
	}
	digits := digitCount(rock)
	if digitCount(rock)%2 == 0 {
		leftRock, rightRock := splitRock(rock, digits)
		//fmt.Printf("Split %d, %d & %d\n", rock, leftRock, rightRock)
		return []int{leftRock, rightRock}
	} else {
		return []int{rock * 2024}
	}
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

func processInput(raw []byte) map[int]RockMath {
	stoneStrs := strings.Fields(string(raw))
	stones := make(map[int]RockMath)
	for _, stoneStr := range stoneStrs {
		stone, err := strconv.Atoi(stoneStr)
		if err != nil {
			panic(err)
		}
		stoneRM := stones[stone]
		stoneRM.qty++
		stones[stone] = stoneRM
	}
	fmt.Println(stones)
	return stones
}

func main() {
	raw, err := os.ReadFile("./input.txt")
	if err != nil {
		panic("Bad File")
	}
	start := time.Now()
	stones := processInput(raw)
	for i := 0; i < 75; i++ {
		stones = blink182(stones)
	}
	stonect := 0
	for _, st := range stones {
		stonect += st.qty
	}
	duration := time.Since(start)
	fmt.Printf("On Exercise 2: %d\t(%s)\n", stonect, duration)
	/*
		for i := 0; i < 50; i++ {
			stones = blink182(stones)
		}
		fmt.Printf("after 75 : %d\n", len(stones))
	*/
}
