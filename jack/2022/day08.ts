import { readFileSync } from "fs";

const answer = {
  part1: 0,
  part2: 0,
}

function day8(filePath: string) {
  const treeGridRows = readFileSync(filePath).toString().replace(/\n$/, "").split('\n')
  let vt = 0;
  let scenery = [];
  const treeGrid = treeGridRows.map((str) => str.split(""))
  for (let i = 0; i < treeGrid.length; i++) {
    // add 2 trees for index 0 and row.length
    vt = vt + 2
    let row = treeGrid[i]
    for (let j = 1; j < row.length - 1; j++) {
      // top and bottom trees are all visible
      if (i === 0 || i === treeGrid.length - 1) {
        vt++
        continue;
      }
      let ct = treeGrid[i][j]
      let lBlock = false, rBlock = false, tBlock = false, bBlock = false
      let lScene = 1, rScene = 1, tScene = 1, bScene = 1
      //left
      for (let k = j - 1; k >= 0; k--) {
        if (ct <= treeGrid[i][k]) {
          lBlock = true
          break;
        };
        if (k !== 0) lScene++;
      }
      //right
      for (let k = j + 1; k < row.length; k++) {
        if (ct <= treeGrid[i][k]) {
          rBlock = true
          break;
        };
        if (k !== row.length - 1) rScene++;
      }
      //top
      for (let k = i - 1; k >= 0; k--) {
        if (ct <= treeGrid[k][j]) {
          tBlock = true
          break;
        };
        if (k !== 0) tScene++;
      }
      //bottom
      for (let k = i + 1; k < treeGrid.length; k++) {
        if (ct <= treeGrid[k][j]) {
          bBlock = true;
          break;
        };
        if (k !== treeGrid.length - 1) bScene++;
      }

      if (!lBlock || !rBlock || !tBlock || !bBlock) {
        vt++
      }
      scenery.push(lScene * rScene * tScene * bScene)
    }
  }
  answer.part1 = vt;
  answer.part2 = Math.max(...scenery);
  console.log(answer)
  return answer
}

export { day8 }
