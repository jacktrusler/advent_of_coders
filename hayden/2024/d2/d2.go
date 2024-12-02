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
		fmt.Println(line)
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
					fmt.Printf("P: %d, V: %d, D: %d Verdict: ", prev, val, direction)
					if val < prev {
						fmt.Println("Negative Movement")
						direction = -1
					} else if val > prev {
						fmt.Println("Positive Movement")
						direction = 1
					}
				}
				//Check that we didn't flip directionality
				if (direction == 1 && val < prev) || (direction == -1 && val > prev) {
					fmt.Println("Flip")
					safe = false
					break
				}
				// Check that we didn't exceed movement limits
				dist := val - prev
				fmt.Printf("P: %d, V: %d, Dist: %d\n", prev, val, dist)
				if dist > 3 || dist < -3 || dist == 0 {
					fmt.Println("Exceeded Movement")
					safe = false
					break
				}
				prev = val
			}
		}
		if safe {
			fmt.Println("Safe")
			safeCount += 1
		}
	}
	return safeCount
}
func e2(lines []string) int {
	safeCount := 0
	for _, line := range lines {
		readings := strings.Fields(line)
		fmt.Println(line)
		previousReading := 0
		dampenAllowed := true
		dirSet := false
		direction := 0
		rewindReading := 0
		safe := true
		for idx, reading := range readings {
			val, err := strconv.Atoi(reading)
			if err != nil {
				panic("FEED ME A PARSABLE INTEGER")
			}
			//If the previous reading was -1, set the value and skip to next
			if idx == 0 {
				fmt.Printf("Initial Reading: %d\n", val)
				previousReading = val
			} else {
				// We need to check direction
				newDirection := 0
				if val > previousReading {
					newDirection = 1
				} else if val < previousReading {
					newDirection = -1
				}
				// Now pull distance
				distance := val - previousReading
				fmt.Printf("Rew: %d Prev: %d, Val: %d, Dir: %d, NewDir: %d, Dist: %d\n", rewindReading, previousReading, val, direction, newDirection, distance)
				//The following events would be disqualifying:
				if distance > 3 || distance < -3 || distance == 0 {
					fmt.Printf("Disqualified \n")
					if dampenAllowed {
						fmt.Printf("Dampening\n")
						dampenAllowed = false
						previousReading = rewindReading
						continue
					}
					safe = false
				}
				if newDirection != direction && dirSet {
					fmt.Printf("Disqualified \n")
					if dampenAllowed {
						fmt.Printf("Dampening\n")
						dampenAllowed = false
						previousReading = rewindReading
						continue
					}
					safe = false
				}
				if !dirSet {
					direction = newDirection
				}
				fmt.Printf("updating previous reading\n")
				rewindReading = previousReading
				previousReading = val
			}
		}
		if safe {
			fmt.Printf("Safe \n")
			safeCount += 1
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
	safeCount := e2(lines)
	fmt.Println(safeCount)
}
