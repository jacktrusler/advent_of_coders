import { readFileSync } from 'fs'

const directions = readFileSync("./Day2Input.txt")
  .toString()
  .replace(/\n$/, "")
  .split("\n")

function MOVEerino(inputs) {
  let x = 0;
  let y = 0;
  inputs.forEach((input) => {
    const [command, numba] = input.split(' ')
    const num = Number(numba);
    switch (command) {
      case 'forward': {
        x += num;
        break;
      }
      case 'up': {
        y -= num;
        break;
      }
      case 'down': {
        y += num;
        break;
      }
    }
  })
  console.log(`Moved: ${x} units Horizontally  ---  `, `Moved: ${y} units Down`)
  console.log(`Multiplied for Answer: ${x * y} units²`)
}

function AIMerino(inputs) {
  let x = 0;
  let y = 0;
  let aim = 0;
  inputs.forEach((input) => {
    const [command, numba] = input.split(' ')
    const num = Number(numba);
    switch (command) {
      case 'forward': {
        x += num
        y += (aim * num)
        break;
      }
      case 'up': {
        aim -= num;
        break;
      }
      case 'down': {
        aim += num;
        break;
      }
    }
  })
  console.log(`Moved: ${x} units Horizontally  ---  `, `Moved: ${y} units Down`)
  console.log(`Multiplied for Answer: ${x * y} units²`)
}

MOVEerino(directions);
AIMerino(directions);
