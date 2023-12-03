package main

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"
)

const Max_Red = 12
const Max_Green = 13
const Max_Blue = 14

func checkGreater(s []string, rxp *regexp.Regexp, maxVal int) bool {
	for _, str := range s {
		digits := rxp.FindAllString(str, -1)
		for _, digit := range digits {
			num, _ := strconv.Atoi(digit)
			if num > maxVal {
				return true
			}
		}
	}
	return false
}

func checkMax(s []string, rxp *regexp.Regexp, maxVal int) int {
	max := 0
	for _, str := range s {
		digits := rxp.FindAllString(str, -1)
		for _, digit := range digits {
			num, _ := strconv.Atoi(digit)
			if num > max {
				max = num
			}
		}
	}
	return max
}

func Day2() {
	fileAsString := FileAsString("./data/day02.txt")
	fileAsString = strings.TrimSuffix(fileAsString, "\n")
	allGames := strings.Split(fileAsString, "\n")

	idTotal := 0
	sumPower := 0

	for _, game := range allGames {
		rgxDigits, err1 := regexp.Compile("\\d+")
		rgxBlue, err2 := regexp.Compile(`\d+\s+(?:blue)`)
		rgxGreen, err3 := regexp.Compile(`\d+\s+(?:green)`)
		rgxRed, err4 := regexp.Compile(`\d+\s+(?:red)`)

		if err1 != nil || err2 != nil || err3 != nil || err4 != nil {
			fmt.Println("Error compiling regex")
			return
		}

		id := rgxDigits.FindString(game)
		reds := rgxRed.FindAllString(game, -1)
		greens := rgxGreen.FindAllString(game, -1)
		blues := rgxBlue.FindAllString(game, -1)

		// Part 1
		redGreater := checkGreater(reds, rgxDigits, Max_Red)
		greenGreater := checkGreater(greens, rgxDigits, Max_Green)
		blueGreater := checkGreater(blues, rgxDigits, Max_Blue)

		if !redGreater && !greenGreater && !blueGreater {
			numId, _ := strconv.Atoi(id)
			idTotal += numId
		}

		// Part 2
		redMax := checkMax(reds, rgxDigits, Max_Red)
		greenMax := checkMax(greens, rgxDigits, Max_Green)
		blueMax := checkMax(blues, rgxDigits, Max_Blue)

		sumPower += redMax * greenMax * blueMax

	}
	fmt.Println("Part 1: ", idTotal)
	fmt.Println("Part 2: ", sumPower)
}
