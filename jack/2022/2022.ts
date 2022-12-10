import { day1 } from "./day01"
import { day2 } from "./day02"
import { day3 } from "./day03"
import { day4 } from "./day04"
import { day5 } from "./day05"
import { day6 } from "./day06"
import { day7 } from "./day07"
import { day8 } from "./day08"

day1("./day01.txt")
day2("./day02.txt")
day3("./day03.txt")
day4("./day04.txt")
day5("./day05.txt")
day6("./day06.txt")
day7("./day07.txt")
const t0 = performance.now();
day8("./day08.txt")
const t1 = performance.now();
console.log(`Day 8 took ${t1 - t0} milliseconds.`)
