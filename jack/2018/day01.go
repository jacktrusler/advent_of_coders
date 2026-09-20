package main

import (
	"bufio"
	"os"
	"strconv"
)

// read in raw bytes and switch
func Day01(input []byte) int {
	sum := 0
	sign := 1
	num := 0
	for _, b := range input {
		switch b {
		case '+':
			sign = 1
		case '-':
			sign = -1
		case '\n':
			sum += sign * num
			num = 0
		default:
			num = num*10 + int(b-'0')
		}
	}
	sum += sign * num // no trailing newline, so must add final number manually
	return sum
}

// Standard library is faster than switching on raw bytes... Crazy
func Day01AtoI(file *os.File) int {
	scanner := bufio.NewScanner(file)
	sum := 0
	for scanner.Scan() {
		n, _ := strconv.Atoi(scanner.Text())
		sum += n
	}
	return sum
}

func Day01AtoIPart2(file *os.File) int {
	scanner := bufio.NewScanner(file)
	var changes []int
	for scanner.Scan() {
		n, _ := strconv.Atoi(scanner.Text())
		changes = append(changes, n)
	}

	sum := 0
	seen := map[int]bool{0: true}
	for {
		for _, n := range changes {
			sum += n
			if seen[sum] {
				return sum
			}
			seen[sum] = true
		}
	}
}
