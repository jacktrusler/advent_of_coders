import { readFileSync } from "fs";

const answer = { part1: 0, part2: 0, }

// function flattenArr(arr: any): number[] {
//   if (Array.isArray(arr)) {
//     let newArr = arr.flat()
//     if (typeof newArr[0] !== 'number' && typeof newArr[0] === undefined) {
//       flattenArr(newArr)
//     }
//   }
//   return arr;
// }

function arrayMaker(left, right): { left: any[], right: any[] } {
  if (Array.isArray(left) && Array.isArray(right)) {
    return { left, right }
  }
  if (typeof left === 'number' && Array.isArray(right)) {
    arrayMaker([left], right)
  }
  if (typeof right === 'number' && Array.isArray(left)) {
    arrayMaker(left, [right])
  }
}

function day13(filePath: string) {
  const input = readFileSync(filePath).toString().replace(/\n$/, "").split('\n\n')
  const inputPairs: string[] = input.map((input) => input.split('\n')).flat()
  const pairs: any[] = inputPairs.map((str) => JSON.parse(str))

  function tester(lhs: any[], rhs: any[]) {
    //lhs must be shorter
    if (rhs.length < lhs.length) return false;

    for (let j = 0; j < lhs.length; j++) {
      if (Array.isArray(lhs)) {
        if (typeof lhs[j] === 'number' && typeof rhs[j] === 'number') {
          if (lhs[j] > rhs[j]) return false;
          continue;
        }
        const { left, right } = arrayMaker(lhs[j], rhs[j])
        for (let k = 0; k < Math.max(left.length, right.length); k++) {
          if (typeof left[k] === 'number' && typeof right[k] === 'number') {
            if (lhs[j] > rhs[j]) return false;
          }
        }
      }
    }
    return true;
  }


  for (let i = 0; i < pairs.length; i = i + 2) {
    let lhs = pairs[i];
    let rhs = pairs[i + 1];
    console.log(tester(lhs, rhs));
  }
}

day13('./day13small.txt')
