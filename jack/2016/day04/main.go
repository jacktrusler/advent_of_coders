package main

import (
	"aoc2016/util"
	"bufio"
	"fmt"
	"os"
	"regexp"
	"sort"
	"strconv"
	"strings"
)

func getInfo(lastEl string) (string, string) {
	//eqivalent to ^([0-9]+)\[([a-z]+)\]$
	// () are capture groups
	// ^$ start-end of line
	re := regexp.MustCompile(`^(\d+)\[(\w+)\]$`)

	matches := re.FindStringSubmatch(lastEl)
	var sectorID, commonLetters string

	if len(matches) == 3 {
		// 123
		sectorID = matches[1]
		//abxyz
		commonLetters = matches[2]
	}

	return sectorID, commonLetters

}

func part1(input string) {
	rooms := strings.Split(input, "\n")

	validRooms := make([]int, 0)

	// golang label for selecting loop to jump to
roomLoop:
	for _, room := range rooms {
		r := strings.Split(room, "-")

		// last element of the room is sectorID[commonLetters]
		lastEl := r[len(r)-1]

		sectorID, commonLetters := getInfo(lastEl)

		//remove sectorID[commonLetters]
		r = r[:len(r)-1]
		letters := strings.Join(r, "")
		asciiMap := make(map[rune]int)
		for _, char := range letters {
			asciiMap[char]++
		}

		// convert map to slice
		type pair struct {
			letter rune
			count  int
		}

		pairs := make([]pair, 0)
		for key, value := range asciiMap {
			pairs = append(pairs, pair{letter: key, count: value})
		}

		sort.Slice(pairs, func(i, j int) bool {
			return pairs[i].count > pairs[j].count
		})

		// inner bubble sort for ties alphabetically
		for i := 0; i < len(pairs)-1; i++ {
			for j := i; j < len(pairs)-1; j++ {
				if pairs[i].count == pairs[j+1].count {
					if pairs[i].letter > pairs[j+1].letter {
						//swap
						tmp := pairs[i]
						pairs[i] = pairs[j+1]
						pairs[j+1] = tmp
					}
				}
			}
		}

		top5 := pairs[:5]

		for _, pair := range top5 {
			if !strings.ContainsRune(commonLetters, pair.letter) {
				continue roomLoop
			}
		}
		id, err := strconv.Atoi(sectorID)
		if err != nil {
			panic("SectorID is not valid string to convert to int")
		}
		validRooms = append(validRooms, id)
	}

	total := 0
	for _, id := range validRooms {
		total += id
	}
	fmt.Println(total)
}

func part2(input string) {
	type cypher struct {
		id     string
		output string
	}

	rooms := strings.Split(input, "\n")
	cypherArr := make([]cypher, 0)
	for _, room := range rooms {
		r := strings.Split(room, "-")

		// last element of the room is sectorID[commonLetters]
		lastEl := r[len(r)-1]

		sectorID, _ := getInfo(lastEl)

		//remove sectorID[commonLetters]
		r = r[:len(r)-1]
		letters := strings.Join(r, "")

		runeArr := make([]rune, 0)
		id, err := strconv.Atoi(sectorID)
		if err != nil {
			panic("SectorID is not valid string to convert to int")
		}
		shift := id % 26
		for _, rn := range letters {
			var newRune int
			if int(rn)+shift > 'z' {
				newRune = int(rn) + shift - 26
			} else {
				newRune = int(rn) + shift
			}
			runeArr = append(runeArr, rune(newRune))
		}
		cypherArr = append(cypherArr, cypher{id: sectorID, output: string(runeArr)})
	}

	// output to file for fun
	filename := "cyphers.txt"
	file, err := os.Create("cyphers.txt")
	if err != nil {
		fmt.Println("Error creating file:", err)
		return
	}
	defer file.Close()

	writer := bufio.NewWriter(file)

	target := "northpoleobjectstorage"
	for _, cypher := range cypherArr {
		//part2 answer: locate target
		if cypher.output == target {
			fmt.Println(cypher.id)
		}

		//write each cypher to file, line by line
		_, err := writer.WriteString(cypher.output + "\n")
		if err != nil {
			fmt.Println("Error writing to file:", err)
			return
		}
		err = writer.Flush()
		if err != nil {
			fmt.Println("Error flushing to file:", err)
			return
		}
	}

	fmt.Printf("All cyphers written to file %s successfully!", filename)
}

func main() {
	input := util.FileAsString("./input.txt")
	fmt.Println("----- Part 1 -----")
	part1(input)
	fmt.Println("----- Part 2 -----")
	part2(input)
}
