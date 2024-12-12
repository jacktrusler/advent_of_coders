package goutils

import (
	"fmt"
	"log"
	"os"
	"strconv"
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

func StringArrAtoI(arr []string) []int {
	arr2 := make([]int, 0)
	for _, i := range arr {
		j, err := strconv.Atoi(i)
		if err != nil {
			panic(err)
		}
		arr2 = append(arr2, j)
	}
	return arr2
}

func PrintMap(someMap map[any]any) {
	for k, v := range someMap {
		fmt.Printf("key: %+v | value: %+v\n", k, v)
	}
}

func IntArrayToLinkedList(arr []int) *Node {
	if len(arr) == 0 {
		return nil
	}

	head := &Node{Val: arr[0]}
	current := head

	for _, val := range arr[1:] {
		newNode := &Node{Val: val}
		current.Next = newNode
		current = newNode
	}

	return head
}

// Create a Set type
type Set[T comparable] map[T]bool

func NewSetFromArr[T comparable](items []T) {
	s := NewSet[T]()
	for _, item := range items {
		s.Add(item)
	}
	fmt.Println(s)
}

func NewSet[T comparable]() Set[T] {
	return make(Set[T])
}

func (s Set[T]) Add(e T) Set[T] {
	s[e] = true
	return s
}

func (s Set[T]) Remove(e T) Set[T] {
	delete(s, e)
	return s
}

func (s Set[T]) Has(e T) bool {
	_, ok := s[e]
	return ok
}
