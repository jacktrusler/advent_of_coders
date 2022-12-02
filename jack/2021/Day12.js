const fs = require ('fs');
dataInput = fs.readFileSync('./Day12Input.txt', 'utf-8');

const exampleInput = 
`start-A
start-b
A-c
A-b
b-d
A-end
b-end`

exampleArr = exampleInput.split('\n')

const directions = dataInput.split('\n')

const paths = {}; 

//build the cave system
const caveLayout = (arr) => {
  const caveSystem = {};
  //make an object of directions the letter could point to
  for (const line of arr) {
    const [b, e] = line.split("-");
    caveSystem[b] = [...(caveSystem[b] ?? []), e];
    caveSystem[e] = [...(caveSystem[e] ?? []), b];
  }
  for (const [key,value] of Object.entries(caveSystem)){
    caveSystem[key] = value.filter(val => !val.includes('start'))
  }
  return caveSystem;
}

console.log(caveLayout(exampleArr));

//part 1
const exploreCave1 = (cave, lowerCaveCache, caveSystem) => {
  if (cave === 'end'){
    return 1;
  }

  if(cave === 'start'){
    let safe = 0;
    for (let c of caveSystem[cave]){
      safe += exploreCave1(c, lowerCaveCache, caveSystem)
    }
    return safe;
  }

  const isLowerCase = (string) => /^[a-z]*$/.test(string)
  if (lowerCaveCache[cave]){
    return 0;
  }

  if (isLowerCase(cave)){
      lowerCaveCache[cave] = true;
  }

  let sum = 0
  for (let c of caveSystem[cave]){
  sum += exploreCave1(c, lowerCaveCache, caveSystem)
    }
    delete lowerCaveCache[cave]
    return sum; 
}

//part 2
const exploreCave2 = (cave, lowerCaveCache, caveSystem) => {
  if (cave === 'end'){
    return 1;
  }

  if(cave === 'start'){
    let safe = 0;
    for (let c of caveSystem[cave]){
      safe += exploreCave2(c, lowerCaveCache, caveSystem)
    }
    return safe;
  }

  if (lowerCaveCache[cave] === 3){
    return 0;
  }

  const isLowerCase = (string) => /^[a-z]*$/.test(string)
  if (isLowerCase(cave)){
    if (lowerCaveCache[cave] === 2){
      return 0; 
    }
    if (lowerCaveCache[cave] && Object.values(lowerCaveCache).some(visits => visits === 2)){
      return 0;
    }
    if (!lowerCaveCache[cave]){
      lowerCaveCache[cave] = 0;
    }
    lowerCaveCache[cave]++
  }

  let sum = 0
  for (let c of caveSystem[cave]){
  sum += exploreCave2(c, lowerCaveCache, caveSystem)
    }
    lowerCaveCache[cave]--
    return sum;
}

const a = performance.now();

console.log(exploreCave2('start',{},caveLayout(directions)));

const b = performance.now();
console.log('It took ' + (b - a) + ' ms.');
