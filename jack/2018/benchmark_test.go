package main

import (
	"os"
	"testing"
)

func BenchmarkDay01(b *testing.B) {
	input, err := os.ReadFile("./input/2018-01-input.txt")
	if err != nil {
		return
	}
	for b.Loop() {
		Day01(input)
	}
}
func BenchmarkDay01AtoI(b *testing.B) {
	f, _ := os.Open("./input/2018-01-input.txt")
	defer f.Close()
	for b.Loop() {
		Day01AtoI(f)
	}
}
