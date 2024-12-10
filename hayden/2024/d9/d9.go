package main

import (
	"fmt"
	"os"
	"strconv"
)

type fsBlock struct {
	inode int
	size  int
	start int
}

func preprocessInput(raw []byte) ([]*fsBlock, []int, []*fsBlock) {
	filesys := []*fsBlock{}
	fileList := []*fsBlock{}
	freeSpaces := []int{}
	var nextInode int = 0
	for idx, blk := range raw {
		fileSize, err := strconv.Atoi(string(blk))
		if err != nil {
			panic("not an int")
		}
		if idx%2 == 0 {
			block := &fsBlock{
				inode: nextInode,
				size:  fileSize,
				start: len(filesys),
			}
			expandedFile := make([]*fsBlock, fileSize)
			for i := 0; i < fileSize; i++ {
				expandedFile[i] = block
			}
			fileList = append(fileList, block)
			filesys = append(filesys, expandedFile...)
			nextInode++
		} else {
			block := &fsBlock{
				inode: -1,
				size:  fileSize,
				start: len(filesys),
			}
			expandedFree := make([]*fsBlock, fileSize)
			freeIndexes := make([]int, fileSize)
			start := len(filesys)
			for i := 0; i < fileSize; i++ {
				expandedFree[i] = block
				freeIndexes[i] = start + i
			}
			filesys = append(filesys, expandedFree...)
			freeSpaces = append(freeSpaces, freeIndexes...)
		}
	}
	return filesys, freeSpaces, fileList
}
func debugPrintBlocks(blocks []*fsBlock) {
	for _, block := range blocks {
		if block.inode == -1 {
			fmt.Printf(".")
		} else {
			fmt.Printf("%d", block.inode)
		}
	}
	fmt.Println("")
}
func main() {
	raw, err := os.ReadFile("input.txt")
	if err != nil {
		panic("Failed to open file ./input.txt")
	}
	filesys, freeSpaces, flist := preprocessInput(raw)
	fmt.Println(freeSpaces)
	fmt.Println(flist)
	debugPrintBlocks(filesys)
	fmt.Println("")
	fmt.Println("Start movement")
	for fileCur := len(flist) - 1; fileCur >= 0; fileCur-- {
		file := flist[fileCur]
		fmt.Println(file)
		fmt.Printf("Need %d space, expanded %d\n", file.size, len(filesys))
		for blk := range file.size {
			freeBlock := freeSpaces[0]

		}

		/* To Do: Rewrite this to pull one block off, put one back and then sort and grab */
		/*
			myReallocSpace := freeSpaces[0:file.size]
			reclaimedSpace := make([]int, file.size)
			for i := 0; i < file.size; i++ {
				reclaimedSpace[i] = file.start + i
			}
			fmt.Printf("Taking %v\n", myReallocSpace)
			fmt.Printf("Giving %v\n", reclaimedSpace)
			freeSpaces = freeSpaces[file.size:]
			fmt.Printf("Cut Free Space %v\n", freeSpaces)
			freeSpaces = append(freeSpaces, reclaimedSpace...)
			slices.Sort(freeSpaces)
			fmt.Printf("Appended reclaimed space %v\n", freeSpaces)
			for blk := range file.size {
				if file.start+blk < myReallocSpace[blk] {
					break
				}
				filesys[myReallocSpace[blk]] = file
				filesys[file.start+blk] = &fsBlock{inode: -1}
			}
			debugPrintBlocks(filesys)
		*/
	}
	debugPrintBlocks(filesys)
	/*
		start := time.Now()
		total := e1(antennas, boundary)
		duration := time.Since(start)
		fmt.Printf("On Exercise 1: %d\t(%s)\n", total, duration)
		start = time.Now()
		total = e2(antennas, boundary)
		duration = time.Since(start)
		fmt.Printf("On Exercise 2: %d\t(%s)\n", total, duration)
	*/
}
