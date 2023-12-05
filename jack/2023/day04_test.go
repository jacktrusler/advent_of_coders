package main

import (
	"testing"
)

func BenchmarkDay4(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Day4()
	}
}
