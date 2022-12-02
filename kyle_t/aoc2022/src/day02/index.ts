import run from "aocrunner";

const allTheMoves = (allTheInput: string) => {
  return allTheInput.split("\n");
};

const ROCK_POINTS = 1;
const PAPER_POINTS = 2;
const SCISSORS_POINTS = 3;

const BIG_WIN_POINTS = 6;
const TIE_POINTS = 3;
const SAD_LOSS_POINTS = 0;

const THEIR_ROCK = "A";
const MY_ROCK = "X";
const THEIR_PAPER = "B";
const MY_PAPER = "Y";
const THEIR_SCISSORS = "C";
const MY_SCISSORS = "Z";

const STRATEGY_ONE = {
  [`${THEIR_ROCK} ${MY_ROCK}`]: ROCK_POINTS + TIE_POINTS,
  [`${THEIR_ROCK} ${MY_PAPER}`]: PAPER_POINTS + BIG_WIN_POINTS,
  [`${THEIR_ROCK} ${MY_SCISSORS}`]: SCISSORS_POINTS + SAD_LOSS_POINTS,
  [`${THEIR_PAPER} ${MY_ROCK}`]: ROCK_POINTS + SAD_LOSS_POINTS,
  [`${THEIR_PAPER} ${MY_PAPER}`]: PAPER_POINTS + TIE_POINTS,
  [`${THEIR_PAPER} ${MY_SCISSORS}`]: SCISSORS_POINTS + BIG_WIN_POINTS,
  [`${THEIR_SCISSORS} ${MY_ROCK}`]: ROCK_POINTS + BIG_WIN_POINTS,
  [`${THEIR_SCISSORS} ${MY_PAPER}`]: PAPER_POINTS + SAD_LOSS_POINTS,
  [`${THEIR_SCISSORS} ${MY_SCISSORS}`]: SCISSORS_POINTS + TIE_POINTS,
};

const part1 = (allTheInput: string) => {
  return allTheMoves(allTheInput).reduce((myGreatScore, move) => {
    return (myGreatScore += STRATEGY_ONE[move]);
  }, 0);
};

const LOSE = "X";
const TIE = "Y";
const WIN = "Z";
const STRATEGY_TWO = {
  [`${THEIR_ROCK} ${LOSE}`]: SCISSORS_POINTS + SAD_LOSS_POINTS,
  [`${THEIR_ROCK} ${TIE}`]: ROCK_POINTS + TIE_POINTS,
  [`${THEIR_ROCK} ${WIN}`]: PAPER_POINTS + BIG_WIN_POINTS,
  [`${THEIR_PAPER} ${LOSE}`]: ROCK_POINTS + SAD_LOSS_POINTS,
  [`${THEIR_PAPER} ${TIE}`]: PAPER_POINTS + TIE_POINTS,
  [`${THEIR_PAPER} ${WIN}`]: SCISSORS_POINTS + BIG_WIN_POINTS,
  [`${THEIR_SCISSORS} ${LOSE}`]: PAPER_POINTS + SAD_LOSS_POINTS,
  [`${THEIR_SCISSORS} ${TIE}`]: SCISSORS_POINTS + TIE_POINTS,
  [`${THEIR_SCISSORS} ${WIN}`]: ROCK_POINTS + BIG_WIN_POINTS,
};

const part2 = (allTheInput: string) => {
  return allTheMoves(allTheInput).reduce((myGreatScore, move) => {
    return (myGreatScore += STRATEGY_TWO[move]);
  }, 0);
};

run({
  part1: {
    tests: [
      {
        input: `A Y
B X
C Z`,
        expected: 15,
      },
    ],
    solution: part1,
  },
  part2: {
    tests: [
      // {
      //   input: ``,
      //   expected: "",
      // },
    ],
    solution: part2,
  },
  trimTestInputs: true,
  onlyTests: false,
});
