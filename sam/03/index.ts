import _, { values } from "lodash";
import * as util from "../../../util/util";
import * as test from "../../../util/test";
import chalk from "chalk";
import { log, logSolution, trace } from "../../../util/log";
import { performance } from "perf_hooks";
import { getPriority } from "os";

const YEAR = 2022;
const DAY = 3;

// solution path: /Users/Sam/Documents/advent-of-code-runner/years/2022/03/index.ts
// data path    : /Users/Sam/Documents/advent-of-code-runner/years/2022/03/data.txt
// problem url  : https://adventofcode.com/2022/day/3

function priority(c: string): number {
	return c.toUpperCase() === c ? c.charCodeAt(0) - 38 : c.charCodeAt(0) - 96;
}

async function p2022day3_part1(input: string, ...params: any[]) {
	let result = 0;
	const lines = input.split("\n");
	for (const line of lines) {
		let chars = new Set();
		for (let i = 0; i < line.length; i++){
			const c = line[i];
			if (i < line.length / 2) { chars.add(c); }
			else if (chars.has(c)) { result += priority(c); break; }
		}
	}
	return result;
}

async function p2022day3_part2(input: string, ...params: any[]) {
	let result = 0;
	const lines = input.split("\n");
	for (let i = 0; i < lines.length; i += 3) {
		const a = new Set(lines[i].split(''));
		const b = new Set(lines[i+1].split(''));
		let c = lines[i+2];
		for (let j = 0; j < c.length; j++){
			if (a.has(c[j]) && b.has(c[j])) {result += priority(c[j]); break}
		}
	}
	return result;
}

async function run() {
	const part1tests: TestCase[] = [{input: "abcdea", expected: "1"}, {input: "AbdAef", expected: "27"}];
	const part2tests: TestCase[] = [];

	// Run tests
	test.beginTests();
	await test.section(async () => {
		for (const testCase of part1tests) {
			test.logTestResult(testCase, String(await p2022day3_part1(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	await test.section(async () => {
		for (const testCase of part2tests) {
			test.logTestResult(testCase, String(await p2022day3_part2(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	test.endTests();

	// Get input and run program while measuring performance
	const input = await util.getInput(DAY, YEAR);

	const part1Before = performance.now();
	const part1Solution = String(await p2022day3_part1(input));
	const part1After = performance.now();

	const part2Before = performance.now()
	const part2Solution = String(await p2022day3_part2(input));
	const part2After = performance.now();

	logSolution(3, 2022, part1Solution, part2Solution);

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
