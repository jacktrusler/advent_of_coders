import * as fs from "fs";

const file = fs.readFileSync("./input.txt", "utf-8").split("\n\n");
const moves: any[] = file[1]
  .split("\n")
  .map((el) => el.match(/\d+/g)?.map((b) => parseInt(b)));
// console.log(moves);
let invstacks: any = file[0]
  .split("\n")
  .reverse()
  .map((el) => el.match(/\s{2,4}|\w/g));
invstacks.shift();
let stacks: any[][] = Array(invstacks.length);
for (const invstack of invstacks) {
  invstack.forEach((crate: string, i: number) => {
    if (!crate.includes(" "))
      stacks[i] ? stacks[i].push(crate) : (stacks[i] = [crate]);
  });
}
//Stacks = starting orientation of crates in stacks
console.log("stacks", stacks);

function moveCrate(n: number, pos1: number, pos2: number, arr: any[][]) {
  //moves n chars from end of pos1 in array to end of pos2
  console.log(arguments);
  arr[pos2 - 1].push(
    ...arr[pos1 - 1].splice(arr[pos1 - 1].length - n).reverse()
  );
}

moves.forEach((move) => moveCrate(move[0], move[1], move[2], stacks));
let output = "";
stacks.forEach((stack) => (output += stack.at(-1)));
console.log(stacks, `The last crates from each stack spell ${output}`);
