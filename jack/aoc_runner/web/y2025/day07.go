package y2025

import (
	"aoc/lib"
	"fmt"
	"net/http"
	"path/filepath"

	"github.com/starfederation/datastar-go/datastar"
)

func DFSplitter2(x, y int, grid []string, target byte, timelines map[lib.Point]int) int {
	rows := len(grid)
	cols := len(grid[0])

	// Hit a splitter that has already been evaluated
	if val, exists := timelines[lib.Point{Y: y, X: x}]; exists {
		return val
	}

	// Only 1 timeline for running oob
	if y < 0 || y >= rows || x < 0 || x >= cols {
		return 1
	}

	if grid[y][x] == target {
		left := x - 1
		right := x + 1
		leftTimelines := DFSplitter2(left, y, grid, '^', timelines)
		rightTimelines := DFSplitter2(right, y, grid, '^', timelines)

		timelines[lib.Point{Y: y, X: x}] = leftTimelines + rightTimelines
		return leftTimelines + rightTimelines
	}

	//Only travel South
	newY := y + 1
	return DFSplitter2(x, newY, grid, target, timelines)
}

func DFSplitter(x, y int, grid []string, target byte, timesSplit *int, visited map[lib.Point]bool) {
	rows := len(grid)
	cols := len(grid[0])

	if y < 0 || y >= rows || x < 0 || x >= cols || visited[lib.Point{Y: y, X: x}] {
		// oob
		return
	}

	if grid[y][x] == target {
		visited[lib.Point{Y: y, X: x}] = true
		*timesSplit++

		left := x - 1
		right := x + 1
		DFSplitter(left, y, grid, '^', timesSplit, visited)
		DFSplitter(right, y, grid, '^', timesSplit, visited)
		return
	}

	//Only travel South
	newY := y + 1

	DFSplitter(x, newY, grid, target, timesSplit, visited)
}

func D7SSE(w http.ResponseWriter, r *http.Request) {
	sse := datastar.NewSSE(w, r)
	inputPath, err := filepath.Abs("web/y2025/input/2025-07-input.txt")
	if err != nil {
		fmt.Println("Error finding filepath")
		return
	}
	p1 := 0
	rows := lib.SplitFileOnNewLines(inputPath)
	visited := make(map[lib.Point]bool)
	timelines := make(map[lib.Point]int)

	for y, row := range rows {
		for x := range row {
			// Start at 'S' only travel down until you hit '^'
			if rows[y][x] == 'S' {
				DFSplitter(x, y, rows, '^', &p1, visited)
				p2 := DFSplitter2(x, y, rows, '^', timelines)
				sse.PatchElementTempl(BothPartsD7(p1, p2))
				return
			}
		}
	}

}
