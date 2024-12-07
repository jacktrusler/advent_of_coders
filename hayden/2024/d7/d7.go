package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
	"time"
	"unicode"
)

const (
	NUL = iota
	ADD
	MUL
	CAT
)

type CalibrationEquation struct {
	result int
	inputs []int
}

func isPossibleCalibration(equation CalibrationEquation, catMode bool) bool {
	myOpps := recurseThruOperands(equation.inputs, 0, catMode)
	for _, opChain := range myOpps {
		lh := equation.inputs[0]
		inputIndex := 1
	Exit:
		for _, op := range opChain {
			switch op {
			case ADD:
				lh += equation.inputs[inputIndex]
			case MUL:
				lh *= equation.inputs[inputIndex]
			case CAT:
				digis := len(strconv.Itoa(equation.inputs[inputIndex]))
				lh *= int(math.Pow10(digis))
				lh += equation.inputs[inputIndex]
			case NUL:
				break Exit
			}
			inputIndex++
		}
		if lh == equation.result {
			return true
		}
	}

	return false
}
func recurseThruOperands(operands []int, index int, catMode bool) [][]int {
	if index == len(operands)-1 {
		return [][]int{{0}}
	}
	downstream := recurseThruOperands(operands, index+1, catMode)
	upstream := make([][]int, 0)
	for _, chainSum := range downstream {
		mChain := []int{MUL}
		aChain := []int{ADD}
		mChain = append(mChain, chainSum...)
		aChain = append(aChain, chainSum...)
		upstream = append(upstream, mChain)
		upstream = append(upstream, aChain)
		if catMode {
			cChain := []int{CAT}
			cChain = append(cChain, chainSum...)
			upstream = append(upstream, cChain)
		}
	}
	return upstream
}
func e1(equations []CalibrationEquation) int {
	total := 0
	for _, equation := range equations {
		if isPossibleCalibration(equation, false) {
			total += equation.result
		}
	}
	return total
}
func e2(equations []CalibrationEquation) int {
	total := 0
	for _, equation := range equations {
		if isPossibleCalibration(equation, true) {
			total += equation.result
		}
	}
	return total
}
func preprocessInput(raw []byte) []CalibrationEquation {
	split := strings.Split(string(raw), "\r\n")
	equations := make([]CalibrationEquation, len(split))
	for idx, rowStr := range split {
		f := func(c rune) bool {
			return unicode.IsSpace(c) || c == ':'
		}
		columns := strings.FieldsFunc(rowStr, f)
		inputs := make([]int, len(columns)-1)
		result, resErr := strconv.Atoi(columns[0])
		if resErr != nil {
			panic(resErr)
		}
		for i := 1; i < len(columns); i++ {
			input, inErr := strconv.Atoi(columns[i])
			if inErr != nil {
				panic(inErr)
			}
			inputs[i-1] = input
		}
		equation := CalibrationEquation{result: result, inputs: inputs}
		equations[idx] = equation
	}
	return equations
}
func main() {
	raw, err := os.ReadFile("input.txt")
	if err != nil {
		panic("Failed to open file ./input.txt")
	}
	equations := preprocessInput(raw)
	start := time.Now()
	total := e1(equations)
	duration := time.Since(start)
	fmt.Printf("On Exercise 1: %d\t(%s)\n", total, duration)
	start = time.Now()
	total = e2(equations)
	duration = time.Since(start)
	fmt.Printf("On Exercise 2: %d\t(%s)\n", total, duration)
}
