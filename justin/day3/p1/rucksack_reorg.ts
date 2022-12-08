import * as fs from "fs";

const file = fs.readFileSync("./rucksack.txt", "utf-8").split("\n");
const rucksacks = file.map((a) => [
  a.slice(0, a.length / 2),
  a.slice(a.length / 2),
]);
let total = 0;
for (let j = 0; j < rucksacks.length; j++) {
  let sack = rucksacks[j];
  for (let i = 0; i < sack[0].length; i++) {
    if (sack[1].includes(sack[0][i])) {
      let val = sack[0].charCodeAt(i);
      if (val > 96) {
        val -= 96;
      } else val -= 38;
      total += val;
      //console.log(sack[0], sack[1], sack[0][i], val, j, total);
      break;
    }
  }
}
console.log(
  `The total priority of the item type that appears in both compartments of each rucksack is ${total}`
);
