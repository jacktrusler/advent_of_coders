import _ from "lodash";
import * as util from "../../../util/util";
import * as test from "../../../util/test";
import chalk from "chalk";
import { log, logSolution, trace } from "../../../util/log";
import { performance } from "perf_hooks";

const YEAR = 2022;
const DAY = 5;

// solution path: /Users/Sam/Documents/advent-of-code-runner/years/2022/05/index.ts
// data path    : /Users/Sam/Documents/advent-of-code-runner/years/2022/05/data.txt
// problem url  : https://adventofcode.com/2022/day/5

function getStacks(input: string): string[][] {
	const lines = input.split('\n');
	const stacks = new Array(9).fill(0).map<string[]>(_ => []);
	for (let i = lines.length-2; i >= 0; i--){
		for (let j = 0; j < 9; j++){
			const c = lines[i][j*4+1];
			if (c !== " ") { stacks[j].push(c); }
		}
	}
	return stacks;
}

async function p2022day5_part1(input: string, ...params: any[]) {
	const [crates, moves] = input.split("\n\n");
	const stacks = getStacks(crates);
	for (const move of moves.split("\n")) {
		const [,ct,,from,,to] = move.split(' ').map(Number);
		for (let i = 0; i < ct; i++) {
			const c = stacks[from-1].pop();
			stacks[to-1].push(c as string);
		}
	}
	return stacks.map(stk => stk[stk.length-1]).join('');
}

async function p2022day5_part2(input: string, ...params: any[]) {
	const [crates, moves] = input.split("\n\n");
	const stacks = getStacks(crates);
	for (const move of moves.split("\n")) {
		const [,ct,,from,,to] = move.split(' ').map(Number);
		const tmp = [];
		for (let i = 0; i < ct; i++) {
			tmp.push(stacks[from-1].pop());
		}
		for (let i = 0; i < ct; i++) {
			stacks[to-1].push(tmp.pop() as string);
		}
	}
	return stacks.map(stk => stk[stk.length-1]).join('');
}

async function run() {
	const part1tests: TestCase[] = [];
	const part2tests: TestCase[] = [];

	// Run tests
	test.beginTests();
	await test.section(async () => {
		for (const testCase of part1tests) {
			test.logTestResult(testCase, String(await p2022day5_part1(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	await test.section(async () => {
		for (const testCase of part2tests) {
			test.logTestResult(testCase, String(await p2022day5_part2(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	test.endTests();

	// Get input and run program while measuring performance
	const input = await util.getInput(DAY, YEAR);

	const part1Before = performance.now();
	const part1Solution = String(await p2022day5_part1(input));
	const part1After = performance.now();

	const part2Before = performance.now()
	const part2Solution = String(await p2022day5_part2(input));
	const part2After = performance.now();

	logSolution(5, 2022, part1Solution, part2Solution);

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
