import * as fs from "fs";
import { findNChars } from "./find_n_unique_chars";

const file = fs.readFileSync("./input.txt", "utf-8");

console.log(findNChars(file, 4));
