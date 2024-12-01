package main

import (
	"fmt"
	"goutils"
	"math"
	"sort"
	"strings"
)

type Occurances map[int]int

func makeIdLists(allIds []string) (l1, l2 []int) {
	l1 = make([]int, 0)
	l2 = make([]int, 0)
	for _, ids := range allIds {
		var x, y int
		fmt.Sscanf(ids, "%d %d", &x, &y)
		l1 = append(l1, x)
		l2 = append(l2, y)
	}
	return l1, l2
}

func part1(input string) {
	allIds := strings.Split(input, "\n")
	list1, list2 := makeIdLists(allIds)

	sort.Slice(list1, func(i, j int) bool {
		return list1[i] < list1[j]
	})
	sort.Slice(list2, func(i, j int) bool {
		return list2[i] < list2[j]
	})

	var total float64
	for i, _ := range list1 {
		distance := list1[i] - list2[i]
		total += math.Abs(float64(distance))
	}
	fmt.Println(int(total))
}

func part2(input string) {
	allIds := strings.Split(input, "\n")
	list1, _ := makeIdLists(allIds)
	map2 := make(Occurances)

	for _, ids := range allIds {
		var x, y int
		fmt.Sscanf(ids, "%d %d", &x, &y)
		map2[y]++
	}

	total := 0
	for _, id := range list1 {
		if map2[id] != 0 {
			total += id * map2[id]
		}
	}
	fmt.Println(total)
}

func main() {
	input := goutils.FileAsString("./input.txt")
	fmt.Println("----- Part 1 -----")
	part1(input)
	fmt.Println("----- Part 2 -----")
	part2(input)
}
