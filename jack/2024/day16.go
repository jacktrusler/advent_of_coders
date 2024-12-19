package main

import (
	"fmt"
	u "goutils"
	"math"
	"slices"
	"strings"
)

type node struct {
	x   int
	y   int
	dir u.Direction
}

type qItem struct {
	point    node
	priority int
	index    int
}

func findStartEnd(maze []string) (start node, end node) {
	for y, line := range maze {
		for x, r := range line {
			if r == 'S' {
				start = node{x: x, y: y, dir: u.East}
			}
			if r == 'E' {
				end = node{x: x, y: y}
			}
		}
	}
	return start, end
}

func isValid(nx, ny int, maze []string) bool {
	return nx >= 0 && ny >= 0 && nx < len(maze) && ny < len(maze[0]) && maze[ny][nx] != '#'
}

func findPath(start, end node, maze []string) []node {
	visited := make(map[string]bool)
	dist := make(map[string]int)
	parent := make(map[node]node)

	// set all points distance to infinity
	for y := range maze {
		for x := range maze[y] {
			anyPoint := fmt.Sprintf("x%d,y%d", x, y)
			dist[anyPoint] = math.MaxInt64
		}
	}

	startStr := fmt.Sprintf("x%d,y%d", start.x, start.y)
	dist[startStr] = 0

	// create priority queue
	pQueue := []qItem{{point: start, priority: 0}}

	// walk nodes
	for len(pQueue) > 0 {
		currentP := pQueue[0].point
		pQueue = pQueue[1:]

		// found end, rebuild path
		if currentP.x == end.x && currentP.y == end.y {
			var path []node
			for at := end; at != start; at = parent[at] {
				path = append([]node{at}, path...)
			}
			return path
		}

		currStr := fmt.Sprintf("x%d,y%d", currentP.x, currentP.y)
		visited[currStr] = true

		for i, dir := range u.Dirs {
			neighbor := node{x: currentP.x + dir[0], y: currentP.y + dir[1], dir: u.Direction(i)}
			newDist := dist[currStr] + 1

			if isValid(neighbor.x, neighbor.y, maze) {
				neighborStr := fmt.Sprintf("x%d,y%d", neighbor.x, neighbor.y)
				if newDist < dist[neighborStr] {
					dist[neighborStr] = newDist

					if neighbor.dir != currentP.dir {
						dist[neighborStr] += 1000
					}

					parent[neighbor] = currentP
					pQueue = append(pQueue, qItem{point: neighbor, priority: newDist})
					slices.SortFunc(pQueue, func(a, b qItem) int {
						return a.priority - b.priority
					})
				}
			}
		}
	}
	return nil
}

func day16part1(maze []string) {

	start, end := findStartEnd(maze)
	path := findPath(start, end, maze)

	turns := 0
	dir := u.East
	for _, step := range path {
		if step.dir != dir {
			turns += 1
			dir = step.dir
		}
	}
	fmt.Println(turns*1000 + len(path))

}

func day16part2(maze []string) {

}

func Day16() {
	input := u.FileAsString("./input/2024-16-input.txt")
	maze := strings.Split(input, "\n")

	fmt.Println("----- Part 1 -----")
	day16part1(maze)
	fmt.Println("----- Part 2 -----")
	// day16part2(maze)
}
