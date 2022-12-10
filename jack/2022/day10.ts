import { readFileSync } from "fs";
const answer = {
  part1: 0,
  part2: 0,
}

function setCharAt(str, index, chr): string {
  console.log(str, "|", index, "|", chr)
  if (index > str.length - 1) return str;
  return str.substring(0, index) + chr + str.substring(index + 1);
}

function day10(filePath: string) {
  const allOps = readFileSync(filePath).toString().replace(/\n$/, "").split('\n')

  ////Part 1
  //let x = 1;
  //let clockCycle = 0;
  //let loaded = false;
  //let clockStoppers = [20, 60, 100, 140, 180, 220]
  //let answer = 0;
  //for (const operation of allOps) {
  //  const [op, number] = operation.split(' ')
  //  if (op === 'noop') {
  //    clockCycle++
  //    if (clockStoppers.includes(clockCycle)) { answer = answer + (clockCycle * x) }
  //  }
  //  if (op === 'addx') {
  //    if (!loaded) {
  //      clockCycle++
  //      if (clockStoppers.includes(clockCycle)) { answer = answer + (clockCycle * x) }
  //      loaded = true;
  //    }
  //    if (loaded) {
  //      clockCycle++
  //      if (clockStoppers.includes(clockCycle)) { answer = answer + (clockCycle * x) }
  //      x += Number(number)
  //      loaded = false;
  //    }
  //  }
  //}

  //Part 2
  const SCREEN_HEIGHT = 6;
  const SCREEN_WIDTH = 40;
  const crtScreen = [];
  for (let i = 0; i < SCREEN_HEIGHT; i++) {
    let row = []
    for (let j = 0; j < SCREEN_WIDTH; j++) {
      row.push(".")
    }
    crtScreen.push(row.join(''))
  }

  let x = 1;
  let spriteRange = [x - 1, x, x + 1]
  let clockCyclep2 = 1;
  let r = 0;
  for (let i = 0; i < allOps.length; i++) {
    const [op, number] = allOps[i].split(' ')
    if (op === 'noop') {
      if (spriteRange.includes(clockCyclep2 - 1)) {
        crtScreen[r] = setCharAt(crtScreen[r], clockCyclep2 - 1, '#')
      }
      clockCyclep2++
      if (clockCyclep2 === SCREEN_WIDTH + 1) { r++; clockCyclep2 = 1; }
    }

    if (op === 'addx') {
      if (spriteRange.includes(clockCyclep2 - 1)) {
        crtScreen[r] = setCharAt(crtScreen[r], clockCyclep2 - 1, '#')
      }
      clockCyclep2++
      if (clockCyclep2 === SCREEN_WIDTH + 1) { r++; clockCyclep2 = 1; }

      if (spriteRange.includes(clockCyclep2 - 1)) {
        crtScreen[r] = setCharAt(crtScreen[r], clockCyclep2 - 1, '#')
      }
      clockCyclep2++
      x = x + Number(number)
      spriteRange = [x - 1, x, x + 1]
      if (clockCyclep2 === SCREEN_WIDTH + 1) { r++; clockCyclep2 = 1; }
    }
  }
  console.log(crtScreen)
}


day10('./day10.txt')
