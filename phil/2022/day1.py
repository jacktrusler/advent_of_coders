from datetime import datetime


def calories(i):
    return [sum([int(num) for num in group.split('\n') if num != '']) for group in i.split('\n\n')]


def problem_a(i):
    return max(calories(i))


def problem_b(i):
    return sum(sorted(calories(i))[-3:])


if __name__ == '__main__':
    with open('./day1_input.txt', mode='r') as f:
        problem_input = f.read()
    start_a = datetime.now()
    result_a = problem_a(problem_input)
    end_a = datetime.now()
    print(f'A: {result_a}, time: {(end_a - start_a).total_seconds()} seconds')
    start_b = datetime.now()
    result_b = problem_b(problem_input)
    end_b = datetime.now()
    print(f'B: {result_b}, time: {(end_b - start_b).total_seconds()} seconds')
