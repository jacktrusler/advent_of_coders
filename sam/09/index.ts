import _ from "lodash";
import * as util from "../../../util/util";
import * as test from "../../../util/test";
import chalk from "chalk";
import { log, logSolution, trace } from "../../../util/log";
import { performance } from "perf_hooks";

const YEAR = 2022;
const DAY = 9;

// solution path: /Users/Sam/Documents/advent-of-code-runner/years/2022/09/index.ts
// data path    : /Users/Sam/Documents/advent-of-code-runner/years/2022/09/data.txt
// problem url  : https://adventofcode.com/2022/day/9

type Direction = "U" | "D" | "L" | "R";
type Position = [number, number];

function move_pos(pos: Position, dir: Direction): void {
	switch(dir){
		case "U": pos[1]++; break;
		case "D": pos[1]--; break;
		case "L": pos[0]--; break;
		case "R": pos[0]++; break;
	}
}

function chase(head: Position, tail: Position): void {
	if (head[1] > tail[1] + 1) { 
		move_pos(tail, 'U');  
		if (head[0] > tail[0]) { move_pos(tail, 'R'); }
		else if (head[0] < tail[0]) { move_pos(tail, 'L'); }
	}
	else if (head[1] < tail[1] - 1) { 
		move_pos(tail, 'D');  
		if (head[0] > tail[0]) { move_pos(tail, 'R'); }
		else if (head[0] < tail[0]) { move_pos(tail, 'L'); }
	}
	else if (head[0] > tail[0] + 1) { 
		move_pos(tail, 'R'); 
		if (head[1] > tail[1]) { move_pos(tail, 'U'); }
		else if (head[1] < tail[1]) { move_pos(tail, 'D'); } 
	}
	else if (head[0] < tail[0] - 1) { 
		move_pos(tail, 'L'); 
		if (head[1] > tail[1]) { move_pos(tail, 'U'); }
		else if (head[1] < tail[1]) { move_pos(tail, 'D'); } 
	}
}

function posToStr(pos: Position): string { return `${pos[0]}:${pos[1]}`; }

async function p2022day9_part1(input: string, ...params: any[]) {
	const visited = new Set();
	visited.add(posToStr([0,0]));
	let h: Position = [0,0];
	let t: Position = [0,0];
	const lines = input.split("\n");
	for (const line of lines) {
		const [move, ct] = line.split(' ');
		for (let i = 0; i < Number(ct); i++){
			move_pos(h, move as Direction);
			chase(h, t);
			visited.add(posToStr(t));
		}
	}
	return visited.size;
}

async function p2022day9_part2(input: string, ...params: any[]) {
	const visited = new Set();
	visited.add(posToStr([0,0]));
	let knots = new Array(10).fill(0).map<Position>(_ => [0,0]);
	const lines = input.split("\n");
	for (const line of lines) {
		const [move, ct] = line.split(' ');
		for (let i = 0; i < Number(ct); i++){
			move_pos(knots[0], move as Direction);
			for (let i = 1; i < knots.length; i++){
				chase(knots[i-1], knots[i]);
			}
			visited.add(posToStr(knots[9]));
		}
	}
	return visited.size;
}

async function run() {
	const part1tests: TestCase[] = [{input:
`R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2`, expected: '13'}];
	const part2tests: TestCase[] = [{input:
`R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20`, expected: '36'}];

	// Run tests
	test.beginTests();
	await test.section(async () => {
		for (const testCase of part1tests) {
			test.logTestResult(testCase, String(await p2022day9_part1(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	await test.section(async () => {
		for (const testCase of part2tests) {
			test.logTestResult(testCase, String(await p2022day9_part2(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	test.endTests();

	// Get input and run program while measuring performance
	const input = await util.getInput(DAY, YEAR);

	const part1Before = performance.now();
	const part1Solution = String(await p2022day9_part1(input));
	const part1After = performance.now();

	const part2Before = performance.now()
	const part2Solution = String(await p2022day9_part2(input));
	const part2After = performance.now();

	logSolution(9, 2022, part1Solution, part2Solution);

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
