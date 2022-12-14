import _ from "lodash";
import * as util from "../../../util/util";
import * as test from "../../../util/test";
import chalk from "chalk";
import { log, logSolution, trace } from "../../../util/log";
import { performance } from "perf_hooks";

const YEAR = 2022;
const DAY = 13;

// solution path: /Users/Sam/Documents/advent-of-code-runner/years/2022/13/index.ts
// data path    : /Users/Sam/Documents/advent-of-code-runner/years/2022/13/data.txt
// problem url  : https://adventofcode.com/2022/day/13

type Packet = (number | Packet[]);
type Result = true | false | 'neutral'

function in_order(a: Packet, b: Packet): Result {
	if (typeof a === 'number' && typeof b === 'number') {
		if (a < b) return true;
		if (a > b) return false;
	}

	if (Array.isArray(a) && Array.isArray(b)) {
		for (let i = 0; i < Math.max(a.length, b.length); i++) {
			if (i === a.length) return true;
			if (i === b.length) return false; 
			const result = in_order(a[i], b[i]);
			if (result !== 'neutral') return result;
		}
	}

	if (Array.isArray(a) && typeof b === 'number') {
		return in_order(a, [b]);
	}

	if (Array.isArray(b) && typeof a === 'number') {
		return in_order([a], b);
	}

	return 'neutral';
}

async function p2022day13_part1(input: string, ...params: any[]) {
	let index = 1;
	let result = 0;
	
	const groups = input.split("\n\n");
	for (const group of groups) {
		const [a, b] = group.split("\n").map(packet => JSON.parse(packet));
		if (in_order(a, b) !== false) { result += index; console.log(index); }
		index++;
	}

	return result;
}

async function p2022day13_part2(input: string, ...params: any[]) {
	const dividers = [[[2]], [[[6]]]]
	const packets = [dividers[0], dividers[1]];
	const groups = input.split("\n\n");
	for (const group of groups) {
		const [a, b] = group.split("\n").map(packet => JSON.parse(packet));
		packets.push(a, b);
	}

	packets.sort((a, b) => {
		const result = in_order(a, b);
		if (result === true) return -1;
		if (result === false) return 1;
		return 0;
	})

	const decoder = (packets.indexOf(dividers[0]) + 1) * (packets.indexOf(dividers[1]) + 1);
	return decoder;
}

async function run() {
	const part1tests: TestCase[] = [{input: `[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]`, expected: '13'}];
	const part2tests: TestCase[] = [];

	// Run tests
	test.beginTests();
	await test.section(async () => {
		for (const testCase of part1tests) {
			test.logTestResult(testCase, String(await p2022day13_part1(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	await test.section(async () => {
		for (const testCase of part2tests) {
			test.logTestResult(testCase, String(await p2022day13_part2(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	test.endTests();

	// Get input and run program while measuring performance
	const input = await util.getInput(DAY, YEAR);

	const part1Before = performance.now();
	const part1Solution = String(await p2022day13_part1(input));
	const part1After = performance.now();

	const part2Before = performance.now()
	const part2Solution = String(await p2022day13_part2(input));
	const part2After = performance.now();

	logSolution(13, 2022, part1Solution, part2Solution);

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
