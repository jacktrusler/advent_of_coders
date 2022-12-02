const fs = require('fs')

//part 1
//data in form ['input (10x) | output (4x)]
const inputData = fs.readFileSync('./Day8Input.txt', 'utf-8'); 
const parseOnDelimiters = inputData.split(/[\n|]/)
const len = parseOnDelimiters.length
//get output data only
function partOne(inputArr){
  const outputArr = [];
  for (let i = 0; i<len; i++){
    if (i % 2 === 1){
      outputArr.push(inputArr[i].trim().split(' '))
    }
  }
  //match codes that are 2,3,4, or 7 letters long, these are all unique
  const regex = /\b\w{5,6}\b/
  const newArr = outputArr.flat().filter((str)=> str.match(regex) == null);
  console.log(newArr.length)
}

//part 2

function partTwo(inputArr){
  const letterKey = {};
  const numberKey = {0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: ''}
  //get the input and output arrays
  const wireInput = [];
  const wireOutput = [];
  const theFinalPush = [];
  for (let i = 0; i<len; i++){
    if (i % 2 === 1){
      wireOutput.push(inputArr[i].trim())
    } else if (i % 2 === 0) {
    wireInput.push(inputArr[i].trim())
    }
  } 
  //count characters in input, put values into letterKey that are known: only 1 letter that repeats 9,6, and 4 times
  const countChar = (str, i) => {
    const counts = {};
    strNoSpace = str.replace(/ /g, "");
    for (const s of strNoSpace) {
      if (counts[s]) {
        counts[s]++
      } else {
        counts[s] = 1
      }
    } 
    function getKeyByValue(value) {
      return Object.keys(counts).find(key => counts[key] === value);
    }
    //wireInput[0] = gea agfcbe egcbfd aecb cegbf cafgde fgeba ea gabdf begfdca
    let eight = wireInput[i].match(/\b\w{7,7}\b/)[0].split('')
    let four = wireInput[i].match(/\b\w{4,4}\b/)[0].split('');
    let seven = wireInput[i].match(/\b\w{3,3}\b/)[0].split('');
    let one = wireInput[i].match(/\b\w{2,2}\b/)[0].split('');
    
    letterKey.rightLow = getKeyByValue(9);
    letterKey.leftHigh = getKeyByValue(6);
    letterKey.leftLow = getKeyByValue(4); 
    if (wireInput[i].match(/\b\w{2,2}\b/)[0][0] === letterKey.rightLow){
      letterKey.rightHigh = one[1]
    } else {
      letterKey.rightHigh = one[0]
    }
    letterKey.top = seven.filter(letter => !one.includes(letter))[0]
    
    letterKey.middle = four.filter(letter => 
      ![letterKey.rightHigh, letterKey.rightLow, letterKey.leftHigh].includes(letter))[0]

    letterKey.bottom = eight.filter(letter => 
      ![letterKey.rightHigh, letterKey.rightLow, letterKey.leftHigh, letterKey.leftLow, letterKey.top, letterKey.middle].includes(letter))[0]

    numberKey[0] = letterKey.top + letterKey.leftHigh + letterKey.rightHigh + letterKey.leftLow + letterKey.rightLow + letterKey.bottom
    numberKey[1] = letterKey.rightHigh + letterKey.rightLow
    numberKey[2] = letterKey.top + letterKey.rightHigh + letterKey.leftLow + letterKey.middle + letterKey.bottom
    numberKey[3] = letterKey.top + letterKey.rightHigh + letterKey.rightLow + letterKey.bottom + letterKey.middle
    numberKey[4] = letterKey.rightHigh + letterKey.rightLow + letterKey.middle + letterKey.leftHigh
    numberKey[5] = letterKey.top + letterKey.leftHigh + letterKey.rightLow + letterKey.middle + letterKey.bottom 
    numberKey[6] = letterKey.top + letterKey.leftHigh + letterKey.leftLow + letterKey.rightLow + letterKey.bottom + letterKey.middle
    numberKey[7] = letterKey.rightHigh + letterKey.rightLow + letterKey.top
    numberKey[8] = letterKey.top + letterKey.leftHigh + letterKey.leftLow + letterKey.rightLow + letterKey.bottom + letterKey.middle + letterKey.rightHigh
    numberKey[9] = letterKey.rightHigh + letterKey.rightLow + letterKey.middle + letterKey.leftHigh + letterKey.top + letterKey.bottom
  }

  function anagrams(stringA, stringB) {
    return cleanString(stringA) === cleanString(stringB);
  }

  function cleanString(str) {
    return str.replace(/[^\w]/g).toLowerCase().split('').sort().join()
  }  

  for (let i = 0; i < 200; i++){
    countChar(wireInput[i],i);
    const newWireOutput = wireOutput[i].split(' ')
    let final = ''; 
    for (let j = 0; j<4; j++){
      for (const [key, value] of Object.entries(numberKey)){
        if (anagrams(value, newWireOutput[j])){
          final += key;
        }
      }
    }
    theFinalPush.push(final);
  }
  console.log(theFinalPush);
 
  console.log(theFinalPush.reduce((acc,val) => acc + parseInt(val),0));
  //console.log(wireOutput);
}

const a = performance.now();

partTwo(parseOnDelimiters)

const b = performance.now();
console.log('It took ' + (b - a) + ' ms.');
