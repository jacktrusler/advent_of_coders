package main

import (
	"os"
	"strconv"
)

func getCartKey(x uint32, y uint32) uint {
	var coordinate uint = uint(x)
	coordinate = coordinate<<32 + uint(y)
	return coordinate
}

func getCoordinates(coordinate uint) (x uint32, y uint32) {
	x = uint32(coordinate >> 32)
	y = uint32(coordinate)
	return x, y
}

func main() {
	rawInput, err := os.ReadFile("input.txt")
	if err != nil {
		panic("MICHAEL")
	}

	var Parts = make(map[uint]*int)
	var Gears = make(map[uint]bool)
	GearRatioSum := 0
	var x, y, xmx, ymx uint32 = 0, 0, 0, 0
	var newPN *int = nil

	for _, byt := range rawInput {
		//Is that A Number!?
		PartDigit, err := strconv.Atoi(string(byt))
		if err == nil {
			if newPN == nil {
				var pn int = 0
				newPN = &pn
			}
			*newPN = *newPN*10 + PartDigit
			coordinate := getCartKey(x, y)
			Parts[coordinate] = newPN
		} else {
			//Flush Part Number
			if newPN != nil {
				newPN = nil
			}
			//Bounce on a NL
			if byt == 10 {
				if y == 0 {
					xmx = x
				}
				x = 0
				y++
				continue
			} else if byt == '*' {
				coordinate := getCartKey(x, y)
				Gears[coordinate] = true
			}
		}
		x++
	}
	ymx = y
	for key, _ := range Gears {
		gx, gy := getCoordinates(key)
		var adjacencies = make(map[int]bool)
		//fmt.Printf("Checking for adjacent PNs to Gear @ (%d, %d)\n", gx, gy)
		//Determine Start X
		atTop := gy == 0
		atBot := gy == ymx
		atLeft := gx == 0
		atRight := gx+1 > xmx
		pcStartX := gx - 1
		pcStopX := gx + 1
		if atRight {
			pcStopX = xmx
		}
		if atLeft {
			pcStartX = 0
		}
		for x := pcStartX; x <= pcStopX; x++ {
			if (x < gx) || (!atRight && x == pcStopX) {
				//fmt.Printf("Checking (%d, %d) => ", x, gy)
				pn := Parts[getCartKey(x, gy)]
				if pn != nil {
					adjacencies[*pn] = true
					//fmt.Printf("%d -> %d", pn, *pn)
				}
			}
			if !atTop {
				//fmt.Printf("Checking (%d, %d) => ", x, gy-1)
				pn := Parts[getCartKey(x, gy-1)]
				if pn != nil {
					adjacencies[*pn] = true
					//fmt.Printf("%d -> %d", pn, *pn)
				}
			}
			if !atBot {
				//fmt.Printf("Checking (%d, %d) => ", x, gy+1)
				pn := Parts[getCartKey(x, gy+1)]
				if pn != nil {
					adjacencies[*pn] = true
					//fmt.Printf("%d -> %d", pn, *pn)
				}
			}
		}
		if len(adjacencies) == 2 {
			gr := 1
			for grc, _ := range adjacencies {
				gr *= grc
			}
			GearRatioSum += gr
		}
	}
	println(GearRatioSum)
}
