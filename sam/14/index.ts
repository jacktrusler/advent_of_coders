import _ from "lodash";
import * as util from "../../../util/util";
import * as test from "../../../util/test";
import chalk from "chalk";
import { log, logSolution, trace } from "../../../util/log";
import { performance } from "perf_hooks";

const YEAR = 2022;
const DAY = 14;

// solution path: /Users/Sam/Documents/advent-of-code-runner/years/2022/14/index.ts
// data path    : /Users/Sam/Documents/advent-of-code-runner/years/2022/14/data.txt
// problem url  : https://adventofcode.com/2022/day/14

function p_to_s(x: number, y: number): string { return `${x}.${y}`}

async function p2022day14_part1(input: string, ...params: any[]) {
	const blocked = new Set();
	let sand_count = 0;
	let max_y = 0;

	const lines = input.split("\n");
	for (const line of lines) {
		const coords = line.split(' -> ').map(xy => xy.split(',').map(Number));
		for (let i = 0; i < coords.length - 1; i++){
			const [x1, y1] = coords[i];
			const [x2, y2] = coords[i+1];

			if (x1 < x2) 
				new Array(Math.abs(x1 - x2) + 1).fill(0).forEach((_, idx) => blocked.add(p_to_s(x1 + idx, y1)));
			if (x2 < x1) 
				new Array(Math.abs(x1 - x2) + 1).fill(0).forEach((_, idx) => blocked.add(p_to_s(x2 + idx, y1)));
			if (y1 < y2)
				new Array(Math.abs(y1 - y2) + 1).fill(0).forEach((_, idx) => blocked.add(p_to_s(x1, y1 + idx)));
			if (y2 < y1)
				new Array(Math.abs(y1 - y2) + 1).fill(0).forEach((_, idx) => blocked.add(p_to_s(x1, y2 + idx)));
			
			max_y = Math.max(max_y, y1, y2);
		}
	}

	const start_x = 500;
	const start_y = 0;
	let sand = [start_x, start_y];


	while (sand[1] < max_y) {
		if (!blocked.has(p_to_s(sand[0], sand[1] + 1))){ 
			sand[1]++; 
		} else if (!blocked.has(p_to_s(sand[0] - 1, sand[1] + 1))){
			sand[0]--; 
			sand[1]++;
		} else if (!blocked.has(p_to_s(sand[0] + 1, sand[1] + 1))){
			sand[0]++; 
			sand[1]++;
		} else {
			blocked.add(p_to_s(sand[0], sand[1]));
			sand = [start_x, start_y];
			sand_count++;
		}
	}

	return sand_count;
}

async function p2022day14_part2(input: string, ...params: any[]) {
	const blocked = new Set();
	let sand_count = 0;
	let max_y = 0;

	const lines = input.split("\n");
	for (const line of lines) {
		const coords = line.split(' -> ').map(xy => xy.split(',').map(Number));
		for (let i = 0; i < coords.length - 1; i++){
			const [x1, y1] = coords[i];
			const [x2, y2] = coords[i+1];

			if (x1 < x2) 
				new Array(Math.abs(x1 - x2) + 1).fill(0).forEach((_, idx) => blocked.add(p_to_s(x1 + idx, y1)));
			if (x2 < x1) 
				new Array(Math.abs(x1 - x2) + 1).fill(0).forEach((_, idx) => blocked.add(p_to_s(x2 + idx, y1)));
			if (y1 < y2)
				new Array(Math.abs(y1 - y2) + 1).fill(0).forEach((_, idx) => blocked.add(p_to_s(x1, y1 + idx)));
			if (y2 < y1)
				new Array(Math.abs(y1 - y2) + 1).fill(0).forEach((_, idx) => blocked.add(p_to_s(x1, y2 + idx)));
			
			max_y = Math.max(max_y, y1, y2);
		}
	}

	max_y += 2;
	const start_x = 500;
	const start_y = 0;
	let sand = [start_x, start_y];

	while (true) {
		if (sand[1] === max_y - 1){
			blocked.add(p_to_s(sand[0], sand[1]));
			sand_count++;
			sand = [start_x, start_y];
		}

		if (!blocked.has(p_to_s(sand[0], sand[1] + 1))){ 
			sand[1]++; 
		} else if (!blocked.has(p_to_s(sand[0] - 1, sand[1] + 1))){
			sand[0]--; 
			sand[1]++;
		} else if (!blocked.has(p_to_s(sand[0] + 1, sand[1] + 1))){
			sand[0]++; 
			sand[1]++;
		} else {
			blocked.add(p_to_s(sand[0], sand[1]));
			sand_count++;
			if (sand[0] === start_x && sand[1] === start_y){ break; }
			sand = [start_x, start_y];
		}
	}

	return sand_count;
}

async function run() {
	const part1tests: TestCase[] = [{input:`498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9`, expected: '24'}];
	const part2tests: TestCase[] = [];

	// Run tests
	test.beginTests();
	await test.section(async () => {
		for (const testCase of part1tests) {
			test.logTestResult(testCase, String(await p2022day14_part1(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	await test.section(async () => {
		for (const testCase of part2tests) {
			test.logTestResult(testCase, String(await p2022day14_part2(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	test.endTests();

	// Get input and run program while measuring performance
	const input = await util.getInput(DAY, YEAR);

	const part1Before = performance.now();
	const part1Solution = String(await p2022day14_part1(input));
	const part1After = performance.now();

	const part2Before = performance.now()
	const part2Solution = String(await p2022day14_part2(input));
	const part2After = performance.now();

	logSolution(14, 2022, part1Solution, part2Solution);

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
