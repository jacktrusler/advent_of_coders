import { readFileSync } from "fs";

const answer = { part1: 0, part2: 0 };

function drawMap(rC: string[][]) {
  let caveHeight = 0;
  let caveWidth = 1000;
  let i = 0;
  do {
    let j = 0;
    do {
      const [lhs, rhs] = rC[i][j].split(",");
      if (parseInt(rhs) > caveHeight) {
        caveHeight = parseInt(rhs);
      }
      j++;
    } while (j < rC[i].length);
    i++;
  } while (i < rC.length);

  const caveP1 = [];
  for (let cH = 0; cH <= caveHeight; cH++) {
    const row = [];
    for (let cW = 0; cW <= caveWidth; cW++) {
      row.push(0);
    }
    caveP1.push(row);
  }
  //Part 2
  const caveP2 = [];
  for (let c = 0; c <= caveHeight + 2; c++) {
    const row = [];
    for (let cW = 0; cW <= caveWidth; cW++) {
      if (c === caveHeight + 2) {
        row.push(8)
        continue;
      }
      row.push(0);
    }
    caveP2.push(row);
  }
  return { caveP1, caveP2 };
}

function drawRocks(cave: number[][], rC: string[][]) {
  for (const coord of rC) {
    for (let i = 0; i < coord.length - 1; i++) {
      let [lhs1, rhs1] = coord[i].split(",");
      let [lhs2, rhs2] = coord[i + 1].split(",");
      if (lhs1 === lhs2) {
        let x = parseInt(lhs1);
        let y1 = parseInt(rhs1);
        let y2 = parseInt(rhs2);
        for (let k = Math.min(y1, y2); k <= Math.max(y1, y2); k++) {
          cave[k][x] = 8;
        }
      }
      if (rhs1 === rhs2) {
        let y = parseInt(rhs1);
        let x1 = parseInt(lhs1);
        let x2 = parseInt(lhs2);
        for (let k = Math.min(x1, x2); k <= Math.max(x1, x2); k++) {
          cave[y][k] = 8;
        }
      }
    }
  }
  return cave;
}
/** 
pouring from 500, 0
......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
......o.#.
#########.
I used 8 for rocks, 1 for sand, 0 for empty
*/
function dropSand(x, y, cR) {
  //sand coordinates
  let sC = [y, x]
  let dropTheBassalt = true
  while (dropTheBassalt) {
    // out of bounds
    if (sC[1] - 1 === - 1) { break; } // left
    if (sC[1] + 1 === cR[0].length) { break; } // right
    if (sC[0] + 1 === cR.length) { break; } // bottom
    // if space underneath is a 0
    if (cR[sC[0] + 1][sC[1]] === 0) {
      sC = [sC[0] + 1, sC[1]]
      continue;
    }
    // check diagonal left & right for sand or rock
    if (cR[sC[0] + 1][sC[1] - 1] > 0 && cR[sC[0] + 1][sC[1] + 1] > 0) {
      cR[sC[0]][sC[1]] = 1
      sC = [y, x]
      continue;
    }
    // check diagonal left and down
    if (cR[sC[0] + 1][sC[1] - 1] < 1) {
      sC = [sC[0] + 1, sC[1] - 1]
      continue;
    }
    // check diagonal right & down
    if (cR[sC[0] + 1][sC[1] + 1] < 1) {
      sC = [sC[0] + 1, sC[1] + 1]
      continue;
    }
  }
  answer.part1 = cR.flatMap((num: number[]) => num)
    .filter((space: number) => space === 1)
    .reduce((acc: number, sand: number) => sand + acc, 0)
}

function dropSandTwoOceanFloorBoogaloo(x, y, cR) {
  //sand coordinates
  let sC = [y, x]
  let dropTheBassalt = true
  while (dropTheBassalt) {
    if (cR[sC[0] + 1][sC[1] - 1] === 1 && cR[sC[0] + 1][sC[1] + 1] === 1 && sC[0] === 0 && sC[1] === 500) {
      cR[sC[0]][sC[1]] = 1;
      break;
    }
    // actually it's a rock now
    if (sC[0] + 1 > cR.length) {
      cR[sC[0]][sC[1]] = 8;
      sC = [y, x]
      continue;
    }
    // if space underneath is a 0
    if (cR[sC[0] + 1][sC[1]] === 0) {
      sC = [sC[0] + 1, sC[1]]
      continue;
    }
    // check diagonal left & right for sand or rock
    if (cR[sC[0] + 1][sC[1] - 1] > 0 && cR[sC[0] + 1][sC[1] + 1] > 0) {
      cR[sC[0]][sC[1]] = 1
      sC = [y, x]
      continue;
    }
    // check diagonal left and down
    if (cR[sC[0] + 1][sC[1] - 1] < 1) {
      sC = [sC[0] + 1, sC[1] - 1]
      continue;
    }
    // check diagonal right & down
    if (cR[sC[0] + 1][sC[1] + 1] < 1) {
      sC = [sC[0] + 1, sC[1] + 1]
      continue;
    }
  }
  answer.part2 = cR.flatMap((num: number[]) => num)
    .filter((space: number) => space === 1)
    .reduce((acc: number, sand: number) => sand + acc, 0)
}

function day14(filePath: string) {
  const input = readFileSync(filePath)
    .toString()
    .replace(/\n$/, "")
    .split("\n");
  const rockCoordinates = input.map((coords) => coords.split(" -> "));
  const { caveP1 } = drawMap(rockCoordinates);
  const { caveP2 } = drawMap(rockCoordinates);
  const caveWithRocks = drawRocks(caveP1, rockCoordinates);
  const cave2WithRocks = drawRocks(caveP2, rockCoordinates);

  dropSand(500, 0, caveWithRocks)
  dropSandTwoOceanFloorBoogaloo(500, 0, cave2WithRocks)
  console.log(answer)
  return answer
}

export { day14 }
