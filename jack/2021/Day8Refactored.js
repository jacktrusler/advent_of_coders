const fs = require('fs')

const inputData = fs.readFileSync('./Day8Input.txt', 'utf-8'); 
const parseOnDelimiters = inputData.split('\n').map(line => line.split(' | '))

function partTwo(inputs){
  //count characters in input, put them in 'counts' dictionary
  const makeFrequencyMap = (str) => 
    [...str].reduce((map, c) => {
      map[c] = (map[c] + 1 || 1);
      return map
    }, {});
  
  //each number is a unique sum, map sums to their corresponding numbers
  const addedNumbers = {
    '42': '0',
    '17': '1',
    '34': '2',
    '39': '3',
    '30': '4', 
    '37': '5',
    '41': '6',
    '25': '7',
    '49': '8',
    '45': '9'
  };

  return inputs.map(([wireIn, wireOut]) => {
    const frequencyMap = makeFrequencyMap(wireIn);
    return wireOut
      .split(' ')
      .map(output => [...output]
          .map(char => frequencyMap[char])
          .reduce((acc, val) => acc + val, 0))
      .map(key => addedNumbers[String(key)])
      .join('');
  })
  .reduce((acc, decodedOutput) => acc + parseInt(decodedOutput, 10), 0);
}

const a = performance.now();
console.log(partTwo(parseOnDelimiters));
const b = performance.now();

console.log('It took ' + (b - a) + ' ms.');