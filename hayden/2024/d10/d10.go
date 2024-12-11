package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Point2D struct {
	x int
	y int
}

func processInput(raw []byte) ([][]int, Point2D, []Point2D, map[Point2D]int) {
	strRows := strings.Split(string(raw), "\n")
	maxY := len(strRows)
	maxX := len(strRows[0])
	boundary := Point2D{x: maxX, y: maxY}
	topoMap := make([][]int, maxY)
	startPoints := make([]Point2D, 0)
	endPoints := make(map[Point2D]int)
	for yCur, strRow := range strRows {
		row := make([]int, maxX)
		for xCur, cellRune := range strRow {
			cell, err := strconv.Atoi(string(cellRune))
			if err != nil && cellRune != '.' {
				panic("Bad value in input, NaN")
			}
			if cell == 0 && cellRune != '.' {
				startPoints = append(startPoints, Point2D{x: xCur, y: yCur})
			}
			if cell == 9 && cellRune != '.' {
				endPoints[Point2D{x: xCur, y: yCur}] = 0
			}
			if cellRune == '.' {
				row[xCur] = -1
			} else {
				row[xCur] = cell
			}
		}
		topoMap[yCur] = row
	}
	return topoMap, boundary, startPoints, endPoints
}
func oob(p Point2D, b Point2D) bool {
	return !(p.x >= 0 && p.y >= 0 && p.x < b.x && p.y < b.y)
}
func up(start Point2D) Point2D {
	return Point2D{x: start.x, y: start.y + 1}

}
func down(start Point2D) Point2D {
	return Point2D{x: start.x, y: start.y - 1}
}
func left(start Point2D) Point2D {
	return Point2D{x: start.x - 1, y: start.y}
}
func right(start Point2D) Point2D {
	return Point2D{x: start.x + 1, y: start.y}
}
func hikeTrail(start Point2D, topoMap [][]int, boundary Point2D, endPoints map[Point2D]int) (int, int) {
	rating := hike(up(start), start, topoMap, boundary, endPoints) + hike(down(start), start, topoMap, boundary, endPoints) + hike(left(start), start, topoMap, boundary, endPoints) + hike(right(start), start, topoMap, boundary, endPoints)
	score := 0
	for pt, count := range endPoints {
		if count > 0 {
			endPoints[pt] = 0
			score++
		}
	}
	return score, rating
}
func hike(position Point2D, previous Point2D, topoMap [][]int, boundary Point2D, endPoints map[Point2D]int) int {
	if oob(position, boundary) {
		return 0
	}
	if topoMap[position.y][position.x]-topoMap[previous.y][previous.x] != 1 {
		return 0
	}
	if topoMap[position.y][position.x] == 9 {
		endPoints[position] += 1
		return 1
	}
	return hike(up(position), position, topoMap, boundary, endPoints) + hike(down(position), position, topoMap, boundary, endPoints) + hike(left(position), position, topoMap, boundary, endPoints) + hike(right(position), position, topoMap, boundary, endPoints)
}

func main() {
	raw, err := os.ReadFile("./input.txt")
	if err != nil {
		panic("Bad File")
	}
	totalScore := 0
	totalRating := 0
	topoMap, boundary, startPoints, endPoints := processInput(raw)
	for _, point := range startPoints {
		trlScore, trlRating := hikeTrail(point, topoMap, boundary, endPoints)
		totalScore += trlScore
		totalRating += trlRating
	}
	fmt.Printf("Exercise 1: %d\n", totalScore)
	fmt.Printf("Exercise 2: %d\n", totalRating)
}
