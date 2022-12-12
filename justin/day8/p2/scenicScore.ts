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
  scenicScore() {
    return this.viewUp() * this.viewDown() * this.viewLeft() * this.viewRight();
  }

  visible(all: boolean = false) {
    //checks if visible from any direction
    return all
      ? this.up() && this.down() && this.left() && this.right()
      : this.up() || this.down() || this.left() || this.right();
  }

  private viewUp() {
    let count = 0;
    for (let i = this.row - 1; i >= 0; i--) {
      count++;
      if (grid[i][this.column] >= this.height) return count;
    }
    return count;
  }

  private viewDown() {
    let count = 0;
    for (let i = this.row + 1; i < grid.length; i++) {
      count++;
      if (grid[i][this.column] >= this.height) return count;
    }
    return count;
  }

  private viewLeft() {
    let count = 0;
    for (let i = this.column - 1; i >= 0; i--) {
      count++;
      if (grid[this.row][i] >= this.height) return count;
    }
    return count;
  }

  private viewRight() {
    let count = 0;
    for (let i = this.column + 1; i < grid[0].length; i++) {
      count++;
      if (grid[this.row][i] >= this.height) return count;
    }
    return count;
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
  .readFileSync("../p1/input.txt", "utf-8")
  .split("\n")
  .map((a) => a.split("").map((b) => parseInt(b)));

//loop through trees and check if they are visible from the outside

let maxScore = 0;
grid.forEach((row, i) => {
  row.forEach((height, j) => {
    maxScore = Math.max(maxScore, new Tree(i, j, height, grid).scenicScore());
  });
});

console.log(`The maximum scenic score is ${maxScore}`);
