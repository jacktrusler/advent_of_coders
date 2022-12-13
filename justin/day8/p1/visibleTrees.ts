import * as fs from "fs";

export class Tree {
  row: number;
  column: number;
  height: number;
  grid: number[][];
  constructor(row: number, column: number, height: number, grid: number[][]) {
    this.row = row;
    this.column = column;
    this.height = height;
    this.grid = grid;
  }

  visible(all: boolean = false) {
    //checks if visible from any direction
    return all
      ? this.up() && this.down() && this.left() && this.right()
      : this.up() || this.down() || this.left() || this.right();
  }

  private up() {
    // checks if visible from up
    for (let i = this.row - 1; i >= 0; i--) {
      if (grid[i][this.column] >= this.height) return false;
    }
    return true;
  }
  private down() {
    //checks if visible from down
    for (let i = this.row + 1; i < grid.length; i++) {
      if (grid[i][this.column] >= this.height) return false;
    }
    return true;
  }
  private left() {
    //checks if visible from left
    for (let i = this.column - 1; i >= 0; i--) {
      if (grid[this.row][i] >= this.height) return false;
    }
    return true;
  }
  private right() {
    //checks if visible from right
    for (let i = this.column + 1; i < grid[0].length; i++) {
      if (grid[this.row][i] >= this.height) return false;
    }
    return true;
  }
}

//Create grid of trees
const grid = fs
  .readFileSync("./input.txt", "utf-8")
  .split("\n")
  .map((a) => a.split("").map((b) => parseInt(b)));

//loop through trees and check if they are visible from the outside
const len = grid.length;
const wid = grid[0].length;
let visibleCount = 0;
grid.forEach((row, i) => {
  if (i === 0 || i === len - 1) {
    visibleCount += wid;
  } else {
    row.forEach((height, j) => {
      if (new Tree(i, j, height, grid).visible()) visibleCount++;
    });
  }
});
console.log(grid.length * grid[0].length);
console.log(visibleCount);
