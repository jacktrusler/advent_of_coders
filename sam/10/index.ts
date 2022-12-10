import _ from "lodash";
import * as util from "../../../util/util";
import * as test from "../../../util/test";
import chalk from "chalk";
import { log, logSolution, trace } from "../../../util/log";
import { performance } from "perf_hooks";

const YEAR = 2022;
const DAY = 10;

// solution path: /Users/Sam/Documents/advent-of-code-runner/years/2022/10/index.ts
// data path    : /Users/Sam/Documents/advent-of-code-runner/years/2022/10/data.txt
// problem url  : https://adventofcode.com/2022/day/10

async function p2022day10_part1(input: string, ...params: any[]) {
	let signal = 0;
	let cycle = 1;
	let x = 1;

	function tick(){
		if (cycle % 40 === 20) { signal += cycle * x; }
		cycle++;
	}

	const lines = input.split("\n");
	for (const line of lines) {
		const [cmd, n] = line.split(' ');
		if (cmd === 'noop'){ tick(); }
		else { tick(); tick(); x += Number(n);}
	}

	return signal;
}

async function p2022day10_part2(input: string, ...params: any[]) {
	let cycle = 1;
	let x = 1;
	const width = 40;
	const height = 6;
	const buf: string[] = [];

	function plot(){
		const position = (cycle - 1) % width;
		if (Math.abs(position - x) <= 1) { buf.push("#"); }
		else { buf.push("."); }
	}

	function tick(){
		plot();
		cycle++;
	}

	const lines = input.split("\n");
	for (const line of lines) {
		const [cmd, n] = line.split(' ');
		if (cmd === 'noop'){ tick(); }
		else { tick(); tick(); x += Number(n);}
	}

	function printbuf(){
		for (let i = 0; i < height; i++){
			const line = buf.slice(i * width, i * width + width);
			console.log(line.join(''));
		}
	}
	
	printbuf();
	return '';
}

async function run() {
	const part1tests: TestCase[] = [];
	const part2tests: TestCase[] = [];

	// Run tests
	test.beginTests();
	await test.section(async () => {
		for (const testCase of part1tests) {
			test.logTestResult(testCase, String(await p2022day10_part1(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	await test.section(async () => {
		for (const testCase of part2tests) {
			test.logTestResult(testCase, String(await p2022day10_part2(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	test.endTests();

	// Get input and run program while measuring performance
	const input = await util.getInput(DAY, YEAR);

	const part1Before = performance.now();
	const part1Solution = String(await p2022day10_part1(input));
	const part1After = performance.now();

	const part2Before = performance.now()
	const part2Solution = String(await p2022day10_part2(input));
	const part2After = performance.now();

	logSolution(10, 2022, part1Solution, part2Solution);

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
