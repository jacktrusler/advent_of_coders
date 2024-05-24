package main

import (
	"aoc2015/pkg/utils"
	"fmt"
	"strings"
)

func Day2() {
	fileAsString := utils.FileAsString("./data/day2.txt")
	presents := strings.Split(fileAsString, "\n")

	totalPaper := 0
	totalRibbon := 0
	for _, v := range presents {
		pDimms := strings.Split(v, "x")
		pDimmsInt := utils.StrArr2IntArr(pDimms)
		pLen := len(pDimmsInt) - 1
		// bubble sort array for smallest side
		for i := 0; i < pLen; i++ {
			for j := 0; j < pLen-i; j++ {
				if pDimmsInt[j] > pDimmsInt[j+1] {
					temp := pDimmsInt[j]
					pDimmsInt[j] = pDimmsInt[j+1]
					pDimmsInt[j+1] = temp
				}
			}
		}
		// 6 sides: 2 * l * w | 2 * w * h | 2 * h * l
		lw := pDimmsInt[0] * pDimmsInt[1]
		wh := pDimmsInt[1] * pDimmsInt[2]
		hl := pDimmsInt[0] * pDimmsInt[2]
		surfaceArea := (2 * lw) + (2 * wh) + (2 * hl)
		// extraPaper is the area of the smallest side, sorted array means [0][1] smallest side
		extraPaper := lw
		totalPaper += surfaceArea + extraPaper
		// totalRibbon is the smallest perimeter + volume of present
		totalRibbon += (2 * pDimmsInt[0]) + (2 * pDimmsInt[1]) + (pDimmsInt[0] * pDimmsInt[1] * pDimmsInt[2])
	}
	fmt.Printf("Total wrapping paper: %d\nTotal ribbon: %d\n", totalPaper, totalRibbon)
}
