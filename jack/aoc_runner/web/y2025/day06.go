package y2025

import (
	"aoc/lib"
	"net/http"
	"path/filepath"
	"strconv"
	"strings"

	"github.com/starfederation/datastar-go/datastar"
)

func D6SSE(w http.ResponseWriter, r *http.Request) {
	sse := datastar.NewSSE(w, r)
	p, _ := filepath.Abs("web/y2025/input/2025-06-input.txt")
	input := lib.SplitFileOnNewLines(p)

	p1, m := 0, make(map[int][]string)
	for y, row := range input {
		flds := strings.Fields(row)
		for i, f := range flds {
			if y == len(input)-1 {
				ans := 0
				for _, v := range m[i] {
					n, _ := strconv.Atoi(v)
					if ans == 0 {
						ans = n
						continue
					}
					if f == "*" {
						ans *= n
					} else {
						ans += n
					}
				}
				p1 += ans
			}
			m[i] = append(m[i], f)
		}
	}
	p2, s := 0, ""
	for x := len(input[0]) - 1; x >= 0; x-- {
		// Treat input as 2d arr and scan top to bottom right to left until you encounter an operator
		for y := range input {
			ch := input[y][x]
			if ch == ' ' && y == len(input)-1 {
				// Make csv for parsing answer, instead of adding to array
				// Empty space at bottom indicates number to be added
				s += ","
			}
			if ch != ' ' && ch != '+' && ch != '*' {
				s += string(ch)
			}
			if ch == '*' || ch == '+' {
				s = strings.TrimPrefix(s, ",")
				ns := strings.Split(s, ",")
				a, _ := strconv.Atoi(ns[0])
				for _, v := range ns[1:] {
					n, _ := strconv.Atoi(v)
					if ch == '*' {
						a *= n
					} else {
						a += n
					}
				}
				p2 += a
				s = ""
			}
		}
	}
	sse.PatchElementTempl(BothPartsD6(p1, p2))
}
