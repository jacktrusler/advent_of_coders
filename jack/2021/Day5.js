const fs = require('fs')

const fileInput = fs.readFileSync('./Day5Input.txt', 'utf-8');
const inputSplit = fileInput.split(/\n|->|,/).map((numStr) => parseInt(numStr, 10));

function ventField(numArr){
  const fieldArr = []; 
  //populate field arr
  const max = Math.max(...numArr) + 1
  for (let i = 0; i<max; i++){
    const row = new Array(max).fill(0);
    fieldArr.push(row);
  }
  const chonk = 4; 
  for (let i=0; i<numArr.length; i+=chonk){
    const [x1,y1,x2,y2] = [numArr[i], numArr[i+1], numArr[i+2], numArr[i+3]] 
    //if x1 === x2 index x and add 1 to every y position visa versa for y1 === y2
    if (x1 === x2){
      const startingValue = y1 < y2 ? y1 : y2
      for (let y = startingValue; y<=(startingValue+(Math.abs(y2-y1))); y++){
        fieldArr[y][x1] += 1
      }
    } else if (y1 === y2) {
      const startingValue = x1 < x2 ? x1 : x2
      for (let x = startingValue; x<=(startingValue+(Math.abs(x2-x1))); x++){
        fieldArr[y1][x] += 1
      }
      //diagonals
    } else if (x1 - y1 === x2 - y2){
      const startingValueX = x1 < x2 ? x1 : x2
      let startingValueY = y1 < y2 ? y1 : y2
      for (let x = startingValueX; x<=(startingValueX+(Math.abs(x2-x1))); x++){
        fieldArr[startingValueY++][x] += 1
      }
    } else if (Math.abs(x1 - x2) === (Math.abs(y1-y2))){
      const startingValueX = x1 < x2 ? x1 : x2
      let startingValueY = y1 < y2 ? y2 : y1
      for (let x = startingValueX; x<=(startingValueX+(Math.abs(x2-x1))); x++){
        fieldArr[startingValueY--][x] += 1
      }
    }
  }
  //filter the array to only contain numbers greater than 1
  const overlappingLines = fieldArr.flat().filter(num=>num>1);
  return overlappingLines.length
}

