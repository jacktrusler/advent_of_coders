package main

import (
	"fmt"
	"os"
	"strings"
)

const UP = 0
const RIGHT = 1
const DOWN = 2
const LEFT = 3

type Vector struct {
	x int
	y int
	a int
}

func getNextPosition(guard Vector) Vector {
	switch guard.a {
	case UP:
		return Vector{y: guard.y - 1, x: guard.x, a: guard.a}
	case RIGHT:
		return Vector{y: guard.y, x: guard.x + 1, a: guard.a}
	case DOWN:
		return Vector{y: guard.y + 1, x: guard.x, a: guard.a}
	case LEFT:
		return Vector{y: guard.y, x: guard.x - 1, a: guard.a}
	}
	panic("Uh which way do I go boss?")
}
func e1(facilityMap [][]bool, guard Vector, boundaryX int, boundaryY int) int {
	visited := make(map[string]bool)
	cordkey := fmt.Sprintf("(%d,%d)", guard.y, guard.x)
	visited[cordkey] = true
	for {
		candidatePosition := getNextPosition(guard)
		if !(candidatePosition.x >= 0 && candidatePosition.x < boundaryX && candidatePosition.y >= 0 && candidatePosition.y < boundaryY) {
			break
		}
		if facilityMap[candidatePosition.y][candidatePosition.x] {
			guard.a = (guard.a + 1) % 4
		} else {
			guard = candidatePosition
			cordkey := fmt.Sprintf("(%d,%d)", candidatePosition.y, candidatePosition.x)
			visited[cordkey] = true
		}
	}
	return len(visited)
}
func isBruhLooping(facilityMap [][]bool, guard Vector, boundaryX int, boundaryY int) bool {
	escapedCagie := false
	for cycles := 0; cycles < (boundaryX * boundaryY); cycles++ {
		candidatePosition := getNextPosition(guard)
		if !(candidatePosition.x >= 0 && candidatePosition.x < boundaryX && candidatePosition.y >= 0 && candidatePosition.y < boundaryY) {
			escapedCagie = true
			break
		}
		if facilityMap[candidatePosition.y][candidatePosition.x] {
			guard.a = (guard.a + 1) % 4
		} else {
			guard = candidatePosition
		}
	}
	return escapedCagie
}
func e2(facilityMap [][]bool, guard Vector, boundaryX int, boundaryY int) int {
	nonEscapes := 0
	for rowIdx, facRow := range facilityMap {
		for colIdx, cell := range facRow {
			if !cell {
				facilityMap[rowIdx][colIdx] = true
				didEscape := isBruhLooping(facilityMap, Vector{guard.x, guard.y, guard.a}, boundaryX, boundaryY)
				if !didEscape {
					nonEscapes += 1
				}
				facilityMap[rowIdx][colIdx] = false
			}
		}
	}
	return nonEscapes
}
func main() {
	raw, err := os.ReadFile("input.txt")
	if err != nil {
		panic("Failed to open file ./input.txt")
	}
	split := strings.Split(string(raw), "\r\n")
	facilityMap := make([][]bool, len(split))
	guardVec := Vector{0, 0, LEFT}
	boundaryX := len(split[0])
	boundaryY := len(split)
	for YCur, row := range split {
		facilityRow := make([]bool, boundaryX)
		for XCur, cell := range row {
			switch cell {
			case '#':
				facilityRow[XCur] = true
			case '^':
				guardVec.x = XCur
				guardVec.y = YCur
				guardVec.a = UP
			case '>':
				guardVec.x = XCur
				guardVec.y = YCur
				guardVec.a = RIGHT
			case 'v':
				guardVec.x = XCur
				guardVec.y = YCur
				guardVec.a = DOWN
			case '<':
				guardVec.x = XCur
				guardVec.y = YCur
				guardVec.a = LEFT
			}
			facilityMap[YCur] = facilityRow
		}
	}
	total := e1(facilityMap, guardVec, boundaryX, boundaryY)
	fmt.Printf("On Exercise 1: %d\n", total)
	total = e2(facilityMap, guardVec, boundaryX, boundaryY)
	fmt.Printf("On Exercise 2: %d\n", total)
}
