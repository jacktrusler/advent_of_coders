package main

import (
	"fmt"
)

func main() {
	// var day int
	// flag.IntVar(&day, "day", 0, "Day 1 through 25")
	// flag.Parse()
	day := 9
	switch day {
	case 1:
		Day1()
	case 2:
		Day2()
	case 3:
		Day3()
	case 4:
		Day4()
	case 5:
		Day5()
	case 6:
		Day6()
	case 7:
		Day7()
	case 8:
		Day8()
	case 9:
		Day9()
	default:
		fmt.Println("Please select a day by adding a flag, e.g. -day 2")
	}
}
