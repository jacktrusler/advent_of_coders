package main

import (
	"fmt"
	"math"
	"regexp"
	"strings"
)

func Day4() {
	fileAsString := FileAsString("./data/day04.txt")

	re, _ := regexp.Compile(`^Card\s*\d+:\s*`)
	numbersOnly := re.ReplaceAllString(fileAsString, "")
	lines := strings.Split(numbersOnly, "\n")

	myCards := make([]string, 0)
	winningNums := make([]string, 0)
	for _, line := range lines {
		newLine := re.ReplaceAllString(line, "")
		splitLine := strings.Split(newLine, "|")
		myCards = append(myCards, splitLine[0])
		winningNums = append(winningNums, splitLine[1])
	}

	length := len(myCards)
	totalP1 := 0.0
	totalP2 := 0

	// Part 2
	// Make an array with the amount of times you have to play the card and how many copies it makes
	// Every card starts at 1 play
	var playedArr [208]int
	for i := range playedArr {
		playedArr[i] = 1
	}

	for i := 0; i < length; i++ {
		myCard := strings.Fields(myCards[i])
		winning := strings.Fields(winningNums[i])
		matches := 0
		for _, myNum := range myCard {
			for _, winNum := range winning {
				if myNum == winNum {
					matches++
				}
			}
		}
		if matches > 0 {
			// Part 1
			totalP1 += math.Pow(2, float64(matches-1))
			// Part 2
			for ; 0 < matches; matches-- {
				playedArr[i+matches] = playedArr[i+matches] + playedArr[i]
			}
		}
	}

	for _, cardCount := range playedArr {
		totalP2 += cardCount
	}
	fmt.Println("----- Day 4 -----")
	fmt.Println("Part 1: ", totalP1)
	fmt.Println("Part 2: ", totalP2)
}
