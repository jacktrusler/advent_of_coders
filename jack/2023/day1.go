package main

import (
	"fmt"
	"log"
	"strconv"
	"strings"
)

func determineSum(s []string) int {
	calibrationValues := make([]string, 0)
	// Part 1
	for _, line := range s {
		val1, val2 := "0", "0"
		for _, runeValue := range line {
			if runeValue >= 48 && runeValue <= 57 {
				if val1 == "0" {
					val1 = string(runeValue)
				}
				val2 = string(runeValue)
			}
		}
		calibrationValues = append(calibrationValues, val1+val2)
	}
	fmt.Println(s)

	totalSum := 0
	for _, value := range calibrationValues {
		num, err := strconv.Atoi(value)
		if err != nil {
			log.Fatal(err)
		}

		totalSum += num
	}
	fmt.Println(calibrationValues)
	return totalSum
}

func Day1() {
	fileAsString := FileAsString("day1.txt")
	fileAsString = strings.TrimSuffix(fileAsString, "\n")
	stringArrP1 := strings.Split(fileAsString, "\n")

	// Part 1
	totalSumP1 := determineSum(stringArrP1)

	// Part 2
	arr1 := [9]string{"one", "two", "three", "four", "five", "six", "seven", "eight", "nine"}
	arr2 := [9]string{"1", "2", "3", "4", "5", "6", "7", "8", "9"}

	fileAsStr2 := fileAsString
	fileAsStr2 = strings.TrimSuffix(fileAsStr2, "\n")
	replacedNumbers := fileAsStr2
	// Dirty hack to get this to work, append "word" before and after digit so word
	// collisions like twone and oneight get separated into
	// twone1one and one1oneight
	// two2twone1one one1oneight8eight
	for i := 0; i < 9; i++ {
		replacedNumbers = strings.Replace(replacedNumbers, arr1[i], arr1[i]+arr2[i]+arr1[i], -1)
	}

	stringArrP2 := strings.Split(replacedNumbers, "\n")
	totalSumP2 := determineSum(stringArrP2)

	fmt.Println(totalSumP1)
	fmt.Println(totalSumP2)
}
