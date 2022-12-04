from datetime import datetime


def priority(letter: str) -> int:
    return ord(letter.lower()) - ord('a') + (27 if letter.isupper() else 1)


def problem_a(i: str) -> int:
    return sum([priority((set(row[:len(row)//2]) & set(row[len(row)//2:])).pop()) for row in i.splitlines()])


def problem_b(i: str) -> int:
    rows = i.splitlines()
    groups = [rows[x:x+3] for x in range(0, len(rows), 3)]
    return sum([priority((set(group[0]) & set(group[1]) & set(group[2])).pop()) for group in groups])


if __name__ == '__main__':
    with open('./day3_input.txt', mode='r') as f:
        problem_input = f.read()
    start_a = datetime.now()
    result_a = problem_a(problem_input)
    end_a = datetime.now()
    print(f'A: {result_a}, time: {(end_a - start_a).total_seconds()} seconds')
    start_b = datetime.now()
    result_b = problem_b(problem_input)
    end_b = datetime.now()
    print(f'B: {result_b}, time: {(end_b - start_b).total_seconds()} seconds')
