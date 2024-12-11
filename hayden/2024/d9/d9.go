package main

import (
	"fmt"
	"os"
	"slices"
	"strconv"
)

type fsBlock struct {
	inode int
	size  int
	start int
}

func preprocessInputForNonContiguous(raw []byte) ([]*fsBlock, []int, []*fsBlock) {
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
			//fmt.Printf(".")
		} else {
			//fmt.Printf("%d", block.inode)
		}
	}
	//fmt.Println("")
}
func calculatechecksum(blocks []*fsBlock) {
	checksum := 0
	for idx, block := range blocks {
		if block.inode == -1 {
			break
		}
		checksum += block.inode * idx
	}
	//fmt.Printf("Check Sum %d\n", checksum)
}
func calculateChecksum(inodes []fsBlock) int {
	checksum := 0
	for _, inode := range inodes {
		for compIdx := 0; compIdx < inode.size; compIdx++ {
			checksum += (inode.start + compIdx) * inode.inode
		}
	}
	return checksum
}
func e1(raw []byte) {
	filesys, freeSpaces, flist := preprocessInputForNonContiguous(raw)
	for fileCur := len(flist) - 1; fileCur >= 0; fileCur-- {
		file := flist[fileCur]
		for blk := range file.size {
			freeBlock := freeSpaces[0]
			if freeBlock > file.start+blk {
				break
			}
			//Push our block on to reclaim
			freeSpaces[0] = file.start + blk
			filesys[freeBlock] = file
			filesys[file.start+blk] = &fsBlock{inode: -1}
			slices.Sort(freeSpaces)
		}
	}
	debugPrintBlocks(filesys)
	calculatechecksum(filesys)
}
func preprocessInputforContiguous(raw []byte) ([][]int, []fsBlock) {
	freeSpaceLookup := make([][]int, 10)
	inodes := make([]fsBlock, 0)
	blockCursor := 0
	var nextInode int = 0
	for idx, blk := range raw {
		fileSize, err := strconv.Atoi(string(blk))
		if err != nil {
			panic("not an int")
		}
		if idx%2 == 0 {
			//fmt.Printf("Advancing cursor from %d to %d to accomodate for insertion of file of size: %d\n", blockCursor, blockCursor+fileSize, fileSize)
			block := fsBlock{
				inode: nextInode,
				size:  fileSize,
				start: blockCursor,
			}
			blockCursor += fileSize
			nextInode++
			inodes = append(inodes, block)
		} else {
			if fileSize == 0 {
				//fmt.Printf("Skipping a zero sized free space @ %d\n", blockCursor)
				continue
			}
			//fmt.Printf("Advancing cursor from %d to %d to accomodate free space of size: %d\n", blockCursor, blockCursor+fileSize, fileSize)
			//Pull the array of size from
			fsl := freeSpaceLookup[fileSize]
			if fsl == nil {
				fsl = []int{blockCursor}
			} else {
				fsl = append(fsl, blockCursor)
			}
			freeSpaceLookup[fileSize] = fsl
			//Move our cursor forward
			blockCursor += fileSize
		}
	}
	return freeSpaceLookup, inodes
}
func e2(raw []byte) {
	freeSpaceLookup, inodes := preprocessInputforContiguous(raw)
	for idx, inode := range slices.Backward(inodes) {
		//Attempt to locate an space in the Free Space Lookup with a size that will fit. Prefer the lower index over the most compact fit
		daWinnerFSLI := -1
		daWinnerFSL := 69
		for FSLCur := inode.size; FSLCur < len(freeSpaceLookup); FSLCur++ {
			if len(freeSpaceLookup[FSLCur]) == 0 {
				//If it's empty it doesn't qualify
				continue
			}
			if daWinnerFSLI == -1 {
				//If we have -1 in the FreeSpaceLookup Index, we don't have a best candidate so set it.
				daWinnerFSLI = freeSpaceLookup[FSLCur][0]
				daWinnerFSL = FSLCur
			} else {
				//fmt.Printf("Cmp %d < %d %t\n", freeSpaceLookup[FSLCur][0], daWinnerFSLI, freeSpaceLookup[FSLCur][0] < daWinnerFSLI)
				//Check to see if the index for free space is lower than our best candidate
				if freeSpaceLookup[FSLCur][0] < daWinnerFSLI {
					//fmt.Printf("Replacing FSLI and FSL\n")
					daWinnerFSLI = freeSpaceLookup[FSLCur][0]
					daWinnerFSL = FSLCur
				}
			}
		}
		if daWinnerFSLI == -1 {
			//fmt.Printf("It don't fit\n")
			continue
		}
		if daWinnerFSLI > inode.start {
			//fmt.Printf("It's not to the left of my current position\n")
			continue
		}
		//fmt.Printf("Best candidate for insertion %d on FSL Size %d\n", daWinnerFSLI, daWinnerFSL)
		//fmt.Printf("Pull off the array\n")
		freeSpaceLookup[daWinnerFSL] = freeSpaceLookup[daWinnerFSL][1:]
		//fmt.Printf("Insert our reclaimed size\n")
		freeSpaceLookup[inode.size] = append(freeSpaceLookup[inode.size], inode.start)
		//fmt.Printf("Inserting %d into freeSpaceLookup[%d] at end: %v\n", inode.start, inode.size, freeSpaceLookup[inode.size])
		//fmt.Printf("Check if we leave any space over\n")
		if daWinnerFSL > inode.size {
			//fmt.Printf("We will have %d remaining starting at %d, will place in FSL[%d]\n", daWinnerFSL-inode.size, daWinnerFSLI+inode.size, daWinnerFSL-inode.size)
			//fmt.Println(freeSpaceLookup[daWinnerFSL-inode.size])
			freeSpaceLookup[daWinnerFSL-inode.size] = append(freeSpaceLookup[daWinnerFSL-inode.size], daWinnerFSLI+inode.size)
			slices.Sort(freeSpaceLookup[daWinnerFSL-inode.size])
			//fmt.Printf("Reordering freespace: %v\n", freeSpaceLookup[daWinnerFSL-inode.size])
		}
		slices.Sort(freeSpaceLookup[inode.size])
		//fmt.Printf("Reordering freespace: %v\n", freeSpaceLookup[inode.size])
		//fmt.Printf("Update inode start to %d from %d\n", daWinnerFSLI, inode.start)
		inode.start = daWinnerFSLI
		inodes[idx] = inode
	}
	//fmt.Println("Inodes moved, resort array using custom function that sorts by start pos")
	//fmt.Printf("%v\n", inodes)
	slices.SortFunc(inodes, func(a fsBlock, b fsBlock) int {
		if a.start < b.start {
			return -1
		} else if a.start > b.start {
			return 1
		} else {
			return 0
		}
	})
	//fmt.Printf("%v\n", inodes)
	checksum := calculateChecksum(inodes)
	fmt.Printf("check sum %d\n", checksum)
}
func main() {
	raw, err := os.ReadFile("input.txt")
	if err != nil {
		panic("Failed to open file ./input.txt")
	}
	//e1(raw)
	e2(raw)
}
