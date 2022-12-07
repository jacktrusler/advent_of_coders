import { readFileSync } from "fs";

const answer = {
  part1: 0,
  part2: 0,
}

class Dir {
  name: string;
  dirs: any;
  filesizes: number;
  parent: Dir;

  constructor(val: string, parent) {
    this.name = val;
    this.dirs = {};
    this.parent = parent
    this.filesizes = 0;
  }
}

class Filesystem {
  fedoraRoot: null | { [key: string]: any }
  constructor() {
    this.fedoraRoot = null;
  };

  createFilesystem(output: string[]): { [key: string]: any } {
    let current = this.fedoraRoot
    let root;
    for (let i = 0; i < output.length; i++) {
      let [x, y, z] = output[i].split(' ')
      if (z !== undefined) {
        if (!this.fedoraRoot) {
          const newDir = new Dir(z, z)
          this.fedoraRoot = newDir;
          current = this.fedoraRoot;
          root = this.fedoraRoot
          continue;
        }
      }

      if (y === "cd" && current !== null) {
        if (z === "..") {
          current = current.parent
          continue;
        }
        else if (z === "/") {
          current = root;
          continue;
        } else {
          const newDir = new Dir(z, current)
          current.dirs[z] = newDir;
          current = current.dirs[z];
          continue;
        }
      }
      if (x === 'dir' && current !== null) {
        const newDir = new Dir(y, current)
        current.dirs[y] = newDir;
        continue;
      }
      if (parseInt(x) > 0 && current !== null) {
        current.filesizes += parseInt(x)
        continue;
      }
    }

    return this.fedoraRoot;
  }
}

function getDirSizes(fs, arr = [], key?) {
  let childrenSize = 0;
  if (Object.keys(fs.dirs).length > 0) {
    for (const key of Object.keys(fs.dirs)) {
      childrenSize = childrenSize + getDirSizes(fs.dirs[key], arr, key)
    }
  }
  //fs.filesizes is the size of current dir
  const totalSize = fs.filesizes + childrenSize
  arr.push(totalSize)
  return totalSize;
}

function day7(filePath: string) {
  const outputAndCommands = readFileSync(filePath).toString().replace(/\n$/, "").split('\n')
  const fedoraFilesystem = new Filesystem().createFilesystem(outputAndCommands)
  const totals = []
  getDirSizes(fedoraFilesystem, totals)

  //part 1
  const part1 = totals
    .filter((dirSize) => dirSize <= 100000)
    .reduce((acc, thing) => thing + acc, 0)
  answer.part1 = part1;

  //part 2
  const UPDATE_SIZE = 30000000
  const availableSpace = 70000000 - Math.max(...totals)
  const spaceNeeded = UPDATE_SIZE - availableSpace
  const part2 = totals
    .filter((dirSize) => dirSize >= spaceNeeded)
    .sort((a, b) => a - b)

  answer.part2 = part2[0]

  console.log(answer);
  return answer;
}


day7("./day7.txt")
