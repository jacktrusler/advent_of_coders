package main

import (
	"os"
	"strconv"
)

type Game struct {
	draws  [32]int
	wins   map[int]bool
	number int
}

func main() {
	inputData, err := os.ReadFile("input.txt")
	if err != nil {
		panic("Where's the file, Lebowski!?")
	}
	cards := buildCards(inputData)
	totalPts := 0
	for _, card := range cards {
		gamePts := 0
		for _, draw := range card.draws {
			if card.wins[draw] {
				if gamePts == 0 {
					gamePts = 1
				} else {
					gamePts *= 2
				}
			}
		}
		totalPts += gamePts
	}
	println(totalPts)
}

func buildCards(input []byte) map[int]Game {
	cards := make(map[int]Game)
	winningNumbers := make(map[int]bool)
	var drawnNumbers [32]int = [32]int{}
	workingNumber := 0
	drawInd := 0
	cardNumber := 0
	inDraws, inWinning := false, false
	for _, char := range input {
		switch char {
		case '\n':
			drawnNumbers[drawInd] = workingNumber
			cards[cardNumber] = Game{draws: drawnNumbers, wins: winningNumbers, number: cardNumber}
			winningNumbers = make(map[int]bool)
			drawnNumbers = [32]int{}
			workingNumber = 0
			drawInd = 0
			cardNumber = 0
			inDraws, inWinning = false, false
		case '|':
			inWinning = false
			inDraws = true
		case ':':
			inWinning = true
			cardNumber = workingNumber
			workingNumber = 0
		case ' ':
			if workingNumber == 0 {
				continue
			}
			if inDraws {
				drawnNumbers[drawInd] = workingNumber
				workingNumber = 0
				drawInd++
			} else if inWinning {
				winningNumbers[workingNumber] = true
				workingNumber = 0
			} else {
				cardNumber = workingNumber
				workingNumber = 0
			}
		default:
			digit, err := strconv.Atoi(string(char))
			if err != nil {
				continue
			}
			if workingNumber == 0 {
				workingNumber = digit
			} else {
				workingNumber = workingNumber*10 + digit
			}
		}
	}
	drawnNumbers[drawInd] = workingNumber
	cards[cardNumber] = Game{draws: drawnNumbers, wins: winningNumbers, number: cardNumber}
	winningNumbers = make(map[int]bool)
	return cards
}
