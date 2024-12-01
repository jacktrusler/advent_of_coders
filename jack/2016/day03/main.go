package main

import (
	"aoc2016/util"
	"fmt"
	"strings"
)

func part1(input string) {
	triangles := strings.Split(input, "\n")
	var s1, s2, s3 int
	validTriangles := 0
	for _, triangle := range triangles {
		fmt.Sscan(triangle, &s1, &s2, &s3)
		if isValidTriangle(s1, s2, s3) {
			validTriangles++
		}
	}
	fmt.Println(validTriangles)
}

func part2(input string) {
	// make triangles into a grid
	triangles := strings.Split(input, "\n")
	var s1, s2, s3, s4, s5, s6, s7, s8, s9 int

	validTriangles := 0
	for i := 0; i < len(triangles); i += 3 {
		fmt.Sscan(triangles[i], &s1, &s2, &s3)
		fmt.Sscan(triangles[i+1], &s4, &s5, &s6)
		fmt.Sscan(triangles[i+2], &s7, &s8, &s9)

		if isValidTriangle(s1, s4, s7) {
			validTriangles++
		}
		if isValidTriangle(s2, s5, s8) {
			validTriangles++
		}
		if isValidTriangle(s3, s6, s9) {
			validTriangles++
		}
	}
	fmt.Println(validTriangles)
}

func isValidTriangle(s1, s2, s3 int) bool {
	return s1+s2 > s3 && s2+s3 > s1 && s3+s1 > s2
}

func main() {
	input := util.FileAsString("./input.txt")
	fmt.Println("----- Part 1 -----")
	part1(input)
	fmt.Println("----- Part 2 -----")
	part2(input)
}
