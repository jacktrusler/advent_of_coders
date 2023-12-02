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
		lacc := 0
		//Forward
		for i := 0; i < len(line); i++ {
			digit, err := strconv.Atoi(string(line[i]))
			if err == nil {
				lacc += digit * 10
				break
			}
		}
		//Backward
		for i := len(line) - 1; i >= 0; i-- {
			digit, err := strconv.Atoi((string(line[i])))
			if err == nil {
				lacc += digit
				break
			}
		}
		acc += lacc
	}
	println(acc)
}
