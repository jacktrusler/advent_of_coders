const fs = require ('fs'); 
const inputData = fs.readFileSync('./Day6Input.txt','utf-8')
const fisholasCage = inputData.split(',').map(num=>parseInt(num, 10))

//count number of fish in each day, push day 0 out and add to day 6 and day 8

function countingFeesh(fishArr){
  //[day0,day1,day2,day3,day4,day5,day6,day7,day8]
  const fishCountPerDay = new Array(9).fill(0); 
  fishArr.forEach(num=>fishCountPerDay[num] = fishCountPerDay[num] + 1)
  maxFishAge = 9; //9 days counting day 0
  const days=256;
  for (let i = 0; i<days; i++){
    let extraFish = 0;
    //decrement all indexes one to the left
    for(let j = 0; j<maxFishAge; j++){
      if (j===0){
        extraFish = fishCountPerDay[j];
      }
      fishCountPerDay[j-1] = fishCountPerDay[j]; 
    }
    //add amount of fish in 0 position to day 6 and day 8 position
    fishCountPerDay[6] = fishCountPerDay[6] + extraFish
    fishCountPerDay[8] = extraFish  
  }
  return fishCountPerDay.reduce((acc,val) => acc+val);
}

//check Performance
const a = performance.now();
console.log(countingFeesh(fisholasCage));
const b = performance.now();
console.log('It took ' + (b - a) + ' ms.');
