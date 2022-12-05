import { readFileSync } from "fs";

/** 
            [G] [W]         [Q]    
[Z]         [Q] [M]     [J] [F]    
[V]         [V] [S] [F] [N] [R]    
[T]         [F] [C] [H] [F] [W] [P]
[B] [L]     [L] [J] [C] [V] [D] [V]
[J] [V] [F] [N] [T] [T] [C] [Z] [W]
[G] [R] [Q] [H] [Q] [W] [Z] [G] [B]
[R] [J] [S] [Z] [R] [S] [D] [L] [J]
 1   2   3   4   5   6   7   8   9
 */

//top ---> bottom
const shipContainers = () => [
  ['Z', 'V', 'T', 'B', 'J', 'G', 'R'],
  ['L', 'V', 'R', 'J'],
  ['F', 'Q', 'S'],
  ['G', 'Q', 'V', 'F', 'L', 'N', 'H', 'Z'],
  ['W', 'M', 'S', 'C', 'J', 'T', 'Q', 'R'],
  ['F', 'H', 'C', 'T', 'W', 'S'],
  ['J', 'N', 'F', 'V', 'C', 'Z', 'D'],
  ['Q', 'F', 'R', 'W', 'D', 'Z', 'G', 'L'],
  ['P', 'V', 'W', 'B', 'J'],
]

function day5(filePath: string) {
  const answer: { [key: string]: any } = {}
  const strData: string[] = readFileSync(filePath)
    .toString()
    .trim()
    .replace(/\n$/, "")
    .split('\n')

  //split on letters and whitespace -- filter for non ''
  const reggy = /[a-z ]+/
  const instructions: number[][] = strData
    .map((instruction) => instruction.split(reggy)
      .filter((str) => str)
      .map((numStr) => Number(numStr))
    )
  //Make a deep copy of nested arrays
  const shipCopy: string[][] = shipContainers()
  //instructions = [[6,5,7], [4,9,3]] -> move x from [i] to [j]
  //part 1
  instructions.map((inst) => {
    for (let i = 0; i < inst[0]; i++) {
      let container = shipCopy[inst[1] - 1].shift()
      shipCopy[inst[2] - 1].unshift(container as string)
    }
  })

  //part 2
  const shipCopy2: string[][] = shipContainers()
  instructions.map((inst) => {
    let container = shipCopy2[inst[1] - 1].splice(0, inst[0])
    shipCopy2[inst[2] - 1] = [...container, ...shipCopy2[inst[2] - 1]]
  })

  answer.part1 = shipCopy.map((container) => container[0]).join()
  answer.part2 = shipCopy2.map((container) => container[0]).join()
  console.log(answer)
  return answer
}

export { day5 }
