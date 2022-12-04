import _ from "lodash";
import * as util from "../../../util/util";
import * as test from "../../../util/test";
import chalk from "chalk";
import { log, logSolution, trace } from "../../../util/log";
import { performance } from "perf_hooks";

const YEAR = 2022;
const DAY = 4;

// solution path: /Users/Sam/Documents/advent-of-code-runner/years/2022/04/index.ts
// data path    : /Users/Sam/Documents/advent-of-code-runner/years/2022/04/data.txt
// problem url  : https://adventofcode.com/2022/day/4

function contains(a: number, b: number, c: number, d: number): boolean {
	return a <= c && b >= d;
}

async function p2022day4_part1(input: string, ...params: any[]) {
	let result = 0;
	const lines = input.split("\n");
	for (const line of lines) {
		const [a,b] = line.split(",");
		const [amin, amax] = a.split('-').map(Number);
		const [bmin, bmax] = b.split('-').map(Number);
		if (contains(amin, amax, bmin, bmax) || contains(bmin, bmax, amin, amax)) result++;
	}
	return result;
}

function within(a: number, b: number, c: number): boolean {
	return (a >= b && a <= c);
 }

async function p2022day4_part2(input: string, ...params: any[]) {
	let result = 0;
	const lines = input.split("\n");
	for (const line of lines) {
		const [a,b] = line.split(",");
		const [amin, amax] = a.split('-').map(Number);
		const [bmin, bmax] = b.split('-').map(Number);
		if (within(amin, bmin, bmax) || within(amax, bmin, bmax) || within(bmin, amin, amax))  result++;
	}
	return result;
}

async function run() {
	const part1tests: TestCase[] = [];
	const part2tests: TestCase[] = [{input: `2-4,6-8\n2-3,4-5\n5-7,7-9\n2-8,3-7\n6-6,4-6\n2-6,4-8`, expected: "4"}];

	// Run tests
	test.beginTests();
	await test.section(async () => {
		for (const testCase of part1tests) {
			test.logTestResult(testCase, String(await p2022day4_part1(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	await test.section(async () => {
		for (const testCase of part2tests) {
			test.logTestResult(testCase, String(await p2022day4_part2(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	test.endTests();

	// Get input and run program while measuring performance
	const input = await util.getInput(DAY, YEAR);

	const part1Before = performance.now();
	const part1Solution = String(await p2022day4_part1(input));
	const part1After = performance.now();

	const part2Before = performance.now()
	const part2Solution = String(await p2022day4_part2(input));
	const part2After = performance.now();

	logSolution(4, 2022, part1Solution, part2Solution);

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
