const fs = require('fs');
inputData = fs.readFileSync('./Day11Input.txt','utf-8');

//const inputGrid = inputData.split('\n')
const inputGrid = inputData.split('\n').map(input=> input.split('').map(str=>parseInt(str, 10)))

function dayEleven(arr,steps){
  let len = arr.length //10x10 grid
  let flashy = arr;
  let flashCount = 0;

  function isSurrounding(arr, i,j){
    //out of bounds
    if (i >= len || j >= len || i < 0 || j < 0){
      return;
    } 
  
    if (arr[i][j] === 'Greg'){
      return; 
    }

    arr[i][j]++

    if (arr[i][j] > 9){
      arr[i][j] = 'Greg';
      isSurrounding(arr, i-1, j-1) //lawful good
      isSurrounding(arr, i-1, j) //neutral good
      isSurrounding(arr, i-1, j+1) //chaotic good
      isSurrounding(arr, i, j-1) //lawful neutral
      isSurrounding(arr, i, j+1) //chatoic neutral
      isSurrounding(arr, i+1, j-1) //lawful evil
      isSurrounding(arr, i+1, j) //neutral evil
      isSurrounding(arr, i+1, j+1) //chaotic evil
      flashCount++
      return;
    }  
  }

  let GregCounter = 0;
  function scanAndIncrement(){ 
    GregCounter = 0;
    for (let i = 0; i<len; i++){
      for (let j = 0; j<len; j++){
        if (flashy[i][j] === 'Greg'){
          GregCounter++
          flashy[i][j] = 0;        
        }
      }
    }

    for (let i = 0; i<len; i++){
      for (let j = 0; j<len; j++){
        isSurrounding(flashy,i,j);
      }
    }
  }
  //Part 2
  let stepCounter = 0;
  for (let i = 0; i<steps; i++){
    scanAndIncrement();
    if (GregCounter === 100){
      console.log(`--- 100 Simultaneous Blinkos were found on step: ${stepCounter} ---`)   
    } 
    stepCounter++
  }
  //Part 1
  console.log(`--- Flash Count: ${flashCount} after ${stepCounter} steps ---`)
}

dayEleven(inputGrid,500);