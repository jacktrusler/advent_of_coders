package main

import (
	"os"
	"strconv"
	"strings"
)

func main() {
	var power_sum int = 0
	input, err := os.ReadFile("input.txt")
	if err != nil {
		panic(err)
	}
	games := strings.Split(string(input), "\n")
	for _, gamestr := range games {
		gamestrSplit := strings.Split(gamestr, ":")
		gamePlayStr := gamestrSplit[1]
		draws := strings.Split(gamePlayStr, ";")
		if err != nil {
			panic(err)
		}
		var min_red, min_green, min_blue int = 0, 0, 0
		for _, draw := range draws {
			cubes := strings.Split(draw, ",")
			for _, cube := range cubes {
				cube := strings.TrimSpace(cube)
				cubeSplit := strings.Split(cube, " ")
				cubeColor := cubeSplit[1]
				cubeQuant, err := strconv.Atoi(cubeSplit[0])
				if err != nil {
					panic("Holy shit pissssssssssss")
				}
				var cmp *int
				switch cubeColor {
				case "red":
					cmp = &min_red
				case "green":
					cmp = &min_green
				case "blue":
					cmp = &min_blue
				default:
					panic("It is so hot in here")
				}
				if cubeQuant > *cmp {
					*cmp = cubeQuant
				}
			}
		}
		power_sum += min_red * min_green * min_blue
	}
	println(power_sum)
}
