package main

import (
	"aoc2015/pkg/utils"
	"fmt"
	"sort"
	"strings"
)

func Day9() {
	fmt.Println("Running day 9...")
	ans1 := day9Part1(utils.ReadFile("./data/day09.txt"))
	fmt.Println("--- Part 1 ---")
	fmt.Println(ans1)

	ans2 := day9Part2(utils.ReadFile("./data/day09.txt"))
	fmt.Println("--- Part 2 ---")
	fmt.Println(ans2)
}

func day9Part1(input string) int {
	edgeMap, nodes, err := generateGraph(input)
	if err != nil {
		return 0
	}
	distArr := generateDistances(nodes, edgeMap)
	sort.Slice(distArr, func(i, j int) bool {
		return distArr[i] < distArr[j]
	})
	return distArr[0]
}

func day9Part2(input string) int {
	edgeMap, nodes, err := generateGraph(input)
	if err != nil {
		return 0
	}
	distArr := generateDistances(nodes, edgeMap)
	sort.Slice(distArr, func(i, j int) bool {
		return distArr[i] > distArr[j]
	})
	return distArr[0]
}

type Edge struct {
	from string
	to   string
	dist int
}

type Nodes map[string]bool
type Edges map[string][]Edge

func generateGraph(input string) (Edges, Nodes, error) {
	edgeMap := make(Edges)
	nodes := make(Nodes)
	var from, to string
	var dist int
	for _, line := range strings.Split(input, "\n") {
		n, err := fmt.Sscanf(line, "%s to %s = %d", &from, &to, &dist)

		if err != nil || n != 3 {
			fmt.Println("Problem scanning string: ", err)
			return nil, nil, err
		}

		// {from: Dublin, to: London, dist: 464}
		// {from: Dublin, to: Belfast, dist: 141}
		// ...
		edgeMap[from] = append(edgeMap[from], Edge{
			from: from,
			to:   to,
			dist: dist,
		})
		edgeMap[to] = append(edgeMap[to], Edge{
			from: to,
			to:   from,
			dist: dist,
		})
		nodes[from] = true
		nodes[to] = true
	}
	return edgeMap, nodes, nil
}

type boolMap map[string]bool

func generateDistances(nodeMap Nodes, edgeMap Edges) []int {
	paths := []int{}

	for from := range nodeMap {
		paths = append(paths, visitNode(edgeMap, from, make(boolMap), 0)...)
	}

	return paths
}

func visitNode(edges Edges, from string, visited boolMap, sum int) []int {
	// Copy the visited array so recursion doesn't
	// reference the only visited map in memory
	newVisited := make(boolMap)
	for key, value := range visited {
		newVisited[key] = value
	}

	newVisited[from] = true

	if len(newVisited) == len(edges) {
		return []int{sum}
	}

	paths := []int{}
	for _, edge := range edges[from] {
		if !newVisited[edge.to] {
			paths = append(paths, visitNode(edges, edge.to, newVisited, sum+edge.dist)...)
		}
	}

	return paths
}
