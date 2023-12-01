import re

def get_input():
    input = "Day 5/input.txt"
    with open(input) as f:
        lines = f.readlines()
    return lines


def split_input(list_of_lines):
    stack_lines = list_of_lines[:(list_of_lines.index('\n')-1)]
    instruction_lines =list_of_lines[(list_of_lines.index('\n')+1):]
    return stack_lines, instruction_lines


def get_stacks(lines, num_stacks):
    # for s in range(num_stacks)
    stacks_as_lists = [[] for _ in range(num_stacks)]
    for line in lines:
        # print(line)
        # line = re.split('(\[[A-Z]\]\s)|(\s{4})',line)
        line = re.split(r'(.{3})\s',line)
        for i in range(num_stacks*2):
            if i % 2 == 1:
                if line[i].strip() != '':
                    stacks_as_lists[i//2].append(line[i].strip())
    for j in stacks_as_lists:
        j = j.reverse()
    return stacks_as_lists


def get_instructions(instruction_lines):
    instructions = []
    for line in instruction_lines:
        line = re.split(r'[A-Za-z\s\n]',line)
        while(line.count('')):
            line.remove('')
        instructions.append(line)
        # line = line
        # print(line)
    # print(instructions)
    return instructions


def move_crates(number, source, dest, stacks):
    for n in range(int(number)):
        temp  = stacks[int(source)-1].pop()
        stacks[int(dest)-1].append(temp)
    return stacks


def get_num_stacks(list_of_lines):
    return int(max(list_of_lines[list_of_lines.index('\n')-1].split()))

def solve(stacks, instructions):
    for i in range(len(instructions)):
        stacks = move_crates(instructions[i][0],instructions[i][1],instructions[i][2],stacks)
    print(stacks)
    return 0


if __name__ == "__main__":
    input_lines = get_input()
    num_stacks = get_num_stacks(input_lines)
    stack_lines, instruction_lines = split_input(input_lines)
    stacks_as_lists = get_stacks(stack_lines,num_stacks)
    instructions = get_instructions(instruction_lines)
    solve(stacks_as_lists,instructions)


