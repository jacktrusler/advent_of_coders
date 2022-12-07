import _ from "lodash";
import * as util from "../../../util/util";
import * as test from "../../../util/test";
import chalk from "chalk";
import { log, logSolution, trace } from "../../../util/log";
import { performance } from "perf_hooks";

const YEAR = 2022;
const DAY = 7;

// solution path: /Users/Sam/Documents/advent-of-code-runner/years/2022/07/index.ts
// data path    : /Users/Sam/Documents/advent-of-code-runner/years/2022/07/data.txt
// problem url  : https://adventofcode.com/2022/day/7

async function p2022day7_part1(input: string, ...params: any[]) {
	const dirs: {[k: string]: number} = {};
	let path: string[] = [];
	const lines = input.split("\n");
	for (const line of lines) {
		const [a,b,c] = line.split(' ');
		if (a === '$'){
			if (b !== 'cd'){ continue; }
			if (c === '..'){ path.pop(); }
			else { path.push(c); }
		}
		else if (a !== 'dir'){
			const tmp = [];
			for (let i = 0; i < path.length; i ++){
				tmp.push(path[i]);
				const dir = tmp.join('/');
				dirs[dir] =  (dirs[dir] || 0) + Number(a);
			}
		}
	}
	return Object.values(dirs).filter(x => x < 100000).reduce((a,c) => a + c, 0);
}

async function p2022day7_part2(input: string, ...params: any[]) {
	const dirs: {[k: string]: number} = {};
	let path: string[] = [];
	const lines = input.split("\n");
	for (const line of lines) {
		const [a,b,c] = line.split(' ');
		if (a === '$'){
			if (b !== 'cd'){ continue; }
			if (c === '..'){ path.pop(); }
			else { path.push(c); }
		}
		else if (a !== 'dir'){
			const tmp = [];
			for (let i = 0; i < path.length; i ++){
				tmp.push(path[i]);
				const dir = tmp.join('/');
				dirs[dir] =  (dirs[dir] || 0) + Number(a);
			}
		}
	}
	const capacity = 70000000;
	const used = dirs['/']
	const required = 30000000;
	const unused = capacity - used; 
	const to_free = required - unused;
	return Object.values(dirs).sort((a, b) => a - b).find(x => x >= to_free);
}

async function run() {
	const part1tests: TestCase[] = [{
		input: `$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k`, expected: '95437'}];
	const part2tests: TestCase[] = [{
		input: `$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k`, expected: '95437'}];

	// Run tests
	test.beginTests();
	await test.section(async () => {
		for (const testCase of part1tests) {
			test.logTestResult(testCase, String(await p2022day7_part1(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	await test.section(async () => {
		for (const testCase of part2tests) {
			test.logTestResult(testCase, String(await p2022day7_part2(testCase.input, ...(testCase.extraArgs || []))));
		}
	});
	test.endTests();

	// Get input and run program while measuring performance
	const input = await util.getInput(DAY, YEAR);

	const part1Before = performance.now();
	const part1Solution = String(await p2022day7_part1(input));
	const part1After = performance.now();

	const part2Before = performance.now()
	const part2Solution = String(await p2022day7_part2(input));
	const part2After = performance.now();

	logSolution(7, 2022, part1Solution, part2Solution);

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



async function part1bad(input: string, ...params: any[]) {
	const dirs: any = {__size: 0, __files: []};
	let path: string[] = [];
	const lines = input.split("\n");
	for (let i = 0; i < lines.length; i++) {
		const line = lines[i];
		if (line[0] == '$'){
			const [,cmd,arg] = line.split(' ');
			switch(cmd){
				case 'cd':
					if (arg === '..') { path.pop(); break; }
					if (arg === '/') { path = []; break; }
					path.push(arg);
					break;
				case 'ls':
					let tmp = dirs;
					for (const seg of path){
						if (!Object.hasOwnProperty.call(tmp, seg)) tmp[seg] = {__size: 0,  __files: []};
						tmp = tmp[seg];
					}

					while (i < lines.length - 1 && lines[i+1][0] !== '$'){
						const line2 = lines[++i];
						if (line2[0] === 'd'){
							const [,name] = line2.split(' ');
							tmp[name] = tmp[name] || {__size: 0,  __files: []};
						} else {
							const [size, name] = line2.split(' ');
							if (!tmp.__files.includes(name)) { tmp.__size += Number(size); } 
							tmp.__files.push(name);
						}
					}
					break;
			}
		}
	}

	let acc = 0;
	function helper(o: any) {
		let total = o.__size;
		for (const c in o){
			if (c !== '__size' && c !== '__files') { total += helper(o[c]); }
		}
		if (total < 100000) acc += total;
		return total;
	}

	//console.log(dirs);
	helper(dirs);
	return acc;
}

async function part2bad(input: string, ...params: any[]) {
	const dirs: any = {__size: 0, __files: []};
	let path: string[] = [];
	const lines = input.split("\n");
	for (let i = 0; i < lines.length; i++) {
		const line = lines[i];
		if (line[0] == '$'){
			const [,cmd,arg] = line.split(' ');
			switch(cmd){
				case 'cd':
					if (arg === '..') { path.pop(); break; }
					if (arg === '/') { path = []; break; }
					path.push(arg);
					break;
				case 'ls':
					let tmp = dirs;
					for (const seg of path){
						if (!Object.hasOwnProperty.call(tmp, seg)) tmp[seg] = {__size: 0,  __files: []};
						tmp = tmp[seg];
					}

					while (i < lines.length - 1 && lines[i+1][0] !== '$'){
						const line2 = lines[++i];
						if (line2[0] === 'd'){
							const [,name] = line2.split(' ');
							tmp[name] = tmp[name] || {__size: 0,  __files: []};
						} else {
							const [size, name] = line2.split(' ');
							if (!tmp.__files.includes(name)) { tmp.__size += Number(size); } 
							tmp.__files.push(name);
						}
					}
					break;
			}
		}
	}

	function get_used(o: any) {
		let total = o.__size;
		for (const c in o){
			if (c !== '__size' && c !== '__files') { total += get_used(o[c]); }
		}
		return total;
	}
	
	const capacity = 70000000;
	const used = get_used(dirs);
	const required = 30000000;
	const unused = capacity - used; 
	const to_free = required - unused;
	
	const dir_sizes: number[] = [];
	function helper(o: any) {
		let total = o.__size;
		for (const c in o){
			if (c !== '__size' && c !== '__files') { total += helper(o[c]); }
		}
		dir_sizes.push(total);
		return total;
	}
	helper(dirs);
	dir_sizes.sort((a,b) => a - b);
	for (let i = 0; i < dir_sizes.length; i++){
		if (dir_sizes[i] >= to_free) return dir_sizes[i]
	}
}