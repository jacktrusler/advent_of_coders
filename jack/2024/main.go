package main

import (
	"fmt"
	"log"
	"os"
	"runtime/pprof"
)

func main() {
	f, err := os.Create("cpu_profile.prof")
	if err != nil {
		log.Fatal("could not create CPU profile:", err)
	}
	pprof.StartCPUProfile(f)
	defer pprof.StopCPUProfile()

	// -----------
	Day14()
	// -----------

	fmt.Println("CPU profile saved to cpu_profile.prof")
}
