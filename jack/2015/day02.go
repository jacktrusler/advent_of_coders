package main

import (
	"aoc2015/pkg/utils"
	"strings"
)

type Dimms struct {
	l int
	w int
	h int
}

func Day2() {
	fileAsString := utils.FileAsString("./data/day2.txt")
	presents := strings.Split(fileAsString, "\n")

	for _, v := range presents {
		pDimms := strings.Split(v, "x")
		pDimmsInt := utils.StrArr2IntArr(pDimms)
		pLen := len(pDimmsInt)
		for i := 0; i < pLen; i++ {
			for j := 0; j < pLen-i; j++ {
				if pDimmsInt[j] > pDimmsInt[j+1] {
					temp := pDimmsInt[j]
					pDimmsInt[j] = pDimmsInt[j+1]
					pDimmsInt[j+1] = temp
				}
			}
		}

	}

	// take slice of Dimms and figure out

}
