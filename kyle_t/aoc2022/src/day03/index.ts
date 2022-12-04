import run from "aocrunner";
import assert from "assert";

// Let's Get it! 🌲🌄🌻

const getSacky = (sacks: string) => {
  const sackBin = sacks.split("\n");
  const sacagawea = sackBin.map((sack) => {
    return [
      sack.slice(0, sack.length / 2),
      sack.slice(sack.length / 2, sack.length),
    ];
  });
  return sacagawea;
};

const getElfySacky = (sacks: string) => {
  const sackySplit = sacks.split("\n");
  const sacagawea = sackySplit.reduce((sackyTrip, sack, i) => {
    if (i % 3 == 0) sackyTrip.push([sack.split("")]);
    else sackyTrip[sackyTrip.length - 1].push(sack.split(""));
    return sackyTrip;
  }, []);
  return sacagawea;
};

const getKeyCodeValuePlease = (key: string): number => {
  return key.charCodeAt(0) - (key.toLowerCase() == key ? 96 : 38);
};
const part1 = (sackWhispers: string) => {
  const sacagawea = getSacky(sackWhispers);
  let totalSackage = 0;
  for (let i = 0; i < sacagawea.length; i++) {
    const leftSet = new Set(
      Array.from(new Set(sacagawea[i][0].split(""))).sort(),
    );
    const rightSet = new Set(
      Array.from(new Set(sacagawea[i][1].split(""))).sort(),
    );
    for (let key of leftSet) {
      if (rightSet.has(key)) {
        totalSackage += getKeyCodeValuePlease(key);
      }
    }
  }
  return totalSackage;
};

const part2 = (sackWhispers: string) => {
  const sackyTrips = getElfySacky(sackWhispers);
  return sackyTrips.reduce((sackyTotal, [sackyOne, sackyTwo, sackyThree]) => {
    return (
      sackyTotal +
      getKeyCodeValuePlease(
        sackyOne.find(
          (gift) => sackyTwo.includes(gift) && sackyThree.includes(gift),
        ),
      )
    );
  }, 0);
};

run({
  part1: {
    tests: [
      {
        input: `vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw`,
        expected: 157,
      },
    ],
    solution: part1,
  },
  part2: {
    tests: [
      {
        input: `vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw`,
        expected: 70,
      },
    ],
    solution: part2,
  },
  trimTestInputs: true,
  onlyTests: false,
});
