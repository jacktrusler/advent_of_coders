package main

import (
	"fmt"
	"os"
	"strings"
)

type Point2D struct {
	x int
	y int
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

func processInput(raw []byte) ([][]rune, Point2D) {
	strRows := strings.Split(string(raw), "\n")
	boundary := Point2D{x: len(strRows[0]), y: len(strRows)}
	garden := make([][]rune, boundary.y)
	for rIdx, strRow := range strRows {
		gRow := make([]rune, boundary.x)
		for cIdx, cell := range strRow {
			gRow[cIdx] = cell
		}
		garden[rIdx] = gRow
	}
	return garden, boundary
}
func myAdjacents(start Point2D) []Point2D {
	return []Point2D{up(start), down(start), left(start), right(start)}
}
func adjacentFlowerSearch(start Point2D, boundary Point2D, flowerMap [][]rune, flowerPlot map[Point2D]bool, area *int, perimeter *int) {
	//fmt.Printf("Entry for (%v)\n", start)
	flowerPlot[start] = true
	directions := myAdjacents(start)
	for _, direction := range directions {
		if oob(direction, boundary) {
			//fmt.Printf("\tMove from (%v) to (%v) is oob, skipping\n", start, direction)
			*perimeter++
			continue
		}
		if flowerPlot[direction] {
			continue
		}
		if flowerMap[start.y][start.x] == flowerMap[direction.y][direction.x] {
			//fmt.Printf("\tAdjacent from (%v) is (%v) jumping\n", start, direction)
			*area++
			adjacentFlowerSearch(direction, boundary, flowerMap, flowerPlot, area, perimeter)
		} else {
			//fmt.Printf("\tBoundary from (%v) is (%v) val: %c\n", start, direction, flowerMap[direction.y][direction.x])
			*perimeter++
		}
	}
}
func main() {
	raw, err := os.ReadFile("./input.txt")
	if err != nil {
		panic("Bad File")
	}
	gardenTiles, boundary := processInput(raw)
	visited := make(map[Point2D]bool)
	totalCost := 0
	for yCur := 0; yCur < boundary.y; yCur++ {
		for xCur := 0; xCur < boundary.x; xCur++ {
			if (!visited[Point2D{x: xCur, y: yCur}]) {
				myVisits := make(map[Point2D]bool)
				perimeter := 0
				area := 1
				adjacentFlowerSearch(Point2D{x: xCur, y: yCur}, boundary, gardenTiles, myVisits, &area, &perimeter)
				totalCost += perimeter * area
				for key := range myVisits {
					visited[key] = true
				}
				fmt.Printf("Region %c starting at (%d,%d), area: %d, perimeter: %d\n", gardenTiles[yCur][xCur], xCur, yCur, area, perimeter)
			}
		}
	}
	fmt.Printf("Cost: %d\n", totalCost)
}
