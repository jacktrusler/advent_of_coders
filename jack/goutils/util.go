package goutils

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func FileAsString(file string) string {
	content, err := os.ReadFile(file)
	if err != nil {
		log.Fatal(err)
	}

	fileAsString := string(content)
	fileAsString = strings.TrimSuffix(fileAsString, "\n")
	return fileAsString
}

func StringArrAtoI(arr []string) []int {
	arr2 := make([]int, 0)
	for _, i := range arr {
		j, err := strconv.Atoi(i)
		if err != nil {
			panic(err)
		}
		arr2 = append(arr2, j)
	}
	return arr2
}

func PrintMap(someMap map[any]any) {
	for k, v := range someMap {
		fmt.Printf("key: %+v | value: %+v\n", k, v)
	}
}

func IntArrayToLinkedList(arr []int) *Node {
	if len(arr) == 0 {
		return nil
	}

	head := &Node{Val: arr[0]}
	current := head

	for _, val := range arr[1:] {
		newNode := &Node{Val: val}
		current.Next = newNode
		current = newNode
	}

	return head
}

// Create a Set type
type Set[T comparable] map[T]bool

func NewSetFromArr[T comparable](items []T) {
	s := NewSet[T]()
	for _, item := range items {
		s.Add(item)
	}
	fmt.Println(s)
}

func NewSet[T comparable]() Set[T] {
	return make(Set[T])
}

func (s Set[T]) Add(e T) Set[T] {
	s[e] = true
	return s
}

func (s Set[T]) Remove(e T) Set[T] {
	delete(s, e)
	return s
}

func (s Set[T]) Has(e T) bool {
	_, ok := s[e]
	return ok
}

// Depth First Search
func DFS(y, x int, grid []string, visited map[Coord]bool, target byte) *Coord {
	// Row: Y | Col: X
	rows := len(grid)
	cols := len(grid[0])

	if y < 0 || y >= rows || x < 0 || x >= cols || visited[Coord{Y: y, X: x}] {
		// oob or already visited!
		return nil
	}

	if grid[y][x] == target {
		return &Coord{y, x}
	}

	visited[Coord{Y: y, X: x}] = true

	for _, dir := range Dirs {
		newY, newX := y+dir[0], x+dir[1]
		if point := DFS(newY, newX, grid, visited, target); point != nil {
			return point
		}
	}

	return nil
}

// Breadth First Search
func BFS(y, x int, grid []string, target byte) *Coord {
	visited := make(map[Coord]bool)

	rows := len(grid)
	cols := len(grid[0])
	start := Coord{y, x}

	queue := []Coord{start}
	visited[start] = true

	for len(queue) > 0 {
		current := queue[0]
		queue = queue[1:]

		if grid[current.Y][current.X] == target {
			return &Coord{current.Y, current.X}
		}

		for _, dir := range Dirs {
			newY, newX := current.Y+dir[0], current.X+dir[1]
			// Check in bounds and not visited
			if newY >= 0 && newY < rows && newX >= 0 && newX < cols && !visited[Coord{newY, newX}] {
				queue = append(queue, Coord{newY, newX})
				visited[Coord{newY, newX}] = true
			}
		}
	}
	return nil
}
