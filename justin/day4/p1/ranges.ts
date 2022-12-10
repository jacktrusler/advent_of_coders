import * as fs from "fs";

class ranges {
  start;
  end;

  constructor(...args: number[]) {
    this.start = Math.min(...args);
    this.end = Math.max(...args);
  }

  intersect(range: ranges) {
    return (
      (this.start >= range.start && this.start <= range.end) ||
      (range.start >= this.start && range.start <= this.end)
    );
  }
}

const file = fs.readFileSync("./input.txt", "utf-8").split("\n");
const arr = file.map((a) =>
  a.split(",").map((b) => b.split("-").map((c) => parseInt(c)))
);
let count = 0;
for (let i = 0; i < arr.length; i++) {
  let r1 = new ranges(...arr[i][0]);
  let r2 = new ranges(...arr[i][1]);
  if (r1.intersect(r2)) count++;
}
console.log(`There are ${count} pairs where one range fully contains another.`);
