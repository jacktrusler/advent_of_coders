const fs = require('fs');
const inputText = fs.readFileSync('./Day7Input.txt', 'utf-8');
const crabPositions = inputText.split(',').map(num=>parseInt(num))

//Part 1
const median = crabPositions.sort((a,b) => {return a-b})[499]

const fuelUsed = crabPositions.reduce((acc, val) => acc + (Math.abs(median - val)),0);

//Part 2


// const averageMan = Math.floor((crabPositions.reduce((acc,val) => acc + val))/(crabPositions.length));
function averageGet(arr){
  let acc = 0;
  for (let i of arr) {
    acc += i;
  }
  return acc / arr.length;
}

const average = Math.floor(averageGet(crabPositions))

const fuelCost = (pos) => {
  const n = Math.abs(pos - average)
  stepWiseAddition = n * (n+1) / 2;
  return stepWiseAddition; 
}

// const fuel = crabPositions.reduce((acc,val) => acc + fuelCost(val),0)
function actualFuelUsed(arr) {
  let acc = 0;
  for (let i of arr) {
    acc += fuelCost(i);
  }
  return acc;
}



const a = performance.now();
console.log(actualFuelUsed(crabPositions));
const b = performance.now();
console.log('It took ' + (b - a) + ' ms.');