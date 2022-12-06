import { readFileSync } from "fs";

const answer = {
  part1: 0,
  part2: 0,
}

function day6(filePath: string) {
  //signal input
  const si = readFileSync(filePath).toString()
  //start-of-packet-marker
  let sopm;
  let packetLen = 4
  const len = si.length
  //part1
  for (let i = 0; i < len; i++) {
    const packet = new Set(si.slice(i, i + packetLen))
    if (packet.size === 4) {
      sopm = i + packetLen;
      break;
    }
  }
  answer.part1 = sopm as number;
  //part2
  packetLen = 14
  for (let i = 0; i < len; i++) {
    const packet = new Set(si.slice(i, i + packetLen))
    if (packet.size === 14) {
      sopm = i + packetLen;
      break;
    }
  }
  answer.part2 = sopm as number;
  console.log(answer)
  return answer
}

export { day6 }
