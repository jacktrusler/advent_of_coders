import { readFileSync } from "fs";

function day1(filePath: string) {
  const data = readFileSync(filePath)
  const dataArr = data.toString().split("\n")

  let sum = 0;
  let elfsCalories = [];
  for (const numStr of dataArr) {
    if (numStr) {
      sum += parseInt(numStr)
    } else {
      elfsCalories.push(sum)
      sum = 0;
    }
  }

  const sortedCalories = elfsCalories.sort((a, b) => b - a)
  const max = sortedCalories[0]
  const top3 = sortedCalories[0] + sortedCalories[1] + sortedCalories[2]

  const answer = {
    part1: max,
    part2: top3,
  }
  console.log(answer)
  return answer;
}

export { day1 };
