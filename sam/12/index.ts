import _ from "lodash";
import * as util from "../../../util/util";
import * as test from "../../../util/test";
import chalk from "chalk";
import { log, logSolution, trace } from "../../../util/log";
import { performance } from "perf_hooks";

const YEAR = 2022;
const DAY = 12;

// solution path: /Users/Sam/Documents/advent-of-code-runner/years/2022/12/index.ts
// data path    : /Users/Sam/Documents/advent-of-code-runner/years/2022/12/data.txt
// problem url  : https://adventofcode.com/2022/day/12

async function p2022day12_part1(input: string, ...params: any[]) {
	const lines = input.split("\n");
	const w = lines[0].length;
	let _grid = lines.join('');
	const start = _grid.indexOf("S");
	const end = _grid.indexOf("E");
	let grid = _grid.split('').map(x => x === 'S' 
		? 0 
		: x === 'E' 
		? 25 
		: x.charCodeAt(0) - 97)
	let steps = 0;

	const left = (n: number): number => n % w === 0 ? -1 : n - 1;
	const right = (n: number): number => n % w === (w - 1) ? -1 : n + 1;

	let queue = [start];
	let nodes_at_level = 1;
	let visited = new Set([start]);
	for (let i = 0;;i++){
		if (i >= queue.length) { return Infinity; }
		if (i === nodes_at_level){ steps++; nodes_at_level = queue.length; }
		
		let node = queue[i];
		if (node === end) { break; }

		const adjacents = [left(node), right(node), node + w, node - w];
		for (const adj of adjacents){
			if (!visited.has(adj) && adj >= 0 && adj < grid.length && (grid[adj] <= (grid[node] + 1))) { 
				queue.push(adj); 
				visited.add(adj); 
			}
		}
	}

	return steps;
}

async function p2022day12_part2(input: string, ...params: any[]) {
	const lines = input.split("\n");
	const w = lines[0].length;
	let _grid = lines.join('');
	const end = _grid.indexOf("E");
	let grid = _grid.split('').map(x => x === 'S' 
		? 0 
		: x === 'E' 
		? 25 
		: x.charCodeAt(0) - 97)
		
	const left = (n: number): number => n % w === 0 ? -1 : n - 1;
	const right = (n: number): number => n % w === (w - 1) ? -1 : n + 1;
	
	let min = Infinity;

	for (let i = 0; i < grid.length; i++) {
		if (grid[i] > 0) continue;
			
		let steps = 0;
		let queue = [i];
		let nodes_at_level = 1;
		let visited = new Set([i]);
		for (let j = 0;;j++){
			if (j >= queue.length) { break; }
			if (j === nodes_at_level){ steps++; nodes_at_level = queue.length; }
			
			let node = queue[j];
			if (node === end) { min = Math.min(min, steps); break; }
	
			const adjacents = [left(node), right(node), node + w, node - w];
			for (const adj of adjacents){
				if (!visited.has(adj) && adj >= 0 && adj < grid.length && (grid[adj] <= (grid[node] + 1))) { 
					queue.push(adj); 
					visited.add(adj); 
				}
			}
		}
	}

	return min;
}

async function run() {
	const part1tests: TestCase[] = [{input: `Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi`, 'expected': '31'}];
	const part2tests: TestCase[] = [];

	// Run tests
	test.beginTests();
	await test.section(async () => {
		for (const testCase of part1tests) {
			test.logTestResult(testCase, String(await p2022day12_part1(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	await test.section(async () => {
		for (const testCase of part2tests) {
			test.logTestResult(testCase, String(await p2022day12_part2(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	test.endTests();

	// Get input and run program while measuring performance
	const input = await util.getInput(DAY, YEAR);

	const part1Before = performance.now();
	const part1Solution = String(await p2022day12_part1(input));
	const part1After = performance.now();

	const part2Before = performance.now()
	const part2Solution = String(await p2022day12_part2(input));
	const part2After = performance.now();

	logSolution(12, 2022, part1Solution, part2Solution);

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
