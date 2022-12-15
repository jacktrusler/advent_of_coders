import { readFileSync } from "fs";

const answer = { part1: 0, part2: 0 };

function drawMap(rC: string[][]) {
  let caveHeight = 0;
  let caveWidthMax = 0;
  let caveWidthMin = Infinity;
  let i = 0;
  do {
    let j = 0;
    do {
      const [lhs, rhs] = rC[i][j].split(",");
      if (parseInt(rhs) > caveHeight) {
        caveHeight = parseInt(rhs);
      }
      if (parseInt(lhs) > caveWidthMax) {
        caveWidthMax = parseInt(lhs);
      }
      if (parseInt(lhs) < caveWidthMin) {
        caveWidthMin = parseInt(lhs);
      }
      j++;
    } while (j < rC[i].length);
    i++;
  } while (i < rC.length);

  const cave = [];
  for (let cH = 0; cH <= caveHeight; cH++) {
    const row = [];
    for (let cW = 0; cW <= caveWidthMax - caveWidthMin; cW++) {
      row.push(0);
    }
    cave.push(row);
  }
  return { cave, caveWidthMin };
}

function drawRocks(cave: number[][], rC: string[][], cW: number) {
  for (const coord of rC) {
    for (let i = 0; i < coord.length - 1; i++) {
      let [lhs1, rhs1] = coord[i].split(",");
      let [lhs2, rhs2] = coord[i + 1].split(",");
      if (lhs1 === lhs2) {
        let x = parseInt(lhs1) - cW;
        let y1 = parseInt(rhs1);
        let y2 = parseInt(rhs2);
        for (let k = Math.min(y1, y2); k <= Math.max(y1, y2); k++) {
          cave[k][x] = 8;
        }
      }
      if (rhs1 === rhs2) {
        let y = parseInt(rhs1);
        let x1 = parseInt(lhs1) - cW;
        let x2 = parseInt(lhs2) - cW;
        for (let k = Math.min(x1, x2); k <= Math.max(x1, x2); k++) {
          cave[y][k] = 8;
        }
      }
    }
  }
  return cave;
}

function day14(filePath: string) {
  const input = readFileSync(filePath)
    .toString()
    .replace(/\n$/, "")
    .split("\n");
  const rockCoordinates = input.map((coords) => coords.split(" -> "));
  const { cave, caveWidthMin } = drawMap(rockCoordinates);
  const caveWithRocks = drawRocks(cave, rockCoordinates, caveWidthMin);
  console.log(caveWithRocks)
}

day14("./day14small.txt");
