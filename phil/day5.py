from datetime import datetime


def parse_stacks(raw_input: str):
    stacks = [''] * int(raw_input[-1])
    for line in raw_input.splitlines():
        for stack_index, row_index in enumerate(range(1, len(line), 4)):
            try:
                if line[row_index].isalpha():
                    stacks[stack_index] += line[row_index]
            except IndexError:
                pass
    return stacks


def parse_moves(i: str):
    moves = []
    for line in i.splitlines():
        line_items = line.split()
        moves.append((int(line_items[1]), int(line_items[3]) - 1, int(line_items[5]) - 1))
    return moves


def problem_a(i: str) -> str:
    stack_input, move_input = i.split('\n\n')
    stacks = parse_stacks(stack_input)
    moves = parse_moves(move_input)
    for num, i_from, i_to in moves:
        stacks[i_to] = stacks[i_from][:num][::-1] + stacks[i_to]
        stacks[i_from] = stacks[i_from][num:]
    return ''.join([stack[0] for stack in stacks])


def problem_b(i: str) -> str:
    stack_input, move_input = i.split('\n\n')
    stacks = parse_stacks(stack_input)
    moves = parse_moves(move_input)
    for num, i_from, i_to in moves:
        stacks[i_to] = stacks[i_from][:num] + stacks[i_to]
        stacks[i_from] = stacks[i_from][num:]
    return ''.join([stack[0] for stack in stacks])


if __name__ == '__main__':
    with open('./day5_input.txt', mode='r') as f:
        problem_input = f.read()
    start_a = datetime.now()
    result_a = problem_a(problem_input)
    end_a = datetime.now()
    print(f'A: {result_a}, time: {(end_a - start_a).total_seconds()} seconds')
    start_b = datetime.now()
    result_b = problem_b(problem_input)
    end_b = datetime.now()
    print(f'B: {result_b}, time: {(end_b - start_b).total_seconds()} seconds')
