package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
)

func e1(fdata string) int {
	re := regexp.MustCompile(`mul\((?P<m1>[0-9]+),(?P<m2>[0-9]+)\)`)
	mulches := re.FindAllStringSubmatch(fdata, -1)
	runningTotal := 0
	for _, mulch := range mulches {
		m1, m1err := strconv.Atoi(mulch[1])
		m2, m2err := strconv.Atoi(mulch[2])
		if m2err != nil || m1err != nil {
			panic("Failed to parse both ints on str " + mulch[0])
		}
		runningTotal += m1 * m2
	}
	return runningTotal
}
func e2(fdata string) int {
	re := regexp.MustCompile(`don't\(\)|do\(\)|mul\((?P<m1>[0-9]+),(?P<m2>[0-9]+)\)`)
	mulchesNOps := re.FindAllStringSubmatch(fdata, -1)
	runningTotal := 0
	mulEnabled := true
	for _, MulOrOp := range mulchesNOps {
		if MulOrOp[0] == "do()" {
			mulEnabled = true
			continue
		}
		if MulOrOp[0] == "don't()" {
			mulEnabled = false
			continue
		}
		if mulEnabled {
			m1, m1err := strconv.Atoi(MulOrOp[1])
			m2, m2err := strconv.Atoi(MulOrOp[2])
			if m2err != nil || m1err != nil {
				panic("Failed to parse both ints on str " + MulOrOp[0])
			}
			runningTotal += m1 * m2
		}
	}
	return runningTotal
}
func main() {
	raw, err := os.ReadFile("input.txt")
	if err != nil {
		panic("Failed to open file ./input.txt")
	}
	total := e1(string(raw))
	fmt.Printf("On Exercise 1: %d\n", total)
	total = e2(string(raw))
	fmt.Printf("On Exercise 2: %d\n", total)
}
