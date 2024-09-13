package main

import (
	"testing"
)

// Terminal command for testing
// go test -vet=off -bench=. .
func BenchmarkPerformance(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Day4()
	}
}
