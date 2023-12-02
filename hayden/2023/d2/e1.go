package main

import (
	"os"
	"strconv"
	"strings"
)

func main() {
	var possible_plays int = 0
	var mx_red, mx_green, mx_blue int = 12, 13, 14
	input, err := os.ReadFile("input.txt")
	if err != nil {
		panic(err)
	}
	games := strings.Split(string(input), "\n")
	for _, gamestr := range games {
		gamestrSplit := strings.Split(gamestr, ":")
		gameIDStr := gamestrSplit[0]
		gamePlayStr := gamestrSplit[1]
		draws := strings.Split(gamePlayStr, ";")
		gameID, err := strconv.Atoi(gameIDStr[5:])
		possible_game := true
		if err != nil {
			panic(err)
		}
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
				var cmp int
				switch cubeColor {
				case "red":
					cmp = mx_red
				case "green":
					cmp = mx_green
				case "blue":
					cmp = mx_blue
				default:
					panic("It is so hot in here")
				}
				if cubeQuant > cmp {
					possible_game = false
				}
			}
		}
		if possible_game {
			possible_plays += gameID
		}
	}
	println(possible_plays)
}
