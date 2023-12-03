from time import perf_counter_ns


def decrypt(numbers: list[int], key: int = 1, n: int = 1):
    i_numbers = list(range(len(numbers)))
    numbers = [x * key for x in numbers]
    for _ in range(n):
        for i in range(len(numbers)):
            next_index = i_numbers.index(i)
            insert_at = (next_index + numbers[i]) % (len(numbers) - 1)
            i_numbers.insert(insert_at, i_numbers.pop(next_index))
    zero_index = i_numbers.index(numbers.index(0))
    return sum(numbers[i_numbers[(zero_index + x) % len(numbers)]] for x in (1000, 2000, 3000))


def solve(raw_input: str):
    numbers = [int(x) for x in raw_input.splitlines()]
    a = decrypt(numbers)
    b = decrypt(numbers, key=811589153, n=10)
    return a, b


def main():
    with open('./day20_input.txt', mode='r') as f:
        problem_input = f.read()
    start_time = perf_counter_ns()
    a, b = solve(problem_input)
    end_time = perf_counter_ns()
    elapsed_ms = round((end_time - start_time) / 1000000, 3)
    print(f'A: {a}')
    print(f'B: {b}')
    print(f'Elapsed time: {elapsed_ms} ms')


if __name__ == '__main__':
    main()
