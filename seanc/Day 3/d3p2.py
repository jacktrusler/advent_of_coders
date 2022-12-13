def solution():
    input = "Day 3/input.txt"

    elf_1 = []
    elf_2 = []
    elf_3 = []
    elf_groups = []

    with open(input) as f:
        lines = f.readlines()

    for line in range(len(lines)):
        lines[line] = list(lines[line].strip())

    elf_1 = list(lines[::3])
    elf_2 = list(lines[1::3])
    elf_3 = list(lines[2::3])

    for i in range(len(elf_1)):
        elf_groups.append(set(elf_1[i])  & set(elf_2[i]) & set(elf_3[i]))

    for i2 in range(len(elf_groups)):
        if (ord(str(elf_groups[i2])[2])) > 96:
            elf_groups[i2] = int((ord(str(elf_groups[i2])[2])) - 96)
        elif (ord(str(elf_groups[i2])[2])) < 91:
            elf_groups[i2] = int((ord(str(elf_groups[i2])[2])) - 38)
    print(sum(elf_groups))
 

if __name__ == "__main__":
    solution()