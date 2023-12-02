def get_input():
    file = "Day 6/input.txt"
    with open(file) as f:
        input = f.read()
    return input


def solve(input):
    list_input = [x for x in input]
    for i in range(len(list_input)):
        if len(set(list_input[i:(i + 14)])) == 14:
            print(i + 14)
            return 0


if __name__ == "__main__":
    solve(get_input())
