
const fs =require('fs')


const lines = fs.readFileSync('./input.txt', {encoding: 'utf8'}).split('\n')
let lineSum= 0


for (const line of lines){
    let foundNumbas =[]
    console.log(line)
    for(const thingy of line){
        const maybeNumber = Number(thingy)
    
        if (Number.isNaN(maybeNumber)) {
            console.log('NaN')
        } else{
            foundNumbas.push(maybeNumber)

        }
    }
    console.log(foundNumbas)
    let lineVal=foundNumbas[0]*10 + foundNumbas[foundNumbas.length-1]
    console.log(lineVal)
   lineSum= lineVal + lineSum


} 
console.log(lineSum)



