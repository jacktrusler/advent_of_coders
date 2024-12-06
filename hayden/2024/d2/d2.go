package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func e1(lines []string) int {
	safeCount := 0
	for _, line := range lines {
		readings := strings.Fields(line)

		prev := -1
		direction := 0
		safe := true
		for _, reading := range readings {
			val, err := strconv.Atoi(reading)
			if err != nil {
				panic("FEED ME A PARSABLE INTEGER")
			}
			// Set first value
			if prev == -1 {
				prev = val
			} else {
				//Check our directionality, if we don't go either up or down toss
				if direction == 0 {
					if val < prev {

						direction = -1
					} else if val > prev {

						direction = 1
					}
				}
				//Check that we didn't flip directionality
				if (direction == 1 && val < prev) || (direction == -1 && val > prev) {

					safe = false
					break
				}
				// Check that we didn't exceed movement limits
				dist := val - prev
				if dist > 3 || dist < -3 || dist == 0 {

					safe = false
					break
				}
				prev = val
			}
		}
		if safe {
			safeCount += 1
		}
	}
	return safeCount
}
func isSafe(readings []int) bool {
	prev := -1
	direction := 0
	safe := true
	for _, reading := range readings {
		// Set first value
		if prev == -1 {
			prev = reading
		} else {
			//Check our directionality, if we don't go either up or down toss
			if direction == 0 {
				if reading < prev {

					direction = -1
				} else if reading > prev {

					direction = 1
				}
			}
			//Check that we didn't flip directionality
			if (direction == 1 && reading < prev) || (direction == -1 && reading > prev) {

				safe = false
				break
			}
			// Check that we didn't exceed movement limits
			dist := reading - prev
			if dist > 3 || dist < -3 || dist == 0 {

				safe = false
				break
			}
			prev = reading
		}
	}
	return safe
}
func e2(lines []string) int {
	safeCount := 0
	for _, line := range lines {
		readings := strings.Fields(line)
		readInts := make([]int, len(readings))
		for idx, reading := range readings {
			val, err := strconv.Atoi(reading)
			if err != nil {
				panic("FEED ME A PARSABLE INTEGER")
			}
			readInts[idx] = val
		}
		if isSafe(readInts) {
			safeCount++
		} else {
			fixable := false
			for cutInd := 0; cutInd < len(readInts) && !fixable; cutInd++ {
				withCut := make([]int, 0)
				sliceable := make([]int, len(readInts))
				copy(sliceable, readInts)
				switch cutInd {
				case 0:
					withCut = append(withCut, sliceable[1:]...)
				case len(readInts) - 1:
					withCut = append(withCut, sliceable[:len(readInts)-1]...)
				default:
					withCut = append(sliceable[:cutInd], sliceable[cutInd+1:]...)
				}
				if isSafe(withCut) {
					fixable = true
				}
			}
			if fixable {
				safeCount++
			}
		}
	}
	return safeCount
}
func main() {
	raw, err := os.ReadFile("input.txt")
	if err != nil {
		panic("Failed to open file ./input.txt")
	}
	lines := strings.Split(string(raw), "\n")
	safeCount := e1(lines)
	fmt.Printf("For Exercise 1: Safe %d\n", safeCount)
	safeCount = e2(lines)
	fmt.Printf("For Exercise 2: Safe %d\n", safeCount)
}
