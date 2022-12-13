import * as fs from "fs";

function sum(...nums: number[]) {
  return nums.reduce((a, b) => a + b);
}

const file = fs
  .readFileSync("../p1/input.txt", "utf-8")
  .split("\n")
  .map((el) => el.split(" "));
let output: string[] = [];
let row: string[] = [];
let cycle = 0;
let x = 1;

for (const line of file) {
  if (line.length === 1) {
    writePixel(x, cycle, row, output);
    cycle++;
    continue;
  } else {
    writePixel(x, cycle, row, output);
    cycle++;
    writePixel(x, cycle, row, output);
    cycle++;
    x += parseInt(line[1]);
  }
}
output.push(row.join(""));
fs.writeFile("./render.txt", output.join("\n"), (err) => console.log(err));
console.log("Render Complete!");

function writePixel(x: number, cycle: number, row: string[], output: string[]) {
  let col = ((cycle - 1) % 40) + 1;
  let sprite = [x - 1, x, x + 1];
  if (col === 1 && cycle > 1) {
    output.push(row.join(""));
    row.length = 0;
  }
  sprite.includes(col) ? row.push("#") : row.push(".");
}
