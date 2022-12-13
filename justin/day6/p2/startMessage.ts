import { timeStamp } from "console";
import * as fs from "fs";
import { findNChars } from "../p1/find_n_unique_chars";

let a = timeStamp();
console.log(a);
console.log(findNChars(fs.readFileSync("../p1/input.txt", "utf-8"), 14));
