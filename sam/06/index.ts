import _ from "lodash";
import * as util from "../../../util/util";
import * as test from "../../../util/test";
import chalk from "chalk";
import { log, logSolution, trace } from "../../../util/log";
import { performance } from "perf_hooks";

const YEAR = 2022;
const DAY = 6;

// solution path: /Users/Sam/Documents/advent-of-code-runner/years/2022/06/index.ts
// data path    : /Users/Sam/Documents/advent-of-code-runner/years/2022/06/data.txt
// problem url  : https://adventofcode.com/2022/day/6

async function p2022day6_part1(input: string, ...params: any[]) {
	for (let i = 0; i < input.length - 4; i++){
		const window = input.slice(i, i+4);
		if (
			window.indexOf(window[1]) === 1 &&
			window.indexOf(window[2]) === 2 &&
			window.indexOf(window[3]) === 3
		) { 
			return i+4;
		}		
	}
	return 0;
}

async function p2022day6_part2(input: string, ...params: any[]) {
	for (let i = 0; i < input.length - 14; i++){
		const s = new Set(input.slice(i, i+14).split(''));
		if (s.size === 14) return i + 14;
	}
	return 0;
}

async function run() {
	const part1tests: TestCase[] = [];
	const part2tests: TestCase[] = [{input: 'mjqjpqmgbljsphdztnvjfqwrcgsmlb', expected: '19'}];

	// Run tests
	test.beginTests();
	await test.section(async () => {
		for (const testCase of part1tests) {
			test.logTestResult(testCase, String(await p2022day6_part1(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	await test.section(async () => {
		for (const testCase of part2tests) {
			test.logTestResult(testCase, String(await p2022day6_part2(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	test.endTests();

	// Get input and run program while measuring performance
	const input = await util.getInput(DAY, YEAR);

	const part1Before = performance.now();
	const part1Solution = String(await p2022day6_part1(input));
	const part1After = performance.now();

	const part2Before = performance.now()
	const part2Solution = String(await p2022day6_part2(input));
	const part2After = performance.now();

	logSolution(6, 2022, part1Solution, part2Solution);

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
