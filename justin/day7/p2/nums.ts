import * as fs from "fs";

const file = fs.readFileSync("../p1/input.txt", "utf-8").split("\n");
const nums = file.filter((a) => a.match(/^[0-9]/g));
let check = nums.reduce((a: any, b: any) => a + parseInt(b.split(" ")[0]), 0);
console.log(check);
