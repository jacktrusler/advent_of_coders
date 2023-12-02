def solution():
    input = "Day 3/input.txt"

    backpack_front = []
    backpack_rear = []
    backpack_dupes = []

    with open(input) as f:
        lines = f.readlines()

    for line in lines:
        half = int(len(line)/2)
        backpack_front.append(list(line.strip()[:half]))
        backpack_rear.append(list(line.strip()[half:]))

    for i in range(len(backpack_rear)):
        backpack_dupes.append(set(backpack_rear[i]) & set(backpack_front[i]))

    for i2 in range(len(backpack_dupes)):

        if (ord(str(backpack_dupes[i2])[2])) > 96:
            backpack_dupes[i2] = int((ord(str(backpack_dupes[i2])[2])) - 96)

        elif (ord(str(backpack_dupes[i2])[2])) < 91:
            backpack_dupes[i2] = int((ord(str(backpack_dupes[i2])[2])) - 38)

    print(sum(backpack_dupes))


if __name__ == "__main__":
    solution()