package main

import (
	"testing"
)

func BenchmarkPerformance(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Day1()
		Day2()
		Day3()
		Day4()
	}
}
