import * as fs from "fs";

function sum(...nums: number[]) {
  return nums.reduce((a, b) => a + b);
}

const file = fs
  .readFileSync("./input.txt", "utf-8")
  .split("\n")
  .map((el) => el.split(" "));
//console.log(file);
const cycles: any[] = [20, 60, 100, 140, 180, 220];
let cycle = 0;
let x = 1;
let signals = [];
for (const line of file) {
  if (line.length === 1) {
    console.log(cycle, x, line);

    cycle++;
    cycle === cycles[0] && signals.push(x * cycles.shift());
    continue;
  } else {
    console.log(cycle, x, line[1]);
    cycle++;
    cycle === cycles[0] && signals.push(x * cycles.shift());
    cycle++;
    cycle === cycles[0] && signals.push(x * cycles.shift());
    x += parseInt(line[1]);
  }
}
console.log(signals);
console.log(sum(...signals));
