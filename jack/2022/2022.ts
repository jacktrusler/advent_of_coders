import { day1 } from "./day01"
import { day2 } from "./day02"
import { day3 } from "./day03"
import { day4 } from "./day04"
import { day5 } from "./day05"
import { day6 } from "./day06"
import { day7 } from "./day07"
import { day8 } from "./day08"
import { day9 } from "./day09"
import { day10 } from "./day10"
import { day11 } from "./day11"
import { day12 } from "./day12"
import { day13 } from "./day13"
import { day14 } from "./day14"

const t0 = performance.now();
day1("./day01.txt")
day2("./day02.txt")
day3("./day03.txt")
day4("./day04.txt")
day5("./day05.txt")
day6("./day06.txt")
day7("./day07.txt")
day8("./day08.txt")
day9("./day09.txt")
day10("./day10.txt")
day11("./day11.txt")
day12("./day12.txt")
day13("./day13.txt")
day14("./day14.txt")
const t1 = performance.now();
console.log(`all days took ${t1 - t0} milliseconds.`)
