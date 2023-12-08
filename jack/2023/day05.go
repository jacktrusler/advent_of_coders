package main

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"
)

/*
seeds: 79 14 55 13
seed-to-soil map:
dest | source | range (s)
50 98 2
52 50 48
*/

//seeds: 104847962 3583832 1212568077 114894281 3890048781 333451605 1520059863 217361990 310308287 12785610 3492562455 292968049 1901414562 516150861 2474299950 152867148 3394639029 59690410 862612782 176128197

func convertSeed(seed int, conversionArr []int) int {
	for i := 0; i < len(conversionArr); i += 3 {
		dest := conversionArr[i]
		source := conversionArr[i+1]
		r := conversionArr[i+2]

		if (seed >= source) && (seed <= source+r-1) {
			seed = seed + (dest - source)
			return seed
		}
	}
	return seed
}

func reverseSeed(seed int, conversionArr []int) int {
	for i := 0; i < len(conversionArr); i += 3 {
		dest := conversionArr[i]
		source := conversionArr[i+1]
		r := conversionArr[i+2]

		if (seed >= dest) && (seed <= dest+r-1) {
			seed = seed + (source - dest)
			return seed
		}
	}
	return seed
}

func theOneSeed(currentSeed int, seeds []int) bool {
	// Check to see if this seed exists in input, if it does return it
	for i := 0; i < len(seeds); i += 2 {
		if (currentSeed >= seeds[i]) && (currentSeed <= seeds[i]+seeds[i+1]) {
			return true
		}
	}
	return false
}

func Day5() {
	fileAsString := FileAsString("./data/day05.txt")
	lines := strings.Split(fileAsString, "\n\n")

	numRegex := regexp.MustCompile("\\d+")
	// find only words
	letterRegex := regexp.MustCompile("[^0-9 \n:]+")

	almanac := make(map[string][]int)

	// Create the almanac i.e
	// key [seed-to-soil]: []int
	for _, line := range lines {
		allNumbers := numRegex.FindAllString(line, -1)
		allLetters := letterRegex.FindAllString(line, -1)
		numArr := make([]int, 0)
		almanac[allLetters[0]] = numArr
		for _, num := range allNumbers {
			n, _ := strconv.Atoi(num)
			almanac[allLetters[0]] = append(almanac[allLetters[0]], n)
		}
	}

	allSeedLocations := make([]int, 0)
	// Part 1 - Send every seed through the seed gauntlet
	for _, seed := range almanac["seeds"] {
		seedToSoil := convertSeed(seed, almanac["seed-to-soil"])
		soilToFert := convertSeed(seedToSoil, almanac["soil-to-fertilizer"])
		fertToWater := convertSeed(soilToFert, almanac["fertilizer-to-water"])
		waterToLight := convertSeed(fertToWater, almanac["water-to-light"])
		lightToTemp := convertSeed(waterToLight, almanac["light-to-temperature"])
		tempToHum := convertSeed(lightToTemp, almanac["temperature-to-humidity"])
		humToLocation := convertSeed(tempToHum, almanac["humidity-to-location"])
		allSeedLocations = append(allSeedLocations, humToLocation)
	}

	// Part 2 - Put that thang down, flip it, and reverse it
	location := 0
	seedFound := false
	for !seedFound {
		humToLocation := reverseSeed(location, almanac["humidity-to-location"])
		tempToHum := reverseSeed(humToLocation, almanac["temperature-to-humidity"])
		lightToTemp := reverseSeed(tempToHum, almanac["light-to-temperature"])
		waterToLight := reverseSeed(lightToTemp, almanac["water-to-light"])
		fertToWater := reverseSeed(waterToLight, almanac["fertilizer-to-water"])
		soilToFert := reverseSeed(fertToWater, almanac["soil-to-fertilizer"])
		seedToSoil := reverseSeed(soilToFert, almanac["seed-to-soil"])

		seedFound = theOneSeed(seedToSoil, almanac["seeds"])
		if seedFound {
			break;
		}
		location++
	}
	fmt.Println("----- Day 5 -----")
	fmt.Println(FindMin(allSeedLocations))
	fmt.Println(location)
}