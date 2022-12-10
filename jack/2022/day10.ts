import { readFileSync } from "fs";
const answer = {
  part1: 0,
  part2: 0,
}

function setCharAt(str: string, index: number, chr: string): string {
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

  let spritePos = 1;
  let spriteRange = [spritePos - 1, spritePos, spritePos + 1]
  let clockCyclep2 = 0;
  let loadedp2 = false;
  for (const operation of allOps) {
    const [op, number] = operation.split(' ')
    for (let i = 0; i < SCREEN_HEIGHT; i++) {
      clockCyclep2 = 0;
      while (clockCyclep2 < SCREEN_WIDTH) {
        if (op === 'noop') {
          if (spriteRange.includes(clockCyclep2)) {
            crtScreen[i] = setCharAt(crtScreen[i], clockCyclep2, '#')
          }
          clockCyclep2++
        }
        if (op === 'addx' && clockCyclep2 < SCREEN_WIDTH) {
          if (!loadedp2) {
            if (spriteRange.includes(clockCyclep2)) {
              crtScreen[i] = setCharAt(crtScreen[i], clockCyclep2, '#')
            }
            clockCyclep2++
            loadedp2 = true;
          }
          if (loadedp2 && clockCyclep2 < SCREEN_WIDTH) {
            if (spriteRange.includes(clockCyclep2)) {
              crtScreen[i] = setCharAt(crtScreen[i], clockCyclep2, '#')
            }
            clockCyclep2++
            spritePos += Number(number)
            loadedp2 = false;
          }
        }
      }
    }
  }
  console.log(crtScreen)
}

day10('./day10.txt')
