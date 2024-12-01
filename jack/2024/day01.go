package main

import (
	"fmt"
	"goutils"
	"math"
	"sort"
	"strings"
)

type Occurances map[int]int

func makeIdListsAndMaps(allIds []string) (l1, l2 []int, m1, m2 Occurances) {
	l1 = make([]int, 0)
	l2 = make([]int, 0)
	m1 = make(Occurances)
	m2 = make(Occurances)
	for _, ids := range allIds {
		var id1, id2 int
		fmt.Sscanf(ids, "%d %d", &id1, &id2)
		l1 = append(l1, id1)
		l2 = append(l2, id2)
		m1[id1]++
		m2[id2]++
	}
	return l1, l2, m1, m2
}

func part1(input string) {
	allIds := strings.Split(input, "\n")
	list1, list2, _, _ := makeIdListsAndMaps(allIds)

	sort.Slice(list1, func(i, j int) bool {
		return list1[i] < list1[j]
	})
	sort.Slice(list2, func(i, j int) bool {
		return list2[i] < list2[j]
	})

	var total float64
	for i := range list1 {
		distance := list1[i] - list2[i]
		total += math.Abs(float64(distance))
	}
	fmt.Println(int(total))
}

func part2(input string) {
	allIds := strings.Split(input, "\n")
	list1, _, _, map2 := makeIdListsAndMaps(allIds)

	total := 0
	for _, id := range list1 {
		if map2[id] != 0 {
			total += id * map2[id]
		}
	}
	fmt.Println(total)
}

func Day1() {
	input := goutils.FileAsString("./input/day01.txt")
	fmt.Println("----- Part 1 -----")
	part1(input)
	fmt.Println("----- Part 2 -----")
	part2(input)
}
