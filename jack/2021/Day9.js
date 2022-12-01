const fs = require('fs');
const inputData = fs.readFileSync('./Day9Input.txt', 'utf-8'); 

const inputGrid = inputData.split('\n')
const eachLineIsArray = inputGrid.map(input=> input.split('').map(str=>parseInt(str, 10)))

function partOne(arr){
  const partOneArr = [];
  len = arr.length

  function isLowerThan(val,i,j){
    //checks corners and edges, if they exist, return true (numbers are always lower than out of bounds)
    if (i >= len || j >= len || i < 0 || j < 0){
      return true;
    } else {
      return val < arr[i][j];
    }
  }

  for (let i = 0; i<len; i++){
    smallerArrLen = arr[i].length
    for (let j = 0; j<smallerArrLen; j++){
      currentNum = arr[i][j]
      if ( isLowerThan(currentNum, i+1, j) 
        && isLowerThan(currentNum, i, j+1)  
        && isLowerThan(currentNum, i-1, j)  
        && isLowerThan(currentNum, i, j-1) ){
          partOneArr.push(currentNum);
      }
    }
  }
  return partOneArr.reduce((acc, value) => acc + (value + 1), 0); 
}

function partTwo(arr){
  const basinSizes = [];
  len = arr.length; 
  const searchBasin = (arr, i, j) => {
    if (i >= len || j >= len || i < 0 || j < 0){
      return 0;
    }
    if (arr[i][j] === 9){
      return 0; 
    }
    arr[i][j] = 9;
    return 1 +
      searchBasin(arr, i-1, j) +
      searchBasin(arr, i, j+1) + 
      searchBasin(arr, i+1, j) + 
      searchBasin(arr, i, j-1)
    
  };

  for (let i = 0; i<len; i++){
    smallerArrLen = arr[i].length
    for (let j = 0; j<smallerArrLen; j++){
      if (arr[i][j] !== 9){
        basinSizes.push(searchBasin(arr,i,j))
      }
      
    }
  }
  const [x,y,z] = basinSizes.sort((a,b) => b>=a ? 1 : -1);
  return x*y*z;
}

const a = performance.now();

console.log(partTwo(eachLineIsArray));

const b = performance.now();
console.log('It took ' + (b - a) + ' ms.');

