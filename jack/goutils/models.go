package goutils

var (
	// N, E, S, W  ---  { X, Y }
	Dirs = [][]int{{0, -1}, {1, 0}, {0, 1}, {-1, 0}}
)

type Node struct {
	Val  int
	Next *Node
}

type Coord struct {
	X int
	Y int
}
