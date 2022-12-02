import _, { result } from "lodash";
import * as util from "../../../util/util";
import * as test from "../../../util/test";
import chalk from "chalk";
import { log, logSolution, trace } from "../../../util/log";
import { performance } from "perf_hooks";

const YEAR = 2022;
const DAY = 2;

// solution path: /Users/Sam/Documents/advent-of-code-runner/years/2022/02/index.ts
// data path    : /Users/Sam/Documents/advent-of-code-runner/years/2022/02/data.txt
// problem url  : https://adventofcode.com/2022/day/2

// A for Rock, B for Paper, and C for Scissors. 
// X for Rock, Y for Paper, and Z for Scissors.
// 1 for Rock, 2 for Paper, and 3 for Scissors
// 0 for loss, 3 for draw, 6 for win

const moves = {
	"A X": 4,
	"A Y": 8,
	"A Z": 3,
	"B X": 1,
	"B Y": 5,
	"B Z": 9,
	"C X": 7,
	"C Y": 2,
	"C Z": 6,
} as const;

async function p2022day2_part1(input: string, ...params: any[]) {
	let total = 0;
	const lines = input.split("\n");
	for (const line of lines) {
		total += moves[line as keyof typeof moves];
	}
	return total;
}

//X means you need to lose, 
//Y means you need to end the round in a draw, 
//and Z means you need to win
const moves2 = {
	"A X": 3,
	"A Y": 4,
	"A Z": 8,
	"B X": 1,
	"B Y": 5,
	"B Z": 9,
	"C X": 2,
	"C Y": 6,
	"C Z": 7,
} as const;

async function p2022day2_part2(input: string, ...params: any[]) {
	let total = 0;
	const lines = input.split("\n");
	for (const line of lines) {
		total += moves2[line as keyof typeof moves2];
	}
	return total;
}

async function run() {
	const part1tests: TestCase[] = [];
	const part2tests: TestCase[] = [];

	// Run tests
	test.beginTests();
	await test.section(async () => {
		for (const testCase of part1tests) {
			test.logTestResult(testCase, String(await p2022day2_part1(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	await test.section(async () => {
		for (const testCase of part2tests) {
			test.logTestResult(testCase, String(await p2022day2_part2(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	test.endTests();

	// Get input and run program while measuring performance
	const input = await util.getInput(DAY, YEAR);

	const part1Before = performance.now();
	const part1Solution = String(await p2022day2_part1(input));
	const part1After = performance.now();

	const part2Before = performance.now()
	const part2Solution = String(await p2022day2_part2(input));
	const part2After = performance.now();

	logSolution(2, 2022, part1Solution, part2Solution);

	log(chalk.gray("--- Performance ---"));
	log(chalk.gray(`Part 1: ${util.formatTime(part1After - part1Before)}`));
	log(chalk.gray(`Part 2: ${util.formatTime(part2After - part2Before)}`));
	log();
}

run()
	.then(() => {
		process.exit();
	})
	.catch(error => {
		throw error;
	});
