from time import perf_counter_ns


def report(a, b, elapsed_time):
    print(f'A: {a}\nB: {b}\nElapsed time: {elapsed_time} ms')


def run_solution(func, input_file):
    with open(input_file, mode='r') as f:
        problem_input = f.read()
    start_time = perf_counter_ns()
    a, b = func(problem_input)
    end_time = perf_counter_ns()
    elapsed_ms = round((end_time - start_time) / 1000000, 3)
    return a, b, elapsed_ms
