function countOccurrences(numberToFind, arrayOfNumbers) {
  let numberOfOccurrences = 0;
  for (let number of arrayOfNumbers) {
    if (number === numberToFind) {
      numberOfOccurrences++;
    }
  }
  return numberOfOccurrences;
}
const fs = require("fs");
const lines = fs.readFileSync("dayOne", { encoding: "utf8" }).split("\n");

const leftNumbers = [];
const rightNumbers = [];

// Split file into two arrays, one of all the left numbers and one of all the right
for (let line of lines) {
  const parts = line.split("   ");
  if (parts.length === 2) {
    leftNumbers.push(Number(parts[0]));
    rightNumbers.push(Number(parts[1]));
  }
}

let totalSimilarity = 0;
for (const number of leftNumbers) {
  const similarity = number * countOccurrences(number, rightNumbers);
  totalSimilarity += similarity;
}
console.log(totalSimilarity);
