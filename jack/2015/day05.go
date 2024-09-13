package main

import (
	"aoc2015/pkg/utils"
	"fmt"
	"strings"

	"github.com/dlclark/regexp2"
)

func Day5() {
	fileAsString := utils.FileAsString("./data/day05.txt")
	stringArr := strings.Split(fileAsString, "\n")

	// use the regexp2 library because Go standard lib uses
	// the RE2 engine, which doesn't contain backreferences
	nice := 0
	re1 := regexp2.MustCompile(`[aeiou].*[aeiou].*[aeiou]`, 0)
	re2 := regexp2.MustCompile(`(\w)\1`, 0)
	re3 := regexp2.MustCompile(`(ab|cd|pq|xy)`, 0)

	for _, str := range stringArr {
		match, _ := re1.MatchString(str)
		match2, _ := re2.MatchString(str)
		match3, _ := re3.MatchString(str)

		if match && match2 && !match3 {
			nice++
		}
	}
	fmt.Println("Part 1, Nice strings: ", nice)

	// Part 2
	rule4 := `(.).(\1)`
	rule5 := `(..).*(\1)`
	re4 := regexp2.MustCompile(rule4, 0)
	re5 := regexp2.MustCompile(rule5, 0)

	nice = 0
	for _, str := range stringArr {
		match, _ := re4.MatchString(str)
		match2, _ := re5.MatchString(str)
		if match && match2 {
			nice++
		}
	}
	fmt.Println("Part 2, Nice strings: ", nice)
}
