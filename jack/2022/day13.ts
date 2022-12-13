import { readFileSync } from "fs";

const answer = { part1: 0, part2: 0, }

function flattenArr(arr: any): number[] {
  if (Array.isArray(arr)) {
    let newArr = arr.flat()
    if (typeof newArr[0] !== 'number' && typeof newArr[0] === undefined) {
      flattenArr(newArr)
    }
  }
  return arr;
}

function day13(filePath: string) {
  const input = readFileSync(filePath).toString().replace(/\n$/, "").split('\n\n')
  const inputPairs: string[] = input.map((input) => input.split('\n')).flat()
  const pairs: any[] = inputPairs.map((str) => JSON.parse(str))

  let totalIndexes = 0;
  function tester(lhs: any[], rhs: any[]) {
    if (rhs.length < lhs.length) return false;

    let lhItem;
    let rhItem;
    for (let j = 0; j < lhs.length; j++) {
      // if lhs undefined skip
      if (lhs[j] === undefined) continue;
      if (Array.isArray(lhs[j]) && rhs[j] === undefined) {
        return false
      } else if (Array.isArray(lhs[j]) && rhs[j]) {
        lhItem = flattenArr(lhs[j])
      } else {
        lhItem = [lhs[j]];
      }
      if (Array.isArray(rhs[j])) {
        rhItem = flattenArr(rhs[j])
      } else {
        rhItem = [rhs[j]];
      }
      for (let k = 0; k < lhItem.length; k++) {
        if (lhItem[k] === undefined || rhItem[k] === undefined) break;
        if (lhItem[k] > rhItem[k]) return false;
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
