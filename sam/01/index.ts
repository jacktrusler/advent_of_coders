import _ from "lodash";
import * as util from "../../../util/util";
import * as test from "../../../util/test";
import chalk from "chalk";
import { log, logSolution, trace } from "../../../util/log";
import { performance } from "perf_hooks";

const YEAR = 2022;
const DAY = 1;

// solution path: /Users/Sam/Documents/advent-of-code-runner/years/2022/01/index.ts
// data path    : /Users/Sam/Documents/advent-of-code-runner/years/2022/01/data.txt
// problem url  : https://adventofcode.com/2022/day/2

async function p2022day1_part1(input: string, ...params: any[]) {
	let max = -Infinity;
	const groups = input.split("\n\n");
	for (const group of groups) {
		let elf = 0;
		const lines = group.split("\n");
		for (const line of lines) {
			elf += Number(line);
		}
		max = Math.max(elf, max);
	}
	return max;
}

async function p2022day1_part2(input: string, ...params: any[]) {
	let elves = [];
	const groups = input.split("\n\n");
	for (const group of groups) {
		let elf = 0;
		const lines = group.split("\n");
		for (const line of lines) {
			elf += Number(line);
		}
		elves.push(elf);
	}
	return elves.sort((a,b) => b - a).slice(0,3).reduce((a,c) => a + c);
}

async function run() {
	const part1tests: TestCase[] = [{input: "100\n\n200\n", expected: "200"}];
	const part2tests: TestCase[] = [];

	// Run tests
	test.beginTests();
	await test.section(async () => {
		for (const testCase of part1tests) {
			test.logTestResult(testCase, String(await p2022day1_part1(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	await test.section(async () => {
		for (const testCase of part2tests) {
			test.logTestResult(testCase, String(await p2022day1_part2(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	test.endTests();

	// Get input and run program while measuring performance
	const input = await util.getInput(DAY, YEAR);

	const part1Before = performance.now();
	const part1Solution = String(await p2022day1_part1(input));
	const part1After = performance.now();

	const part2Before = performance.now()
	const part2Solution = String(await p2022day1_part2(input));
	const part2After = performance.now();

	logSolution(1, 2022, part1Solution, part2Solution);

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
