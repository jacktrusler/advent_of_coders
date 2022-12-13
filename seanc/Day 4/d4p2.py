def solution():

    input = "Day 4/input.txt"
    acc = 0
    with open(input) as f:
        lines = f.readlines()
    for line in range(len(lines)):
        lines[line] = lines[line].strip().split(sep=",")
        # print(range(len(lines)), '\n')
        for num in range(len(lines[line])):
            lines[line][num] = lines[line][num].split(sep="-")

        if (
            int(lines[line][0][1]) >= int(lines[line][1][0]) 
            and int(lines[line][0][0]) <= int(lines[line][1][1])
            ):

            acc = acc + 1

    print(acc)


if __name__ == "__main__":
    solution()
