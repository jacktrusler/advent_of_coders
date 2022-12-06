def main():
    ROCK = 1
    PAPER = 2
    SCISSORS = 3
    LOSS = "X"
    DRAW = "Y"
    WIN = "Z"
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
        print("total score", PlayerTotalScore)
        PlayerTotalScore = 0
        for RockPaperMatch in RockPaperGamesList:
            [NonPlayerMove, MatchResult] = RockPaperMatch.split()
            NonPlayerMove = ord(NonPlayerMove) - 64
            if MatchResult == LOSS:
                if NonPlayerMove == ROCK:
                    PlayerTotalScore += SCISSORS
                elif NonPlayerMove == PAPER:
                    PlayerTotalScore += ROCK
                elif NonPlayerMove == SCISSORS:
                    PlayerTotalScore += PAPER
            elif MatchResult == WIN:
                PlayerTotalScore += 6
                if NonPlayerMove == ROCK:
                    PlayerTotalScore += PAPER
                elif NonPlayerMove == PAPER:
                    PlayerTotalScore += SCISSORS
                elif NonPlayerMove == SCISSORS:
                    PlayerTotalScore += ROCK
            else:
                PlayerTotalScore += 3 + NonPlayerMove
        print("adjusted score", PlayerTotalScore)
        fGameInputs.close()

if __name__ == "__main__":
    main()