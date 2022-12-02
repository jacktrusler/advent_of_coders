const fs = require ('fs'); 

const inputData = fs.readFileSync('./Day6Input.txt','utf-8')
const fishiesArr = inputData.split(',').map(num=>parseInt(num, 10))

fishCount = 1;
nicolasFishCage = []; 
function fishyMultiplier(input, day){
  if (day >= 80){
    return fishCount;
  }
  for (let i = input; i >= 0; i--){
    day++
    if ((i === 0) && (day <=80)){
      fishCount += 1
      fishyMultiplier(6, day)
      fishyMultiplier(8, day)
      break;
    }  
  }
}

//fishyMultiplier(1,0);
// fishyMultiplier(2,0);
// fishyMultiplier(3,0);
//fishyMultiplier(4,0);
//fishyMultiplier(5,0);
// const fishDay6 = fishyMultiplier(6,0);

const map = new Map()
map.set(1,6206821033)
map.set(2,5617089148)
map.set(3,5217223242)
map.set(4,4726100874)
map.set(5,4368232009)

function fishyAdder(fishyArr){
  let acc = 0;
  for (let i = 0; i<fishyArr.length; i++){
    acc += map.get(fishyArr[i])
  }
  return acc;
}

console.log(fishyAdder(fishiesArr));