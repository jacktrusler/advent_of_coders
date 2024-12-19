package goutils

import "container/heap"

// x,y coords of node
//
// g distance from node to start
//
// h distance from node to target, heuristic cost
//
// f = g + h
type AStarNode struct {
	X, Y     int
	priority int
	cost     int
	parent   *AStarNode
}

type PriorityQueue []*AStarNode
type Visited map[AStarNode]bool

func (pq PriorityQueue) Less(i, j int) bool {
	return pq[i].priority < pq[j].priority
}

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
}

func (pq *PriorityQueue) Push(x interface{}) {
	node := x.(*AStarNode)
	*pq = append(*pq, node)
}

func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	node := old[n-1]
	*pq = old[0 : n-1]
	return node
}

func neighbors(node AStarNode, grid []string) []AStarNode {
	var result []AStarNode
	for _, dir := range Dirs {
		nx, ny := node.X+dir[0], node.Y+dir[1]
		if nx >= 0 && ny >= 0 && nx < len(grid) && ny < len(grid[0]) && (grid[ny][nx] == '.' || grid[ny][nx] == 'E') {
			result = append(result, AStarNode{X: nx, Y: ny})
		}
	}
	return result
}

func heuristic(start, end AStarNode) int {
	return ManhattanD(start.X, end.X, start.Y, end.Y)
}

func Astar(start AStarNode, end AStarNode, grid []string) []AStarNode {
	priorityQueue := &PriorityQueue{}
	heap.Init(priorityQueue)
	heap.Push(priorityQueue, &start)
	visited := make(Visited)
	costSoFar := make(map[AStarNode]int)
	costSoFar[start] = 0

	for priorityQueue.Len() > 0 {
		current := heap.Pop(priorityQueue).(*AStarNode)

		// If you found the end, rebuild the path
		if current.X == end.X && current.Y == end.Y {
			path := []AStarNode{}
			for n := current; n != nil; n = n.parent {
				path = append(path, *n)
			}

			// Reverse the path end -> start becomes start -> end
			for i, j := 0, len(path)-1; i < j; i, j = i+1, j-1 {
				path[i], path[j] = path[j], path[i]
			}
			return path
		}

		visited[*current] = true

		for _, neighbor := range neighbors(*current, grid) {
			if visited[neighbor] {
				continue
			}

			newCost := costSoFar[*current] + 1 // add 1 for new cost, distance from start

			if oldCost, ok := costSoFar[neighbor]; !ok || newCost < oldCost {
				costSoFar[neighbor] = newCost
				neighbor.priority = newCost + heuristic(neighbor, end)
				neighbor.parent = current
				heap.Push(priorityQueue, &neighbor)
			}
		}
	}
	return nil
}
