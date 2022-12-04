import { readFileSync } from "fs";

function day3(filePath: string) {
  const allRucksacks = readFileSync(filePath).toString().replace(/\n$/, "").split('\n')
  const answer = {
    part1: 0,
    part2: 0,
  }
  //decimal char codes 97-122 = a - z
  //decimal char codes 65-90 = A - Z

  //Part 1
  let letterArr = []
  for (const r of allRucksacks) {
    let cLen = r.length / 2
    let c1 = r.slice(0, cLen)
    let c2 = r.slice(cLen, r.length)
    for (let i = 0; i < r.length / 2; i++) {
      if (c2.includes(c1[i])) {
        letterArr.push(c1[i])
        break;
      }
    }
  }
  const answerP1 = letterArr.reduce((acc, l) => {
    let lCode = l.charCodeAt(0);
    if (lCode > 90) {
      return acc + lCode - 96
    } else {
      return acc + lCode - 38
    }
  }, 0)

  answer.part1 = answerP1;

  //part 2
  let allR = allRucksacks.length
  let threeSacks: any = [];
  for (let i = 0; i < allR; i = i + 3) {
    const group = [];
    group.push(allRucksacks[i])
    group.push(allRucksacks[i + 1])
    group.push(allRucksacks[i + 2])
    threeSacks.push(group)
  }

  const letArr: string[] = threeSacks
    .map((group: any) => {
      for (const l of group[0]) {
        if (group[1].includes(l)) {
          if (group[2].includes(l)) {
            return l
          }
        }
      }
    })

  const answerP2 = letArr.reduce((acc, l) => {
    let lCode = l.charCodeAt(0);
    if (lCode > 90) {
      return acc + lCode - 96
    } else {
      return acc + lCode - 38
    }
  }, 0)

  answer.part2 = answerP2
  console.log(answer)
  return answer
}

export { day3 }
