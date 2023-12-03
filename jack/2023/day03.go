package main

import (
	"fmt"
	"strconv"
	"strings"
)

func surroundedSymbol(arr [][]rune, col int, row int) bool {
	for dx := -1; dx <= 1; dx++ {
		for dy := -1; dy <= 1; dy++ {
			surrR := arr[col+dy][row+dx]
			if surrR != '.' && (surrR < '0' || surrR > '9') {
				return true
			}
		}
	}
	return false
}

func surroundedGear(arr [][]rune, col int, row int) (int, int) {
	for dx := -1; dx <= 1; dx++ {
		for dy := -1; dy <= 1; dy++ {
			surrR := arr[col+dy][row+dx]
			if surrR == '*' {
				return col + dy, row + dx
			}
		}
	}
	return -1, -1
}

func Day3() {
	fileAsString := FileAsString("./data/day03.txt")
	fileAsString = strings.TrimSuffix(fileAsString, "\n")
	lines := strings.Split(fileAsString, "\n")

	var linesToRunes [][]rune
	// Convert lines to runes and surround the whole 2d matrix with '.' to avoid edge cases

	// adding '.' in x direction
	for _, str := range lines {
		currRunes := []rune(str)
		currRunes = append(currRunes, '.')
		currRunes = append([]rune{'.'}, currRunes...)
		linesToRunes = append(linesToRunes, currRunes)
	}

	// adding line of '.' in y direction
	var dotLine []rune
	for i := 0; i < len(linesToRunes[0]); i++ {
		dotLine = append(dotLine, '.')
	}

	linesToRunes = append([][]rune{dotLine}, linesToRunes...)
	linesToRunes = append(linesToRunes, dotLine)

	totalP1 := 0
	currNum := ""
	columns := len(linesToRunes)
	rows := len(linesToRunes[0])
	symbolTouch := false

	// ------ Part 1 ------
	for y := 0; y < columns; y++ {
		for x := 0; x < rows; x++ {
			// check for numbers 0-9, ascii values 48-57
			currRune := linesToRunes[y][x]
			if currRune >= '0' && currRune <= '9' {
				// build the whole number
				currNum += string(currRune)
				// when any number is found check if any surrounding index contains a special character (not a '.' or number)
				if surroundedSymbol(linesToRunes, y, x) {
					symbolTouch = true
				}
			}
			// when you reach a dot or special character you're done with the numbers
			// if any number touched a special char, add it
			if currRune < '0' || currRune > '9' {
				if symbolTouch {
					intNum, _ := strconv.Atoi(currNum)
					totalP1 += intNum
				}
				// Clear currNum and flag
				currNum = ""
				symbolTouch = false
			}
		}
	}
	fmt.Println("Part 1: ", totalP1)

	// ------ Part 2 ------

	totalP2 := 0
	cacheKey := ""

	gearMap := make(map[string][]string)

	for y := 0; y < columns; y++ {
		for x := 0; x < rows; x++ {
			currRune := linesToRunes[y][x]
			if currRune >= '0' && currRune <= '9' {
				currNum += string(currRune)
				gearPosY, gearPosX := surroundedGear(linesToRunes, y, x)
				if gearPosX != -1 && gearPosY != -1 {
					cacheKey = string(gearPosY) + "," + string(gearPosX)
				}
			}
			if currRune < '0' || currRune > '9' {
				if cacheKey != "" {
					gearMap[cacheKey] = append(gearMap[cacheKey], currNum)
				}
				// Clear currNum and flag
				currNum = ""
				cacheKey = ""
			}
		}
	}

	for _, value := range gearMap {
		if len(value) == 2 {
			val1, _ := strconv.Atoi(value[0])
			val2, _ := strconv.Atoi(value[1])

			totalP2 += val1 * val2
		}
	}

	fmt.Println("Part 2: ", totalP2)
}
