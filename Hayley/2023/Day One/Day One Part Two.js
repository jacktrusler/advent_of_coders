const fs =require('fs')

const re = /(?=(\d|one|two|three|four|five|six|seven|eight|nine))/g

const lines = fs.readFileSync('./input.txt', {encoding: 'utf8'}).split('\n')
let lineSum= 0


for (const line of lines){ 
    let foundNumbas =[]
    const matches = Array.from(line.matchAll(re));
    console.log(`for ${line}: found the following matches: ${matches}`)
    
    if (!matches) {
        continue
    }
    for (const match of matches ) {
        const spelledNumba = match[1]
        let digitNumba= Number(spelledNumba)
        if (Number.isNaN(digitNumba)) {
            switch (spelledNumba){
                case "one" :
                    digitNumba=1 
                    break;
                case "two" :
                    digitNumba=2
                    break
                case "three" :
                    digitNumba=3
                    break
                case "four" :
                    digitNumba=4
                    break
                case "five" :
                    digitNumba=5
                    break
                case "six" :
                    digitNumba=6
                    break
                case "seven" :
                    digitNumba=7
                    break
                case "eight" :
                    digitNumba=8
                    break
                case "nine" :
                    digitNumba=9
                    break
            }
        }
        foundNumbas.push(digitNumba)
    }

    console.log(foundNumbas)
    let lineVal=foundNumbas[0]*10 + foundNumbas[foundNumbas.length-1]
    console.log(`about to add ${lineVal}`)
    if (Number.isNaN(lineVal) == false) {
        // real numbers only!!!!!
        lineSum= lineVal + lineSum
    }


} 
console.log(`total sum = ${lineSum}`)
