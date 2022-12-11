def readfile():
    input = "Day 1/input.txt"
    with open(input) as f:
        lines = f.readlines()
    acc = 0
    elves = []
    for line in lines:
        if line.strip().isnumeric(): 
            acc = acc + int(line)
        if (not line.strip().isnumeric()):
            elves.append(acc)
            acc = 0
    elves.sort()
    sum = elves[-1] + elves[-2] + elves[-3]
    print(sum)

if __name__ == "__main__":
    readfile()