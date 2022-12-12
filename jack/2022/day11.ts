import { readFileSync } from "fs";

const answer = { part1: 0, part2: 0 }

interface Monkey {
  monkey: number,
  items: number[],
  stress: string | 'old' | '+' | '*'[],
  test: number,
  successMonkey: number,
  failMonkey: number,
  inspections: number,
}

function monkeyMaker(monkey, items, stress, test, s, f): Monkey {
  return {
    monkey: monkey,
    items: items,
    stress: stress,
    test: test,
    successMonkey: s,
    failMonkey: f,
    inspections: 0,
  }
}

function monkifier(monks: string[][]) {
  const monkeys = []
  for (let i = 0; i < monks.length; i = i + 6) {
    monkeys.push(monkeyMaker(
      parseInt(monks[i][0]),
      [...monks[i + 1].map((item) => parseInt(item))],
      monks[i + 2],
      parseInt(monks[i + 3][0]),
      parseInt(monks[i + 4][1]),
      parseInt(monks[i + 5][1])
    ))
  }
  return monkeys;
}

function monkeyBusiness(rounds: number, part: 1 | 2, m): number {
  // Put monkeys in trees
  const monkeys: Monkey[] = monkifier(m)

  const modularity = monkeys.reduce((acc, monkey) => monkey.test * acc, 1)
  for (let i = 0; i < rounds; i++) {
    monkeys.forEach((monkey) => {
      while (monkey.items.length > 0) {
        monkey.inspections++
        let worryLevel = monkey.items.shift()
        if (monkey.stress[1] === '*') {
          if (monkey.stress[2] === 'old') {
            worryLevel = worryLevel * worryLevel
          } else {
            worryLevel = worryLevel * parseInt(monkey.stress[2])
          }
        } else {
          worryLevel = worryLevel + parseInt(monkey.stress[2])
        }

        if (part === 1) { worryLevel = Math.floor((worryLevel) / 3); }
        if (part === 2) { worryLevel = worryLevel % modularity; }

        worryLevel % monkey.test === 0
          ? monkeys[monkey.successMonkey].items.push(worryLevel)
          : monkeys[monkey.failMonkey].items.push(worryLevel)
      }
    })
  }
  monkeys.sort((monk1, monk2) => monk2.inspections - monk1.inspections)
  return (monkeys[0].inspections * monkeys[1].inspections)
}

function day11(filePath: string) {
  const mon_k = readFileSync(filePath).toString().replace(/\n$/, "").split('\n\n')
  const reggy = /[0-9+*]+|(old)|(true)|(false)/g
  const m = mon_k
    .map((row) => row.split('\n'))
    .map((inst) => inst.map((str) => str.match(reggy))).flat()
  answer.part1 = monkeyBusiness(20, 1, m)
  answer.part2 = monkeyBusiness(10000, 2, m)

  console.log(answer)
  return answer;
}

export { day11 }
