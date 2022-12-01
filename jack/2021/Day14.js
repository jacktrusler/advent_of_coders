const { dir } = require('console');
const fs = require('fs');
const [inputStr, directions] = fs.readFileSync('./Day14Input.txt', 'utf-8').split(/\n\n/);
const [exampleStr, exampleDirections] = fs.readFileSync('./Day14Example.txt', 'utf-8').split(/\n\n/)

function insertion(template, rules, steps){
  
  const ruleKey = {};
  const newRuleKey = {};

  const ruleArray = rules.split('\n')
  for (const rule of ruleArray) {
    const [k, r] = rule.split(" -> ");
    ruleKey[k] = r;
  }
  for (const [k, r] of Object.entries(ruleKey)) {
    newRuleKey[k] = r + k[1];
  }
  console.log(newRuleKey)
  console.log(template)
  //run function for specified number of steps
  let newTemplate = template;
  for (let i = 0; i < steps; i++){
    const pairs = [];
    for (var j = 0, charsLength = newTemplate.length; j < charsLength; j += 1) {
      pairs.push(newTemplate.substring(j, j + 2));
    }
    pairs.pop()
    //console.log(pairs)
    // filteredPairs = pairs.filter(pair => pair.length === 2);
    
    const newArr = [];
    newArr.push(template[0])
    for (const pair of pairs){
      if (pair.length === 2){
        newArr.push(newRuleKey[pair])
      } else {
        newArr.push(pair);
      }
    }
    
    newTemplate = newArr.join('')
    console.log(newTemplate)
  }
  //after the steps have completed
  //console.log(newTemplate)
  //count all the characters in the string
  const counts = {};
    for (const s of newTemplate) {
      if (counts[s]) {
        counts[s]++
      } else {
        counts[s] = 1
      }
    } 
  const minMax = Object.values(counts).sort((a,b) =>a-b);
  const [min, max] = [minMax[0], minMax[minMax.length - 1]]
  const final = max - min
  console.log(newTemplate.length)
  
}

function insertionFaster(input, rules, steps){

  const ruleKey = {};

  const ruleArray = rules.split('\n')
  for (const rule of ruleArray) {
    const [k, r] = rule.split(" -> ");
    ruleKey[k] = r;
  }

  //count key
  let inputKey = {};
  for (var j = 0, charsLength = input.length; j < charsLength; j += 1) {
    let current = input.substring(j, j+2)
    if (input.substring(j, j+2).length === 2){
      inputKey[current] = 1;
    }
  }


  let outputKey = {}
  for (let i = 0; i < steps; i++){
    outputKey = {}
    for (const [key, value] of Object.entries(inputKey)) {
      if (key.length === 2){
        if (outputKey[key[0] + ruleKey[key]]){
          outputKey[key[0] + ruleKey[key]] += value;
        } else {
          outputKey[key[0] + ruleKey[key]] = value;
        }
        if (outputKey[ruleKey[key] + key[1]]) {
          outputKey[ruleKey[key] + key[1]] += value;
        } else {
          outputKey[ruleKey[key] + key[1]] = value;
        }
      }
    }
    inputKey = outputKey;
  }

  const counts = {};
  for (const [key, value] of Object.entries(inputKey)) {
    if (counts[key[0]]){
      counts[key[0]] += value;
    } else {
      counts[key[0]] = value;
    }
    if (counts[key[1]]){
      counts[key[1]] += value;
    } else {
      counts[key[1]] = value;
    }
  }

  for (const [key, value] of Object.entries(counts)){
    counts[key] = Math.floor(value/2)
    if (key === input[0]){
      counts[key] += 1;
    } 
    if (key === input[input.length - 1]){
      counts[key] += 1;
    }
  }
  const minMax = Object.values(counts).sort((a,b) =>a-b);
  const [min, max] = [minMax[0], minMax[minMax.length - 1]]
  const final = max - min
  console.log(final)
}

const a = performance.now();

insertionFaster(inputStr, directions, 40);

const b = performance.now();
console.log('It took ' + (b - a) + ' ms.');

