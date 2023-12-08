const fs = require('fs');

const file = fs.readFileSync('input.txt', 'utf-8')
const lines = file.split("\n");

let lineSum = 0;
//All my Top -> Bottom Work
for (const line of lines){
    let foundNumbers = [];
    //All my Left -> Right Work
    for (let index = 0; index < line.length; index++ ){
        const char = line[index]
        let testNumber = Number(char);
        if (! Number.isNaN(testNumber)){
            foundNumbers.push(testNumber);
        } else {
            //I am going to look at the next 4 characters to see if a word is spelled
            const lookAhead = line.substring(index, index+5)
            if (lookAhead.indexOf("one") == 0) {
                foundNumbers.push(1)
            } else if (lookAhead.indexOf("two") == 0 ) {
                foundNumbers.push(2)
            } else if (lookAhead.indexOf("three") == 0){
                foundNumbers.push(3)
            } else if (lookAhead.indexOf("four") == 0){
                foundNumbers.push(4)
            } else if (lookAhead.indexOf("five") == 0){
                foundNumbers.push(5)
            } else if (lookAhead.indexOf("six") == 0){
                foundNumbers.push(6)
            } else if (lookAhead.indexOf("seven") == 0){
                foundNumbers.push(7)
            } else if (lookAhead.indexOf("eight") == 0){
                foundNumbers.push(8)
            } else if (lookAhead.indexOf("nine") == 0){
                foundNumbers.push(9)
            }
        }
    }
    //Work that needs all the L->R work done Before Going Down to Next Line
    lineSum += foundNumbers[0] * 10 + foundNumbers[foundNumbers.length-1]
}
//Work that needs all the T -> B Work Done
console.log(lineSum)