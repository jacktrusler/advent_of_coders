import { readFileSync } from 'fs'

const binArray = readFileSync("./Day3Input.txt")
  .toString()
  .replace(/\n$/, "")
  .split("\n")

function binRate(arr) {
  //ones ++ for 1s and zeros ++ for 0s
  //take the first number, add 1s add 0s... whatever's bigger push to array
  const gammaRate = [];
  const epsilonRate = [];
  for (let strIter = 0; strIter < arr[0].length; strIter++) {
    let ones = 0;
    let zeros = 0;
    for (let i = 0; i < arr.length; i++) {
      if (arr[i][strIter] === '1') {
        ones++
      } else { zeros++ }
    }
    if (ones > zeros) {
      gammaRate.push(1);
      epsilonRate.push(0);
    }
    else {
      gammaRate.push(0)
      epsilonRate.push(1)
    };
  }
  console.log(`Gamma Rate --- binary: ${gammaRate.join('')} decimal: ${parseInt(gammaRate.join(''), 2)}`)
  console.log(`Epsilon Rate --- binary: ${epsilonRate.join('')} decimal: ${parseInt(epsilonRate.join(''), 2)}`)
}


function oxyCity(arr) {
  let oxyRate = arr;

  for (let strIter = 0; strIter < arr[0].length; strIter++) {
    let ones = 0;
    let zeros = 0;

    for (let i = 0; i < oxyRate.length; i++) {
      if (oxyRate[i][strIter] === '1') {
        ones++
      } else { zeros++ }
    }
    //if there are MORE ones's than zeros's remove the zeros's and visa versa
    if (ones >= zeros) {
      oxyRate = oxyRate.filter(bin => bin[strIter] === '1');
    } else {
      oxyRate = oxyRate.filter(bin => bin[strIter] === '0');
    }
  }
  console.log(`Oxygen Rate --- binary: ${oxyRate.join('')} decimal: ${parseInt(oxyRate.join(''), 2)}`)
}

function CO2City(arr) {
  let CO2Rate = arr;

  for (let strIter = 0; strIter < arr[0].length; strIter++) {
    let zeros = 0;
    let ones = 0;

    for (let i = 0; i < CO2Rate.length; i++) {
      if (CO2Rate.length === 1) {
        console.log(`CO2 Rate --- binary: ${CO2Rate.join('')} decimal: ${parseInt(CO2Rate.join(''), 2)}`)
      }
      else if (CO2Rate[i][strIter] === '1') {
        zeros++
      } else {
        ones++
      }
    }
    //if there are LESS ones' than zeros' remove the zeros' and visa versa
    if (ones <= zeros) {
      CO2Rate = CO2Rate.filter(bin => bin[strIter] === '0');
    } else {
      CO2Rate = CO2Rate.filter(bin => bin[strIter] === '1');
    }
  }
}

binRate(binArray);
oxyCity(binArray);
CO2City(binArray);

