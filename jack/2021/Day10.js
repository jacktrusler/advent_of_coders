const fs = require('fs'); 

const inputData = fs.readFileSync('./Day10Input.txt','utf-8').split('\n');
const lmao = inputData.map(string=>string.split(''));
len = lmao.length

valueDict = {
  ')': 3,
  ']': 57,
  '}': 1197,
  '>': 25137
}

countUp = {
  '(': ')',
  '[': ']',
  '{': '}',
  '<': '>' 
}

countDown = {
  ')': '(',
  ']': '[',
  '}': '{',
  '>': '<'
}

function partOne(arr){
  const chunkos = [];
  const badBoys = [];
  for (let i = 0; i<len; i++){ 
    rowLen = arr[i].length
    for (let j = 0; j<rowLen; j++){
      if (arr[i][j] in countUp){
      chunkos.push(arr[i][j])
      }
      if (arr[i][j] in countDown && countDown[arr[i][j]] !== chunkos[chunkos.length - 1]){
        badBoys.push(arr[i][j]);
        break;
      }
      if (arr[i][j] in countDown && countDown[arr[i][j]] === chunkos[chunkos.length - 1] ){
        chunkos.pop() 
      }
      
      
    }
  }
  const ans = badBoys.map(key => valueDict[key]).reduce((acc,val)=>acc+val,0)
  return ans ;
}

valueDict2 = {
  '(': 1,
  '[': 2,
  '{': 3,
  '<': 4
}

const example = [
  ['{','{','[','[','(','{','(','['],
  ['(','{','<','[','{','('],
  ['{','{','<','{','<','(','(','(','('],
  ['[','[','{','{','[','{','[','{','<'],
  ['[','(','{','<']
]

function partTwo(arr){
  const incompleteBoys = [];
  for (let i = 0; i<arr.length; i++){ 
    const chunkos = [];
    rowLen = arr[i].length
    for (let j = 0; j<rowLen; j++){
      if (arr[i][j] in countUp){
      chunkos.push(arr[i][j])
      }
      
      if (arr[i][j] in countDown && countDown[arr[i][j]] !== chunkos[chunkos.length - 1]){
        chunkos.push('yikes')
        break;
      }
       
      if (arr[i][j] in countDown && countDown[arr[i][j]] === chunkos[chunkos.length - 1] ){
        chunkos.pop() 
      }  
    }
    incompleteBoys.push(chunkos);
  }

  function valueGet(arr){
    return arr.map(key => valueDict2[key]).reduce((acc,val) => (acc*5)+val,0)
  }
  //if array includes 'yikes' filter those arrays out

  const filteredArr = incompleteBoys.filter((miniArr) => !miniArr.includes('yikes')).map(arr=>arr.reverse());
  const valueArr = filteredArr.map((miniArr) => valueGet(miniArr))
  console.log(valueArr.sort((a,b) => a-b)[(valueArr.length - 1)/2]);
  
}

console.log(partOne(lmao))
console.log(partTwo(lmao))