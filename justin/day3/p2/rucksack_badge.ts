import * as fs from "fs";

const file = fs
  .readFileSync("../p1/rucksack.txt", "utf-8")
  .match(/\w+\n\w+\n\w+/g);
const arr: any = file?.map((el) => el.split("\n"));

let total = 0;
for (const sack of arr) {
  let letters: any = [...new Set(sack.join(""))];
  for (const letter of letters) {
    if (
      sack[0].includes(letter) &&
      sack[1].includes(letter) &&
      sack[2].includes(letter)
    ) {
      let val = letter.charCodeAt(0);
      if (val > 96) {
        val -= 96;
      } else val -= 38;
      total += val;
      break;
    }
  }
}

console.log(`The total priority of the badges is ${total}`);
