package main

import (
	"fmt"
	"os"
	"strconv"
)

type Point2D struct {
	x int
	y int
}

type PartNo struct {
	origin *Point2D
	length int
	number int
}

func newP2D(x int, y int) *Point2D {
	pt := Point2D{x: x, y: y}
	return &pt
}

func main() {
	rawInput, err := os.ReadFile("input.txt")
	if err != nil {
		panic("MICHAEL")
	}

	var PotentialParts []PartNo
	var Symbols = make(map[string]bool)
	var partSum int = 0
	var x, y, xmx int = 0, 0, 0
	var newPN int = 0
	var newOrigin *Point2D = nil
	var newLength int = 0
	for _, byt := range rawInput {
		//Is that A Number!?
		PartDigit, err := strconv.Atoi(string(byt))
		if err == nil {
			if newOrigin == nil {
				newOrigin = newP2D(x, y)
			}
			newPN = newPN*10 + PartDigit
			newLength++
		} else {
			//Flush Part Number
			if newOrigin != nil {
				PotentialParts = append(PotentialParts, PartNo{origin: newOrigin, length: newLength, number: newPN})
				newLength = 0
				newOrigin = nil
				newPN = 0
			}
			//Bounce on a NL
			if byt == 10 {
				if y == 0 {
					xmx = x
				}
				x = 0
				y++
				continue
			} else if byt != '.' {
				Symbols[fmt.Sprintf("%d,%d", x, y)] = true
			}
		}
		x++
	}
	for _, pc := range PotentialParts {
		//Check Tops
		atTop := pc.origin.y == 0
		atBot := pc.origin.y == y
		atLeft := pc.origin.x == 0
		atRight := pc.origin.x+pc.length > xmx
		located := false
		pcStartX := pc.origin.x - 1
		pcStopX := pc.origin.x + pc.length
		if atRight {
			pcStopX = xmx
		}
		if atLeft {
			pcStartX = 0
		}
		//fmt.Printf("Starting search for adjacent part %d @ (%d,%d) len %d\n", pc.number, pc.origin.x, pc.origin.y, pc.length)
		for x := pcStartX; x <= pcStopX && !located; x++ {
			if (x < pc.origin.x) || (!atRight && x == pcStopX) {
				//fmt.Printf("Checking (%d,%d): ", x, pc.origin.y)
				if Symbols[fmt.Sprintf("%d,%d", x, pc.origin.y)] {
					located = true
					//fmt.Printf("located\n")
					continue
				}
				//fmt.Printf("not located\n")
			}
			if !atTop {
				//fmt.Printf("Checking (%d,%d): ", x, pc.origin.y-1)
				if Symbols[fmt.Sprintf("%d,%d", x, pc.origin.y-1)] {
					located = true
					//fmt.Printf("located\n")
					continue
				}
				//fmt.Printf("not located\n")
			}
			if !atBot {
				//fmt.Printf("Checking (%d,%d): ", x, pc.origin.y+1)
				if Symbols[fmt.Sprintf("%d,%d", x, pc.origin.y+1)] {
					located = true
					//fmt.Printf("located\n")
					continue
				}
				//fmt.Printf("not located\n")
			}
		}
		if located {
			partSum += pc.number
		}
	}
	println(partSum)
}
