import { readFileSync } from "fs";

const answer = {
  part1: 0,
  part2: 0,
}

function findFirstMarker(dataStream: string, packetSize: number): number {
  const len = dataStream.length
  for (let i = 0; i < len - packetSize; i++) {
    const s = new Set(dataStream.slice(i, i + packetSize));
    if (s.size === packetSize) {
      return i + packetSize;
    }
  }
  console.log("No unique marker found!")
  return -1;
}

function day6(filePath: string) {
  //signal input
  const si = readFileSync(filePath).toString()
  answer.part1 = findFirstMarker(si, 4)
  answer.part2 = findFirstMarker(si, 14)
  console.log(answer)
  return answer
}

export { day6 }
