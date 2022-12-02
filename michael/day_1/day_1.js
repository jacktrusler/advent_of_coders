//day_1 AOC 2022 with Node
const fs = require('fs');

const [fullData, testData] = ["./michael/day_1/day_1.txt", "./michael/day_1/day_1_min.txt"]

const executionTime = (func, data) =>{
    console.time(`${func.name} time:`)
    const result = func(data);
    console.timeEnd(`${func.name} time:`)
    console.log(`${func.name} Result: ${result}`)
    return result
}

const partOne = (calorieGroups) => {
    const arrSums = calorieGroups.map(x => x.reduce((a, b) => a + b))
    const max = arrSums.reduce((a, b) => Math.max(a, b), -Infinity);
    return max
}

const partTwo = (calorieGroups) => {
    const arrSums = calorieGroups.map(x => x.reduce((acc, current) => acc + current))
    const maxSorted = arrSums.sort((a,b) => a-b).slice(-3)
                           .reduce((a, b) => a + b) 
    return maxSorted
}

const buffer = fs.readFileSync(fullData);
let data = buffer.toString().split("\r\n\r");
data = data.map(x => x.split("\r\n").map(y => +y.replace("\n", "")))

executionTime(partOne, data)
executionTime(partTwo, data)


