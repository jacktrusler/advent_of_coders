import _ from "lodash";
import * as util from "../../../util/util";
import * as test from "../../../util/test";
import chalk from "chalk";
import { log, logSolution, trace } from "../../../util/log";
import { performance } from "perf_hooks";

const YEAR = 2022;
const DAY = 11;

// solution path: /Users/Sam/Documents/advent-of-code-runner/years/2022/11/index.ts
// data path    : /Users/Sam/Documents/advent-of-code-runner/years/2022/11/data.txt
// problem url  : https://adventofcode.com/2022/day/11

async function p2022day11_part1(input: string, ...params: any[]) {
	const monkeys: any = [];
	const groups = input.split("\n\n");
	for (const group of groups) {
		const lines = group.split("\n");
		const items = lines[1].split(': ')[1].split(', ').map(Number);
		const [,,,,,,op, op_value] = lines[2].split(' ');
		const [,,,,,divisor] = lines[3].split(' ');
		const [,,,,,,,,,onsuccess] = lines[4].split(' ');
		const [,,,,,,,,,onfail] = lines[5].split(' ');
		monkeys.push({items, op, op_value, divisor: Number(divisor), onsuccess, onfail, inspections: 0});
	}

	function inspect(monkey: any): void{
		while (monkey.items.length){
			monkey.inspections++;
			let item = monkey.items.pop();
			if (monkey.op === "*" && monkey.op_value === "old") { item *= item; }
			else if (monkey.op === "*") { item *= Number(monkey.op_value);  }
			else { item += Number(monkey.op_value); }
			item = Math.floor(item / 3);
			if (item % monkey.divisor === 0) { monkeys[monkey.onsuccess].items.push(item); }
			else { monkeys[monkey.onfail].items.push(item); }
		}
	}

	for (let i = 0; i < 20; i++){
		for (const monkey of monkeys) {
			inspect(monkey);
		}
	}

	monkeys.sort((a: any, b: any) => b.inspections - a.inspections);
	return monkeys[0].inspections * monkeys[1].inspections;
}

async function p2022day11_part2(input: string, ...params: any[]) {
	const monkeys: any = [];
	const groups = input.split("\n\n");
	for (const group of groups) {
		const lines = group.split("\n");
		const items = lines[1].split(': ')[1].split(', ').map(Number);
		const [,,,,,,op, op_value] = lines[2].split(' ');
		const [,,,,,divisor] = lines[3].split(' ');
		const [,,,,,,,,,onsuccess] = lines[4].split(' ');
		const [,,,,,,,,,onfail] = lines[5].split(' ');
		monkeys.push({items, op, op_value, divisor: Number(divisor), onsuccess, onfail, inspections: 0});
	}
	const gcd = monkeys.reduce((a: any, b: any) => a * b.divisor, 1);

	function inspect(monkey: any): void {
		while (monkey.items.length){
			monkey.inspections++;
			let item = monkey.items.pop();
			if (monkey.op === "*" && monkey.op_value === "old") { item *= item; }
			else if (monkey.op === "*") { item *= Number(monkey.op_value);  }
			else { item += Number(monkey.op_value); }
			item = item % gcd;
			if (item % monkey.divisor === 0) { monkeys[monkey.onsuccess].items.push(item); }
			else { monkeys[monkey.onfail].items.push(item); }
		}
	}

	for (let i = 0; i < 10000; i++){
		for (const monkey of monkeys) {
			inspect(monkey);
		}
	}

	console.log(monkeys);
	monkeys.sort((a: any, b: any) => b.inspections - a.inspections);
	return monkeys[0].inspections * monkeys[1].inspections;
}

async function run() {
	const part1tests: TestCase[] = [{input: `Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1`, expected: '10605'}];
	const part2tests: TestCase[] = [{input: `Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1`, expected: '2713310158'}];

	// Run tests
	test.beginTests();
	await test.section(async () => {
		for (const testCase of part1tests) {
			test.logTestResult(testCase, String(await p2022day11_part1(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	await test.section(async () => {
		for (const testCase of part2tests) {
			test.logTestResult(testCase, String(await p2022day11_part2(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	test.endTests();

	// Get input and run program while measuring performance
	const input = await util.getInput(DAY, YEAR);

	const part1Before = performance.now();
	const part1Solution = String(await p2022day11_part1(input));
	const part1After = performance.now();

	const part2Before = performance.now()
	const part2Solution = String(await p2022day11_part2(input));
	const part2After = performance.now();

	logSolution(11, 2022, part1Solution, part2Solution);

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
