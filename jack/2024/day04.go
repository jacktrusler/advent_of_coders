package main

import (
	"fmt"
	"goutils"
	"strings"
)

var (
	ws []string
)

func makeSusSearch(input string) {
	lines := strings.Split(input, "\n")
	// pad with amogus
	runeArr := make([]rune, len(lines[0])+2)
	// sus
	for i := range runeArr {
		runeArr[i] = '0'
	}

	wordSearch := make([]string, len(lines)+2)
	wordSearch[0] = string(runeArr)
	wordSearch[len(lines)+1] = string(runeArr)
	fmt.Println(wordSearch[0])
	for i, line := range lines {
		line = "0" + line + "0"
		wordSearch[i+1] = line
		fmt.Println(line)
	}
	fmt.Println(wordSearch[len(lines)+1])
	ws = wordSearch
}

func boggleStyle(y, x int, word string, total *int) {
	//exit conditions
	if ws[y][x] == '0' {
		return
	}
	if word == "XA" || word == "XX" || word == "XS" || word == "XMS" || word == "XMX" || word == "XMM" {
		return
	}
	if len(word) >= 4 {
		return
	}

	word = word + string(ws[y][x])
	if word == "XMAS" {
		*total++
		return
	}

	// W
	boggleStyle(y, x-1, word, total)
	// NW
	boggleStyle(y-1, x-1, word, total)
	// N
	boggleStyle(y-1, x, word, total)
	// NE
	boggleStyle(y-1, x+1, word, total)
	// E
	boggleStyle(y, x+1, word, total)
	// SE
	boggleStyle(y+1, x+1, word, total)
	// S
	boggleStyle(y+1, x, word, total)
	// SW
	boggleStyle(y+1, x-1, word, total)

	return
}

func day4part1(input string) {
	makeSusSearch(input)
	var total int
	for y := 1; y < len(ws)-2; y++ {
		for x, rune := range ws[y] {
			var runningTotal int
			if rune == 'X' {
				boggleStyle(y, x, "", &runningTotal)
				runes := []byte(ws[y])
				runes[x] = '0'
				ws[y] = string(runes)
				total += runningTotal
				runningTotal = 0
			}
		}
	}
	fmt.Println(total)

}

func day4part2(input string) {
}

func Day4() {
	input := goutils.FileAsString("./input/04-example.txt")
	fmt.Println("----- Part 1 -----")
	day4part1(input)
	fmt.Println("----- Part 2 -----")
	day4part2(input)
}
