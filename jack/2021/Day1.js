import { readFileSync } from 'fs'

const readings = readFileSync("./Day1Input.txt")
  .toString()
  .replace(/\n$/, "")
  .split("\n")
  .map(Number)

function depthReading(arr) {
  let j = 0;
  for (let i = 0; i < arr.length; i++) {
    if (arr[i + 1] > arr[i]) {
      j++
    }
  }
  return j;
}

function slidingWindow(arr) {
  let j = 0;
  for (let i = 0; i < arr.length; i++) {
    if ((arr[i + 1] + arr[i + 2] + arr[i + 3]) > (arr[i] + arr[i + 1] + arr[i + 2])) {
      j++
    }
  }
  return j;
}

console.log(depthReading(readings));
console.log(slidingWindow(readings));
