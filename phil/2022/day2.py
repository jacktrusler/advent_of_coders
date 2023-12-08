from datetime import datetime


def problem_a(i: str) -> int:
    def score_a(theirs, mine) -> int:
        return [1, 2, 3]['XYZ'.find(mine)] + [3, 0, 6]['ABC'.find(theirs) - 'XYZ'.find(mine)]
    return sum([score_a(line[0], line[2]) for line in i.split('\n') if line != ''])


def problem_b(i: str) -> int:
    def score_b(theirs, score) -> int:
        return [1, 2, 3]['ABC'.find(theirs) + 'ZXY'.find(score) - 2] + 'XYZ'.find(score) * 3
    return sum([score_b(line[0], line[2]) for line in i.split('\n') if line != ''])


if __name__ == '__main__':
    with open('./day2_input.txt', mode='r') as f:
        problem_input = f.read()
    start_a = datetime.now()
    result_a = problem_a(problem_input)
    end_a = datetime.now()
    print(f'A: {result_a}, time: {(end_a - start_a).total_seconds()} seconds')
    start_b = datetime.now()
    result_b = problem_b(problem_input)
    end_b = datetime.now()
    print(f'B: {result_b}, time: {(end_b - start_b).total_seconds()} seconds')
