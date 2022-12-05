def score_thrown(gesture):
    if(gesture == 'X'):
        return 1
    elif(gesture == 'Y'):
        return 2
    elif(gesture == 'Z'):
        return 3

def score_round(elf,you):
    if(elf == 'A'):
        if(you == 'X'):
            return 3
        elif(you == 'Y'):
            return 6
        elif(you == 'Z'):
            return 0
    elif(elf == 'B'):
        if(you == 'X'):
            return 0
        elif(you == 'Y'):
            return 3
        elif(you == 'Z'):
            return 6
    elif(elf == 'C'):
        if(you == 'X'):
            return 6
        elif(you == 'Y'):
            return 0
        elif(you == 'Z'):
            return 3
    

def part_1(input_file):
    # A = Rock
    # B = paper
    # C = Scissors

    # X = Rock
    # Y = Paper
    # Z = scissors
    score = 0
    with open(input_file) as f:
        lines = [line for line in f]
        for line in lines:
            elf, kyle = line.split()
            print(f'elf: {elf} vs kyle: {kyle}')
            score = score + score_thrown(kyle) + score_round(elf,kyle)
    return score

def strat_to_play(elf,your_strat):
    if(elf == 'A'):
        if(your_strat == 'X'):
            return 'Z'
        elif(your_strat == 'Y'):
            return 'X'
        elif(your_strat == 'Z'):
            return 'Y'
    elif(elf == 'B'):
        if(your_strat == 'X'):
            return 'X'
        elif(your_strat == 'Y'):
            return 'Y'
        elif(your_strat == 'Z'):
            return 'Z'
    elif(elf == 'C'):
        if(your_strat == 'X'):
            return 'Y'
        elif(your_strat == 'Y'):
            return 'Z'
        elif(your_strat == 'Z'):
            return 'X'

def part_2(input_file):
    # A = Rock
    # B = paper
    # C = Scissors

    # X = Lose
    # Y = Draw
    # Z = Win
    score = 0
    with open(input_file) as f:
        lines = [line for line in f]
        for line in lines:
            elf, strat = line.split()
            kyle = strat_to_play(elf,strat)
            print(f'elf: {elf} vs kyle: {kyle}')
            score = score + score_thrown(kyle) + score_round(elf,kyle)
    return score

if __name__ == '__main__':
    print(part_1('input.txt'))
    print(part_2('input.txt'))
    