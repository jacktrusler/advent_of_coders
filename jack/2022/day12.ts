import { readFileSync } from "fs";

const answer = { part1: 0, part2: 0, }

interface Point {
  pos: { x: number, y: number }
  f: number,
  g: number,
  h: number,
  height: number,
  parent: null | Point,
}
const Point = (pos, f, g, h, height, parent = null) => {
  return {
    pos, f, g, h, height, parent
  }
}

function heuristic(pos0: Point, pos1: Point) {
  let y = Math.abs(pos0.pos.y - pos1.pos.y)
  let x = Math.abs(pos0.pos.x - pos1.pos.x)
  return y + x
}

function heightMap(filePath: string) {
  const heightMap = readFileSync(filePath).toString().replace(/\n$/, "").split('\n')
  let start: Point;
  let end: Point
  const topography: Point[][] = heightMap
    .map((str, y) => str.split('').map((char, x) => {
      let c = char.charCodeAt(0)
      if (c === 83) {
        //S
        start = Point({ x: x, y: y }, 0, 0, 0, 0)
      }
      if (c === 69) {
        //E
        end = Point({ x: x, y: y }, 0, 0, 0, 0)
      }
      if (c > 69) return Point({ x: x, y: y }, 0, 0, 0, c - 97)
    }))
  return { topography, start, end };
}

function neighbors(grid, point) {
  const ns = [];
  const y = point.pos.y;
  const x = point.pos.x;

  if (grid[y - 1] && grid[y - 1][x]) {
    ns.push(grid[y - 1][x]);
  }
  if (grid[y + 1] && grid[y + 1][x]) {
    ns.push(grid[y + 1][x]);
  }
  if (grid[y][x - 1] && grid[y][x - 1]) {
    ns.push(grid[y][x - 1]);
  }
  if (grid[y][x + 1] && grid[y][x + 1]) {
    ns.push(grid[y][x + 1]);
  }
  return ns;
}


function day12(filePath: string) {
  const { topography, start, end } = heightMap(filePath)
  const openList = [start]
  const searched = []

  while (openList.length > 0) {
    let lowInd = 0;
    for (let i = 0; i < openList.length; i++) {
      if (openList[i].f < openList[lowInd].f) { lowInd = i }
    }
    const currentP = openList[lowInd];

    //End Case -- Walk back
    if (currentP.height === 26) {
      let curr = currentP;
      const ret = [];
      while (curr.parent) {
        ret.push(curr)
        curr = curr.parent
      }
      console.log(ret.reverse)
      return ret.reverse();
    }
    //Normal Case
    const point = openList.pop()
    searched.push(point)
    const n = neighbors(topography, point)
    for (let i = 0; i < n.length; i++) {
      const neighbor = n[i]
      const gScore = currentP.g + 1;

      if (!searched.includes(neighbor)) {
        let possibleG = currentP.g + 1;

        if (!openList.includes(neighbor)) {
          openList.push(neighbor);
        } else if (gScore >= neighbor.g) {
          continue;
        }

        neighbor.g = gScore;
        neighbor.h = heuristic(neighbor, end)
        neighbor.f = neighbor.g + neighbor.h;
        neighbor.parent = currentP;
      }
    }
  }
}

day12('./day12.txt')
