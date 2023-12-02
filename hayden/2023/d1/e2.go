package main

import (
	"os"
	"strconv"
	"strings"
)

func main() {
	input, err := os.ReadFile("input.txt")
	if err != nil {
		panic(err)
	}
	lines := strings.Split(string(input), "\n")
	acc := 0
	for _, line := range lines {
		//Forward Lookup
		var numbers []int
		for i := 0; i < len(line); i++ {
			char := line[i]
			digit, err := strconv.Atoi(string(char))
			//fast out
			if err == nil {
				numbers = append(numbers, digit)
				continue
			}
			if i+3 <= len(line) {
				lah3 := line[i : i+3]
				switch lah3 {
				case "one":
					numbers = append(numbers, 1)
					continue
				case "two":
					numbers = append(numbers, 2)
					continue
				case "six":
					numbers = append(numbers, 6)
					continue
				}
			}
			if i+4 <= len(line) {
				lah4 := line[i : i+4]
				switch lah4 {
				case "four":
					numbers = append(numbers, 4)
					continue
				case "five":
					numbers = append(numbers, 5)
					continue
				case "nine":
					numbers = append(numbers, 9)
					continue
				}
			}
			if i+5 <= len(line) {
				lah5 := line[i : i+5]
				switch lah5 {
				case "three":
					numbers = append(numbers, 3)
					continue
				case "seven":
					numbers = append(numbers, 7)
					continue
				case "eight":
					numbers = append(numbers, 8)
					continue
				}
			}
		}
		acc += numbers[0]*10 + numbers[len(numbers)-1]
	}
	println(acc)
}
