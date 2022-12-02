import { readFileSync } from "fs";

//A: Rock | B: Paper | C: Scizzors -- opponent
//X: Rock | Y: Paper | Z: Scizzors -- you
type ComboKey = keyof typeof combosP1;

// function isComboKey(arg: string): arg is ComboKey {
//   return Object.keys(combosP1).includes(arg)
// }

const combosP1 = {
  "A X": 4,
  "A Y": 8,
  "A Z": 3,
  "B X": 1,
  "B Y": 5,
  "B Z": 9,
  "C X": 7,
  "C Y": 2,
  "C Z": 6,
} as const;

const combosP2 = {
  "A X": 3,
  "A Y": 4,
  "A Z": 8,
  "B X": 1,
  "B Y": 5,
  "B Z": 9,
  "C X": 2,
  "C Y": 6,
  "C Z": 7,
} as const;

function day2(filePath: string) {
  const strData: string[] = readFileSync(filePath).toString().split('\n').splice(0, 2500)

  const answerP1 = strData.reduce((acc, str) => acc + combosP1[str as ComboKey], 0)
  const answerP2 = strData.reduce((acc, str) => acc + combosP2[str as ComboKey], 0)

  const answer = {
    part1: answerP1,
    part2: answerP2,
  }
  console.log(answer)
  return answer
}

export { day2 }
