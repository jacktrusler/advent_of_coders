def main():
    ROCK = 1
    PAPER = 2
    SCISSORS = 3
    with open(file="rockpaperinputs.txt", mode="r") as fGameInputs:
        RockPaperGamesList = fGameInputs.read().splitlines()
        PlayerTotalScore = 0
        for RockPaperMatch in RockPaperGamesList:
            [NonPlayerMove,PlayerMove] = RockPaperMatch.split()
            PlayerMove = ord(PlayerMove) - 87
            NonPlayerMove = ord(NonPlayerMove) - 64
            PlayerTotalScore += PlayerMove
            if PlayerMove == NonPlayerMove:
                PlayerTotalScore += 3
            elif NonPlayerMove == ROCK and PlayerMove == PAPER:
                PlayerTotalScore += 6
            elif NonPlayerMove == PAPER and PlayerMove == SCISSORS:
                PlayerTotalScore += 6
            elif NonPlayerMove == SCISSORS and PlayerMove == ROCK:
                PlayerTotalScore += 6
        print(PlayerTotalScore)
        fGameInputs.close()

if __name__ == "__main__":
    main()