package main

import (
	"os"
	"strconv"
)

type Game struct {
	draws  [50]int
	wins   map[int]bool
	number int
	copies int
}

func makeGame(draws [50]int, wins map[int]bool, number int) *Game {
	return &Game{draws: draws, wins: wins, number: number, copies: 1}
}

func main() {
	inputData, err := os.ReadFile("input.txt")
	if err != nil {
		panic("Where's the file, Lebowski!?")
	}
	cards := buildCards(inputData)
	cardCount := 0
	for i := 1; i <= len(cards); i++ {
		card := cards[i]
		dupeRun := getSpread(card)
		//Play Copies
		cardCount += card.copies
		for s := 1; s <= dupeRun; s++ {
			spreadDraw := cards[i+s]
			spreadDraw.copies = spreadDraw.copies + card.copies
		}
	}
	println(cardCount)
}

func buildCards(input []byte) map[int]*Game {
	cards := make(map[int]*Game)
	winningNumbers := make(map[int]bool)
	var drawnNumbers [50]int = [50]int{}
	workingNumber := 0
	drawInd := 0
	cardNumber := 0
	inDraws, inWinning := false, false
	for _, char := range input {
		switch char {
		case '\n':
			drawnNumbers[drawInd] = workingNumber
			cards[cardNumber] = makeGame(drawnNumbers, winningNumbers, cardNumber)
			winningNumbers = make(map[int]bool)
			drawnNumbers = [50]int{}
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
	cards[cardNumber] = makeGame(drawnNumbers, winningNumbers, cardNumber)
	return cards
}

func getSpread(card *Game) int {
	gamePts := 0
	for _, draw := range card.draws {
		if card.wins[draw] {
			gamePts++
		}
	}
	return gamePts
}
