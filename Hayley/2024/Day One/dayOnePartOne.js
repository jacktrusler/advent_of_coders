function numberSorter(a, b) {
  return a - b;
}
const fs = require("fs");
const lines = fs.readFileSync("dayOne", { encoding: "utf8" }).split("\n");

console.log(lines[0].split(" "));
const leftNumbers = [];
const rightNumbers = [];

for (let line of lines) {
  const parts = line.split("   ");
  if (parts.length === 2) {
    leftNumbers.push(Number(parts[0]));
    rightNumbers.push(Number(parts[1]));
  }
}

leftNumbers.sort(numberSorter);
rightNumbers.sort(numberSorter);

let totalDistance = 0;
for (let i = 0; i < leftNumbers.length; i++) {
  let distance = Math.abs(leftNumbers[i] - rightNumbers[i]);
  totalDistance += distance;
}
console.log(totalDistance);
