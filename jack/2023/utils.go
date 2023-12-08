package main

import (
	"log"
	"os"
	"strings"
)

func FileAsString(file string) string {
	content, err := os.ReadFile(file)
	if err != nil {
		log.Fatal(err)
	}

	fileAsString := string(content)
	fileAsString = strings.TrimSuffix(fileAsString, "\n")
	return fileAsString
}

func FindMin(slice []int) int {
	if len(slice) == 0 {
		return 0
	}

	min := slice[0]

	for _, value := range slice {
		if value < min {
			min = value
		}
	}

	return min
}
