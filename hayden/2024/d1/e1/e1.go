package main

import (
	"fmt"
	"os"
	"slices"
	"strconv"
	"strings"
)

func main() {
	numbers_raw, err := os.ReadFile("../input.txt")
	if err != nil {
		panic("It's goever before it even begon")
	}
	numbers_rows := strings.Split(string(numbers_raw), "\n")
	leftInput := make([]int, len(numbers_rows))
	rightInput := make([]int, len(numbers_rows))
	distance := 0
	for idx, row := range numbers_rows {
		lr_strs := strings.Fields(row)
		if len(lr_strs) != 2 {
			panic("It looks like our strings are inconsistent length")
		}
		left, errL := strconv.Atoi(lr_strs[0])
		right, errR := strconv.Atoi(lr_strs[1])
		if errL != nil || errR != nil {
			panic("You should've given me 2 integer you fricker")
		}
		leftInput[idx] = left
		rightInput[idx] = right
	}
	//Sorting Time
	slices.Sort(leftInput)
	slices.Sort(rightInput)
	for idx, lhs := range leftInput {
		thisDist := lhs - rightInput[idx]
		if thisDist < 0 {
			distance -= thisDist
		} else {
			distance += thisDist
		}
	}
	fmt.Println(distance)
}
