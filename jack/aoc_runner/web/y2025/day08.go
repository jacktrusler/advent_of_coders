package y2025

import (
	"aoc/lib"
	"fmt"
	"math"
	"net/http"
	"path/filepath"
	"strings"

	"github.com/starfederation/datastar-go/datastar"
)

func D8SSE(w http.ResponseWriter, r *http.Request) {
	sse := datastar.NewSSE(w, r)
	p, _ := filepath.Abs("web/y2025/input/2025-08-test-input.txt")
	input := lib.SplitFileOnNewLines(p)

	// box := 0
	// minDis := math.Inf(1)
	for i, coords := range input {
		xyzArr := strings.Split(coords, ",")
		p := &lib.Parser{}
		x1 := p.Atoi(xyzArr[0])
		y1 := p.Atoi(xyzArr[1])
		z1 := p.Atoi(xyzArr[2])
		if p.Err != nil {
			fmt.Println("Error parsing coordinates")
			return
		}
		for j := i + 1; j < len(input); j++ {
			xyzArr := strings.Split(input[j], ",")
			p := &lib.Parser{}
			x2 := p.Atoi(xyzArr[0])
			y2 := p.Atoi(xyzArr[1])
			z2 := p.Atoi(xyzArr[2])
			// calculate euclidian distance
			dX := float64(x2 - x1)
			dY := float64(y2 - y1)
			dZ := float64(z2 - z1)
			// sum the squares then take the sqrt
			sum := math.Pow(dX, 2) + math.Pow(dY, 2) + math.Pow(dZ, 2)
			dis := math.Sqrt(sum)
			// build all distances and store
			// 0-1 333
			// 0-2 555
			fmt.Println(dis)
		}
	}
	p1 := 0
	p2 := 0
	sse.PatchElementTempl(BothPartsD8(p1, p2))
}
