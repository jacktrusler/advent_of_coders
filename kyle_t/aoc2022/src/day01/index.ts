import run from "aocrunner";

const parseInput = (rawInput: string) => rawInput;

const part1 = (rawInput: string) => {
  const input = parseInput(rawInput);

  return Math.max(
    ...input.split("\n").reduce(
      (prev: number[], current: string) => {
        if (current === "") {
          prev.push(0);
        } else {
          prev[prev.length - 1] += parseInt(current);
        }
        return prev;
      },
      [0],
    ),
  );
};

const part2 = (rawInput: string) => {
  const input = parseInput(rawInput);
  return input
    .split("\n")
    .reduce(
      (prev: number[], current: string) => {
        if (current === "") {
          prev.push(0);
        } else {
          prev[prev.length - 1] += parseInt(current);
        }
        return prev;
      },
      [0],
    )
    .sort((a: number, b: number) => b - a)
    .slice(0, 3)
    .reduce((curr, prev) => prev + curr, 0);
};

run({
  part1: {
    tests: [
      {
        input: "10\n20\n\n20\n20",
        expected: 40,
      },
    ],
    solution: part1,
  },
  part2: {
    tests: [
      // {
      //   input: ``,
      //   expected: "",
      // },
    ],
    solution: part2,
  },
  trimTestInputs: true,
  onlyTests: false,
});
