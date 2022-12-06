import { day1 } from "./day1"
import { day2 } from "./day2"
import { day3 } from "./day3"
import { day4 } from "./day4"
import { day5 } from "./day5"
import { day6 } from "./day6"

day1("./day1.txt")
day2("./day2.txt")
day3("./day3.txt")
day4("./day4.txt")
day5("./day5.txt")
const t0 = performance.now();
day6("./day6.txt")
const t1 = performance.now();
console.log(`Day 6 took ${t1 - t0} milliseconds.`)
