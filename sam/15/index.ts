import _ from "lodash";
import * as util from "../../../util/util";
import * as test from "../../../util/test";
import chalk from "chalk";
import { log, logSolution, trace } from "../../../util/log";
import { performance } from "perf_hooks";
import { doesNotReject } from "assert";

const YEAR = 2022;
const DAY = 15;

// solution path: /Users/Sam/Documents/advent-of-code-runner/years/2022/15/index.ts
// data path    : /Users/Sam/Documents/advent-of-code-runner/years/2022/15/data.txt
// problem url  : https://adventofcode.com/2022/day/15

function mh_dist(x1: number, y1: number, x2: number, y2: number): number {
	return Math.abs(x1 - x2) + Math.abs(y1 - y2);
}

async function p2022day15_part1(input: string, ...params: any[]) {
	const sensors: {x: number, y: number, dist: number}[] = [];
	const beacons = [];
	const lines = input.split("\n");
	for (const line of lines) {
		const [sx, sy, bx, by] = line.match(/-?\d+/g)!.map(Number);
		const sensor = { x: sx, y: sy, dist: mh_dist(bx, by, sx, sy) };
		beacons.push({x: bx, y: by});
		sensors.push(sensor);
	}

	const row = 2000000;
	const blocked = new Set<number>();
	for (const sensor of sensors){
		const y_diff = Math.abs(sensor.y - row);
		if (y_diff <= sensor.dist) {
			const count = (sensor.dist * 2) - (y_diff * 2) + 1; 
			const min_x = sensor.x - sensor.dist + y_diff;
			for (let i = 0; i < count; i++){
				blocked.add(min_x + i);
			}
		}
	}

	for (const beacon of beacons){
		if (beacon.y === row && blocked.has(beacon.x)) { blocked.delete(beacon.x); }
	}
	return blocked.size;
}

async function p2022day15_part2(input: string, ...params: any[]) {
	const sensors: {x: number, y: number, dist: number}[] = [];
	const beacons = [];
	const lines = input.split("\n");
	for (const line of lines) {
		const [sx, sy, bx, by] = line.match(/-?\d+/g)!.map(Number);
		const sensor = { x: sx, y: sy, dist: mh_dist(bx, by, sx, sy) };
		beacons.push({x: bx, y: by});
		sensors.push(sensor);
	}

	const search_max = 4000000;
	for (let i = 0; i < search_max; i++){
		for (let j = 0; j < search_max; j++){
			for (const sensor of sensors){
				const dist = mh_dist(i, j, sensor.x, sensor.y);
				if (dist < sensor.dist){ j += Math.abs(sensor.dist - dist); }
			}

			if (sensors.every(sensor => sensor.dist < mh_dist(sensor.x, sensor.y, i, j))) {
				return i * 4000000 + j;
			}
		}
	}

	return -1;
}

async function run() {
	const part1tests: TestCase[] = [{input: `Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3`, expected: '26'}];
	const part2tests: TestCase[] = [{input: `Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3`, expected: '56000011'}];

	// Run tests
	test.beginTests();
	await test.section(async () => {
		for (const testCase of part1tests) {
			test.logTestResult(testCase, String(await p2022day15_part1(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	await test.section(async () => {
		for (const testCase of part2tests) {
			test.logTestResult(testCase, String(await p2022day15_part2(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	test.endTests();

	// Get input and run program while measuring performance
	const input = await util.getInput(DAY, YEAR);

	const part1Before = performance.now();
	const part1Solution = String(await p2022day15_part1(input));
	const part1After = performance.now();

	const part2Before = performance.now()
	const part2Solution = String(await p2022day15_part2(input));
	const part2After = performance.now();

	logSolution(15, 2022, part1Solution, part2Solution);

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
