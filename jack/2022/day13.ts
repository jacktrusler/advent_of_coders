import { readFileSync } from "fs";

const answer = { part1: 0, part2: 0, }

type Packet = number | Packet[]
type PacketOrder = 'ordered' | 'unordered' | 'equal'

function day13(filePath: string) {
  const input = readFileSync(filePath).toString().replace(/\n$/, "").split('\n\n')
  const inputPairs: string[] = input.map((input) => input.split('\n')).flat()
  const packets: Packet[] = inputPairs.map((str) => JSON.parse(str))

  function tester(lhs: Packet, rhs: Packet): PacketOrder {
    if (typeof lhs === 'number' && typeof rhs === 'number') {
      if (rhs < lhs) return 'unordered'
      if (lhs < rhs) return 'ordered'
    }
    if (Array.isArray(lhs) && Array.isArray(rhs)) {
      for (let i = 0; i < Math.max(lhs.length, rhs.length); i++) {
        if (lhs.length === i) return 'ordered'
        if (rhs.length === i) return 'unordered'
        const answer = tester(lhs[i], rhs[i])
        if (answer !== 'equal') {
          return answer
        }
      }
    }
    if (Array.isArray(lhs) && !Array.isArray(rhs)) {
      return tester(lhs, [rhs])
    }
    if (!Array.isArray(lhs) && Array.isArray(rhs)) {
      return tester([lhs], rhs)
    }
    return 'equal'
  }

  // Part 1
  let finalIndex = 0;
  for (let i = 0; i < packets.length; i = i + 2) {
    let lhs = packets[i];
    let rhs = packets[i + 1];
    if (tester(lhs, rhs) !== 'unordered') {
      finalIndex = finalIndex + (i / 2 + 1)
    }
  }
  answer.part1 = finalIndex;

  // Part 2
  const insertedPackets = [[[2]], [[6]]]
  packets.push(insertedPackets[0])
  packets.push(insertedPackets[1])
  packets.sort((lhs, rhs) => {
    const order = tester(lhs, rhs)
    if (order === 'unordered') {
      return 1;
    }
    return -1;
  })

  const findInserted = (packets.indexOf(insertedPackets[0]) + 1) * (packets.indexOf(insertedPackets[1]) + 1)
  answer.part2 = findInserted

  console.log(answer);
  return answer;
}

export { day13 }
