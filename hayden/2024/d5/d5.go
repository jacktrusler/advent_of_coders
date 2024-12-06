package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func e1(lines []string) int {
	runningTotal := 0
	deps := make(map[int][]int)
	rulesdone := false
	for _, row := range lines {
		if len(row) == 0 {
			rulesdone = true
			continue
		}
		if !rulesdone {
			rulesplit := strings.Split(row, "|")
			if len(rulesplit) != 2 {
				panic("We're still reading rules over here boss, but you sent something that doesn't look like <x>|<y>")
			}
			lh, lhErr := strconv.Atoi(rulesplit[0])
			rh, rhErr := strconv.Atoi(rulesplit[1])
			if lhErr != nil || rhErr != nil {
				panic("Unable to parse one of the ints in the rule")
			}
			myDeps := deps[lh]
			if myDeps == nil {
				myDeps = []int{rh}
			} else {
				myDeps = append(myDeps, rh)
			}
			deps[lh] = myDeps
		} else {
			// Parse page order into int arry
			pagesStr := strings.Split(row, ",")
			pages := make([]int, len(pagesStr))
			for idx, pageStr := range pagesStr {
				page, err := strconv.Atoi(pageStr)
				if err != nil {
					panic("Page order consists of non-integer input. Expected <x>,<y>...")
				}
				pages[idx] = page
			}
			//Now iterate thru page arry. Each step pull my deps from dependency table.
			dependencyViolation := false
			for checkPageIndex, page := range pages {
				pageDeps := deps[page]
				if pageDeps == nil {
					continue
				}
				for _, dependency := range pageDeps {
					dependencyLocated := false
					for pageIndex := checkPageIndex - 1; pageIndex >= 0 && !dependencyLocated; pageIndex-- {
						if pages[pageIndex] == dependency {
							dependencyLocated = true
						}
					}
					if dependencyLocated {
						dependencyViolation = true
					}
				}
			}
			if !dependencyViolation {
				runningTotal += pages[len(pages)/2]
			}
		}
	}
	return runningTotal
}
func e2(lines []string) int {
	runningTotal := 0
	deps := make(map[int][]int)
	rulesdone := false
	violators := make([][]int, 0)
	for _, row := range lines {
		if len(row) == 0 {
			rulesdone = true
			continue
		}
		if !rulesdone {
			rulesplit := strings.Split(row, "|")
			if len(rulesplit) != 2 {
				panic("We're still reading rules over here boss, but you sent something that doesn't look like <x>|<y>")
			}
			lh, lhErr := strconv.Atoi(rulesplit[0])
			rh, rhErr := strconv.Atoi(rulesplit[1])
			if lhErr != nil || rhErr != nil {
				panic("Unable to parse one of the ints in the rule")
			}
			myDeps := deps[lh]
			if myDeps == nil {
				myDeps = []int{rh}
			} else {
				myDeps = append(myDeps, rh)
			}
			deps[lh] = myDeps
		} else {
			// Parse page order into int arry
			pagesStr := strings.Split(row, ",")
			pages := make([]int, len(pagesStr))
			for idx, pageStr := range pagesStr {
				page, err := strconv.Atoi(pageStr)
				if err != nil {
					panic("Page order consists of non-integer input. Expected <x>,<y>...")
				}
				pages[idx] = page
			}
			//Now iterate thru page arry. Each step pull my deps from dependency table.
			dependencyViolation := false
			for checkPageIndex, page := range pages {
				pageDeps := deps[page]
				if pageDeps == nil {
					continue
				}
				for _, dependency := range pageDeps {
					dependencyLocated := false
					for pageIndex := checkPageIndex - 1; pageIndex >= 0 && !dependencyLocated; pageIndex-- {
						if pages[pageIndex] == dependency {
							dependencyLocated = true
						}
					}
					if dependencyLocated {
						dependencyViolation = true
					}
				}
			}
			if dependencyViolation {
				violators = append(violators, pages)
			}
		}
	}
	for _, violated := range violators {
		for checkPageIndex := 0; checkPageIndex < len(violated); checkPageIndex++ {
			page := violated[checkPageIndex]
			pageDeps := deps[page]
			if pageDeps == nil {
				continue
			}
			for _, dependency := range pageDeps {
				dependencyLocated := false
				for pageIndex := checkPageIndex - 1; pageIndex >= 0 && !dependencyLocated; pageIndex-- {
					if violated[pageIndex] == dependency {
						violated = insertAfter(violated, pageIndex, checkPageIndex)
						checkPageIndex = 0
					}
				}
			}
		}
		runningTotal += violated[len(violated)/2]
	}
	return runningTotal
}
func insertAfter(pages []int, movIndex int, afterIndex int) []int {
	movVal := pages[movIndex]
	pages = append(pages[:movIndex], pages[movIndex+1:]...)
	rhArr := []int{movVal}
	pages = append(pages[:afterIndex], append(rhArr, pages[afterIndex:]...)...)
	return pages
}
func main() {
	raw, err := os.ReadFile("input.txt")
	if err != nil {
		panic("Failed to open file ./input.txt")
	}
	split := strings.Split(string(raw), "\r\n")
	total := e1(split)
	fmt.Printf("On Exercise 1: %d\n", total)
	total = e2(split)
	fmt.Printf("On Exercise 2: %d\n", total)
}
