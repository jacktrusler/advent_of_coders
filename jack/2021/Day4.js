import { readFileSync } from 'fs'
//synchronous 
const textString = readFileSync("./Day4Input.txt")
  .toString()
  .replace(/\n$/, "")

const [rando, ...allBoards] = textString.split('\n');

const randomNumbers = rando.split(',');
//certainly a better way to do this, just gonna push values to an array
const pushaT = allBoards.filter((t) => (t));
const allBoardsArr = [];
for (let i = 0; i < pushaT.length; i++) {
  allBoardsArr.push(pushaT[i].split(' ').filter(String));
}
//take array values and smash into their own arrays for 25 numbers
const bingoCards = [];
function bingoCardMaker(arr) {
  for (let i = 0; i < arr.length; i = i + 5) {
    let card = []
    for (let j = i; j < i + 5; j++) {
      card.push(arr[j])
    }
    bingoCards.push(card);
  }
}
//all cards are now in bingoCards array, an array of arrays
bingoCardMaker(allBoardsArr);


//all winning combinations index bingoCards[i][0-4] --horizontal & bingoCards[i][0-4][0-4] --vertical
//find every win sequence?

function everyWinningCombo(bingoCards) {
  const solutions = [];
  //check bingo cards using current array values
  for (let i = 0; i < bingoCards.length; i++) {
    //horizontal solutions, make array for vertical lines
    for (let j = 0; j < 5; j++) {
      let verti = [];
      solutions.push(bingoCards[i][j])
      //vertical solutions
      for (let k = 0; k < 5; k++) {
        verti.push(bingoCards[i][k][j])
      }
      solutions.push(verti)
    }
  }
  return solutions;
}

function partOneAnswer(bingoCards, randomNumbers) {
  const solutionsArr = everyWinningCombo(bingoCards);
  const numberArr = [];
  //find a match with random numbers being pushed to the array vs the solutions array, recheck with every new number added
  for (let i = 0; i < randomNumbers.length; i++) {
    numberArr.push(randomNumbers[i])
    for (let j = 0; j < solutionsArr.length; j++) {
      let checker = (numberArr, solutionsArr) => solutionsArr[j].every(nums => numberArr.includes(nums));
      if (checker(numberArr, solutionsArr)) {
        //there are 10 solutions per card so if you divide by 10 you get the card index
        const finalCard = bingoCards[((j - 2) / 10)].flat();
        //return all the numbers from the card that aren't in the random number array and add them together.
        const nonMatchingValues = finalCard.filter(num => !numberArr.includes(num));
        const addedNonMatching = nonMatchingValues.map(numStr => parseInt(numStr, 10)).reduce((acc, val) => acc + val);
        //FINALLY multiply final random picked number with all the numbers added together
        return (addedNonMatching * numberArr[numberArr.length - 1])
      }
    }
  }
}

function partTwoAnswer(bingoCards, randomNumbers) {
  const solutionsArr = everyWinningCombo(bingoCards);
  let counter = 0;
  const numberArr = [];
  //find a match with random numbers being pushed to the array vs the solutions array, recheck with every new number added
  for (let i = 0; i < randomNumbers.length; i++) {
    numberArr.push(randomNumbers[i])
    for (let j = 0; j < solutionsArr.length; j++) {
      counter++;
      let checker = (numberArr, solutionsArr) => solutionsArr[j].every(nums => numberArr.includes(nums));
      if (checker(numberArr, solutionsArr)) {
        //base case - one card
        if (bingoCards.length === 1) {
          const finalCard = bingoCards.flat().flat();
          const nonMatchingValues = finalCard.filter(num => !numberArr.includes(num));
          const addedNonMatching = nonMatchingValues.map(numStr => parseInt(numStr, 10)).reduce((acc, val) => acc + val);
          return addedNonMatching * numberArr[numberArr.length - 1];
        }
        let solutionsIndex = (counter % solutionsArr.length);
        bingoCards.splice((Math.ceil(solutionsIndex / 10) - 1), 1)
        //recursion until you get down to one card
        return partTwoAnswer(bingoCards, randomNumbers);
      }
    }
  }
}

console.log('Part 1 Answer:', partOneAnswer(bingoCards, randomNumbers));
console.log('Part 2 Answer:', partTwoAnswer(bingoCards, randomNumbers));
