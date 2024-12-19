package goutils

var (
	// N, E, S, W  ---  { X, Y }
	Dirs = [][]int{{0, -1}, {1, 0}, {0, 1}, {-1, 0}}
)

type Node struct {
	Val  int
	Next *Node
}

type Point struct {
	X int
	Y int
}

type Direction int

const (
	North Direction = iota
	East
	South
	West
)
