const { count } = require('console');
const fs = require ('fs'); 
const inputData = fs.readFileSync('./Day6Input.txt','utf-8')
const fisholasCage = inputData.split(',').map(num=>parseInt(num, 10))

//memoize (memoization is caching a functions return values to avoid recomputation)
//start at day 0
//countingPerFeesh(3, 20, cache)

//create a cache
cache = {};
function countingPerFeesh(fishAge,daysLeftToMultiply,cache){
  //base case
  
  if (daysLeftToMultiply === 0){
    return 1;
  }
  const cacheKey = `${fishAge},${daysLeftToMultiply}`
  //if answer already in cache return cache value
  if (cache[cacheKey]) {
    return cache[cacheKey];
  }

  if (fishAge === 0){
    daysLeftToMultiply--
    return countingPerFeesh(6,daysLeftToMultiply, cache) + countingPerFeesh(8,daysLeftToMultiply,cache);
  }

  fishAge--
  daysLeftToMultiply--
  return cache[cacheKey] = countingPerFeesh(fishAge, daysLeftToMultiply,cache);  
}

const a = performance.now();
const result = fisholasCage.reduce((sum, fish) => sum + countingPerFeesh(fish, 256, {}), 0);
console.log(result)
const b = performance.now();
console.log('It took ' + (b - a) + ' ms.');


// function fibonacci2(n,memo) {
//   console.log(memo)
//   memo = memo || {}
//   if (memo[n]) {
//       return memo[n]
//   }
//   if (n <= 2) {
//       return memo[n] = 1;
//   }
//   return memo[n] = fibonacci2(n - 1, memo) + fibonacci2(n - 2, memo)
// }

// console.log(fibonacci2(10))