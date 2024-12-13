package goutils

var (
	// N, E, S, W  ---  { Y, X }
	Dirs = [][]int{{-1, 0}, {0, 1}, {1, 0}, {0, -1}}
)

type Node struct {
	Val  int
	Next *Node
}

type Coord struct {
	Y int
	X int
}
