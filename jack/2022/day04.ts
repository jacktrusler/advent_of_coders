import { readFileSync } from "fs";

function ranger(start: number, end: number): Set<number> {
  const newSet: Set<number> = new Set();
  for (let i = start; i <= end; i++) {
    newSet.add(i);
  }
  return newSet;
}

function day4(filePath: string) {
  //split on , - and \n
  let regexSplit = /[,\n-]/
  const dataSplit: string[] = readFileSync(filePath).toString().replace(/\n$/, "").split(regexSplit)

  const allNum: number[] = dataSplit.map((num) => parseInt(num))
  const len = allNum.length
  let part1 = 0;
  //5-7 7-9
  for (let i = 0; i < len; i = i + 4) {
    let [lStart, lEnd, rStart, rEnd] = [allNum[i], allNum[i + 1], allNum[i + 2], allNum[i + 3]]
    if (lStart >= rStart && lEnd <= rEnd) {
      part1++
      continue;
    }
    if (lStart <= rStart && lEnd >= rEnd) {
      part1++
      continue;
    }
  }

  let part2 = 0;
  for (let i = 0; i < len; i = i + 4) {
    let [lStart, lEnd, rStart, rEnd] = [allNum[i], allNum[i + 1], allNum[i + 2], allNum[i + 3]]
    let unifiedSet = ranger(lStart, lEnd)
    for (let j = rStart; j <= rEnd; j++) {
      if (unifiedSet.has(j)) {
        part2++
        break;
      }
    }
  }
  console.log({ part1: part1, part2: part2 })
  return {
    part1: part1,
    part2: part2,
  }
}

export { day4 }
