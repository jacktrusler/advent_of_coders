package main

import (
	"fmt"
	"os"
)

func main() {
	input, err := os.Open("./input/2018-01-input.txt")
	if err != nil {
		return
	}
	repeatFreq := Day01AtoIPart2(input)
	fmt.Println(repeatFreq)
}
