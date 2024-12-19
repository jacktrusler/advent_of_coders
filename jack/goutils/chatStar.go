package goutils

import (
	"container/heap"
	"math"
)

type ChatNode struct {
	X, Y     int
	Cost     float64
	Priority float64
	Parent   *ChatNode
}

type ChatPriorityQueue []*ChatNode

func (pq ChatPriorityQueue) Len() int { return len(pq) }

func (pq ChatPriorityQueue) Less(i, j int) bool {
	return pq[i].Priority < pq[j].Priority
}

func (pq ChatPriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
}

func (pq *ChatPriorityQueue) Push(x interface{}) {
	node := x.(*ChatNode)
	*pq = append(*pq, node)
}

func (pq *ChatPriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	node := old[n-1]
	*pq = old[0 : n-1]
	return node
}

func chatHeuristic(a, b ChatNode) float64 {
	return math.Abs(float64(a.X-b.X)) + math.Abs(float64(a.Y-b.Y))
}

func chatNeighbors(node ChatNode, grid [][]int) []ChatNode {
	directions := []struct{ dx, dy int }{
		{-1, 0}, {1, 0}, {0, -1}, {0, 1},
	}
	var result []ChatNode
	for _, dir := range directions {
		x, y := node.X+dir.dx, node.Y+dir.dy
		if x >= 0 && y >= 0 && x < len(grid) && y < len(grid[0]) && grid[y][x] == 0 {
			result = append(result, ChatNode{X: x, Y: y})
		}
	}
	return result
}

func ChatStar(start, goal ChatNode, grid [][]int) []ChatNode {
	openSet := &ChatPriorityQueue{}
	heap.Init(openSet)
	start.Priority = chatHeuristic(start, goal)
	heap.Push(openSet, &start)

	visited := make(map[ChatNode]bool)
	costSoFar := make(map[ChatNode]float64)
	costSoFar[start] = 0

	for openSet.Len() > 0 {
		current := heap.Pop(openSet).(*ChatNode)

		if current.X == goal.X && current.Y == goal.Y {
			var path []ChatNode
			for n := current; n != nil; n = n.Parent {
				path = append(path, *n)
			}
			// Reverse the path
			for i, j := 0, len(path)-1; i < j; i, j = i+1, j-1 {
				path[i], path[j] = path[j], path[i]
			}
			return path
		}

		visited[*current] = true

		for _, neighbor := range chatNeighbors(*current, grid) {
			if visited[neighbor] {
				continue
			}

			newCost := costSoFar[*current] + 1 // Assuming uniform cost for simplicity
			if oldCost, ok := costSoFar[neighbor]; !ok || newCost < oldCost {
				costSoFar[neighbor] = newCost
				neighbor.Cost = newCost
				neighbor.Priority = newCost + chatHeuristic(neighbor, goal)
				neighbor.Parent = current
				heap.Push(openSet, &neighbor)
			}
		}
	}
	return nil
}
