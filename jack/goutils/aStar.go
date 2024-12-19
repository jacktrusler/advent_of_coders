package goutils

type ANode struct {
	x, y   int
	h      int
	g      int
	f      int
	parent *ANode
}

type PriorityQueue []*ANode

func (pq PriorityQueue) Less(i, j int) bool {
	return pq[i].priority < pq[j].priority
}

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
}

func (pq *PriorityQueue) Push(x interface{}) {
	node := x.(*ANode)
	*pq = append(*pq, node)
}

func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	node := old[n-1]
	*pq = old[0 : n-1]
	return node
}

func heuristic(start, end ANode) int {
	return ManhattanD(start.x, end.x, start.y, end.y)
}

func Astar() {
}
