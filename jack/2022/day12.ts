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
  let startArr: Point[] = [];
  let end: Point
  const topography: Point[][] = heightMap
    .map((str, y) => str.split('').map((char, x) => {
      let c = char.charCodeAt(0)
      if ((c === 97 || c === 83) && x === 0) {
        //S
        let start = Point({ x: x, y: y }, 0, 0, 0, 0)
        startArr.push(start)
        return start
      }
      if (c === 69) {
        //E
        end = Point({ x: x, y: y }, 0, 0, 0, 26)
        return end
      }
      if (c > 83) return Point({ x: x, y: y }, 0, 0, 0, c - 97)
    }))
  return { topography, startArr, end };
}

function neighbors(grid, point) {
  const ns = [];
  const y = point.pos.y;
  const x = point.pos.x;

  //check if the path is too high
  if (grid[y - 1] && grid[y - 1][x]) {
    if ((grid[y - 1][x].height - grid[y][x].height) < 2) {
      ns.push(grid[y - 1][x]);
    }
  }
  if (grid[y + 1] && grid[y + 1][x]) {
    if ((grid[y + 1][x].height - grid[y][x].height) < 2) {
      ns.push(grid[y + 1][x]);
    }
  }
  if (grid[y][x - 1] && grid[y][x - 1]) {
    if ((grid[y][x - 1].height - grid[y][x].height) < 2) {
      ns.push(grid[y][x - 1]);
    }
  }
  if (grid[y][x + 1] && grid[y][x + 1]) {
    if ((grid[y][x + 1].height - grid[y][x].height) < 2) {
      ns.push(grid[y][x + 1]);
    }
  }
  return ns;
}


function day12(filePath: string) {
  const { topography, startArr, end } = heightMap(filePath)
  function walkerTexasTester(start: Point) {
    const openList = [start]
    const searched = []

    while (openList.length > 0) {
      let lowIndex = 0;
      for (let j = 0; j < openList.length; j++) {
        if (openList[j].f < openList[lowIndex].f) { lowIndex = j }
      }
      const currentP = openList[lowIndex];

      //End Case -- Walk back
      if (currentP.height === 26) {
        let curr = currentP;
        const ret = [];
        while (curr.parent) {
          ret.push(curr)
          curr = curr.parent
        }
        return currentP.g
      }
      //Normal Case
      const point = openList.shift()
      searched.push(point)
      const n = neighbors(topography, point)
      for (let i = 0; i < n.length; i++) {
        const neighbor = n[i]

        if (!searched.includes(neighbor)) {
          const gScore = currentP.g + 1;

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

  let searchArrays = []
  for (let i = 0; i < startArr.length; i++) {
    searchArrays.push(walkerTexasTester(startArr[i]))
    topography.forEach((row) => row.forEach((point) => { point.h = 0; point.f = 0; point.g = 0; point.parent = null }))
  }
  answer.part1 = searchArrays[20]
  answer.part2 = Math.min(...searchArrays) - 1
}

export { day12 }
