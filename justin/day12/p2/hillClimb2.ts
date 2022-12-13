import * as fs from "fs";

const file = fs
  .readFileSync("../p1/input.txt", "utf-8")
  .split("\n")
  .map((a) => a.split(""));
let starts: number[][] = [];
let end: number[] = [];
for (let i = 0; i < file.length; i++) {
  for (let j = 0; j < file[0].length; j++) {
    if (file[i][j] === "S" || file[i][j] === "a") {
      starts.push([i, j]);
      file[i][j] = "a";
    }
    if (file[i][j] === "E") {
      end.push(i, j);
      file[i][j] = "z";
    }
  }
}
let minCount = Infinity;

while (starts.length) {
  let start: any = starts.shift();
  let visited = new Set(start.join(","));
  let q: number[][] = nextSteps(file, start, visited);
  let count = 1;
  while (q.length) {
    if (visited.has(end.join(","))) {
      minCount = Math.min(minCount, count);
      break;
    }
    count++;
    let tempq: any[] = [];
    for (const cell of q) {
      let arr = [...nextSteps(file, cell, visited)];
      tempq.push(...arr);
    }
    q = tempq;
  }
}
console.log(`The shortest path from start to finish is ${minCount}`);

function nextSteps(grid: string[][], cell: number[], visited: any) {
  let arr = [];
  const row: number = cell[0];
  const col: number = cell[1];
  const letter = grid[row][col];
  //up
  if (row > 0) {
    if (!visited.has([row - 1, col].join(",")) && grid[row - 1][col]) {
      if (grid[row - 1][col].charCodeAt(0) - letter.charCodeAt(0) <= 1) {
        arr.push([row - 1, col]);
        visited.add([row - 1, col].join(","));
      }
    }
  }
  //down
  if (row < grid.length - 1) {
    if (!visited.has([row + 1, col].join(",")) && grid[row + 1][col]) {
      if (grid[row + 1][col].charCodeAt(0) - letter.charCodeAt(0) <= 1) {
        arr.push([row + 1, col]);
        visited.add([row + 1, col].join(","));
      }
    }
  }
  //left
  if (col > 0) {
    if (!visited.has([row, col - 1].join(",")) && grid[row][col - 1]) {
      if (grid[row][col - 1].charCodeAt(0) - letter.charCodeAt(0) <= 1) {
        arr.push([row, col - 1]);
        visited.add([row, col - 1].join(","));
      }
    }
  }
  //right
  if (col < grid[0].length - 1) {
    if (!visited.has([row, col + 1].join(",")) && grid[row][col + 1]) {
      if (grid[row][col + 1].charCodeAt(0) - letter.charCodeAt(0) <= 1) {
        arr.push([row, col + 1]);
        visited.add([row, col + 1].join(","));
      }
    }
  }
  return arr;
}
