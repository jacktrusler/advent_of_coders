import _ from "lodash";
import * as util from "../../../util/util";
import * as test from "../../../util/test";
import chalk from "chalk";
import { log, logSolution, trace } from "../../../util/log";
import { performance } from "perf_hooks";

const YEAR = 2022;
const DAY = 8;

// solution path: /Users/Sam/Documents/advent-of-code-runner/years/2022/08/index.ts
// data path    : /Users/Sam/Documents/advent-of-code-runner/years/2022/08/data.txt
// problem url  : https://adventofcode.com/2022/day/8

async function p2022day8_part1(input: string, ...params: any[]) {
	let visible = 0;
	const w = [];
	const e = [];
	const n = [];
	const s = [];
	const grid = input.split('\n');

	for (let row = 0; row < grid.length; row++){
		let max = -1;
		const line = [];
		for (let col = 0; col < grid[0].length; col++){
			line.push(max);
			max = Math.max(max, Number(grid[row][col]))
		}
		w.push(line);
	}

	for (let row = 0; row < grid.length; row++){
		let max = -1;
		const line = [];
		for (let col = grid[0].length-1; col >= 0; col--){
			line[col] = max;
			max = Math.max(max, Number(grid[row][col]))
		}
		e.push(line);
	}

	for (let col = 0; col < grid[0].length; col++){
		let max = -1;
		const line = [];
		for (let row = 0; row < grid.length; row++){
			line.push(max);
			max = Math.max(max, Number(grid[row][col]))
		}
		n.push(line);
	}

	for (let col = 0; col < grid[0].length; col++){
		let max = -1;
		const line = [];
		for (let row = grid.length - 1; row >= 0; row--){
			line[row] = max;
			max = Math.max(max, Number(grid[row][col]))
		}
		s.push(line);
	}

	for (let row = 0; row < grid.length; row++){
		for (let col = 0; col < grid[0].length; col++){
			const h = Number(grid[row][col]);
			if (
				n[col][row] < h ||
				s[col][row] < h ||
				w[row][col] < h	||
				e[row][col] < h			
			){
				visible++;
			}
		}
	}

	return visible;
}

async function p2022day8_part2(input: string, ...params: any[]) {
	const grid = input.split('\n')
	let max_visibility = -1;

	function visibility(row: number, col: number): number {
		if (row == 0 || row == grid.length - 1 || col == 0 || col == grid[0].length - 1) return 0;
		
		const h = grid[row][col];
		let vis = 1;

		// look left
		{
			let offset = 1;
			while (col-offset >= 0 && grid[row][col-offset] < h){
				offset++;
			}
			vis *= col-offset >= 0 ? offset : offset - 1;
		}

		// look right
		{
			let offset = 1;
			while (col+offset <= grid[0].length - 1 && grid[row][col+offset] < h) {
				offset++;
			}
			vis *= col+offset <= grid[0].length - 1 ? offset : offset - 1;;
		}

		// look up
		{
			let offset = 1;
			while (row-offset >= 0 && grid[row-offset][col] < h) {
				offset++;
			}
			vis *= row-offset >= 0 ? offset : offset - 1;;
		}

		// look right
		{
			let offset = 1;
			while (row+offset <= grid.length - 1 && grid[row+offset][col] < h) {
				offset++;
			}
			vis *= row+offset <= grid.length - 1 ? offset : offset - 1;
		}

		return vis;
	}

	for (let row = 0; row < grid.length; row++){
		for (let col = 0; col < grid[0].length; col++){
			max_visibility = Math.max(visibility(row, col), max_visibility);
		}
	}
	
	return max_visibility;
}

async function run() {
	const part1tests: TestCase[] = [{input: `30373
25512
65332
33549
35390`, expected: '21'}];
	const part2tests: TestCase[] = [{input: `30373
25512
65332
33549
35390`, expected: '8'}];

	// Run tests
	test.beginTests();
	await test.section(async () => {
		for (const testCase of part1tests) {
			test.logTestResult(testCase, String(await p2022day8_part1(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	await test.section(async () => {
		for (const testCase of part2tests) {
			test.logTestResult(testCase, String(await p2022day8_part2(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	test.endTests();

	// Get input and run program while measuring performance
	const input = await util.getInput(DAY, YEAR);

	const part1Before = performance.now();
	const part1Solution = String(await p2022day8_part1(input));
	const part1After = performance.now();

	const part2Before = performance.now()
	const part2Solution = String(await p2022day8_part2(input));
	const part2After = performance.now();

	logSolution(8, 2022, part1Solution, part2Solution);

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
