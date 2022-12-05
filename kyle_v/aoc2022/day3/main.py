def score_item(item):
    char_num = ord(item)
    # print(f"Item Score: {ord('z')}")
    
    if(char_num > 90):
        return char_num - 96
    else:
        return char_num - 38

    # char_nums
    # a = 97, b = 98, z = 122
    # A = 65, B = 66, Z = 90

    # Desired scores
    # a-z = 1-26
    # A-Z = 27-52

def part_1(input_file):
    score = 0
    with open(input_file) as f:
        lines = [line for line in f]
        for ruksak in lines:
            ruksak = ruksak.rstrip()
            split_point = int(len(ruksak)/2)
            first_compartment = ruksak[:split_point]
            second_compartment = ruksak[split_point:]
            matched_char = ''
            for item in first_compartment:
                # print(f'checking if item: {item} is in {second_compartment}')
                if(item in second_compartment):
                    # print(f'item {item} found in both ruksaks')                    
                    matched_char = matched_char + item
            score = score + score_item(matched_char[0])
    
    return score

def part_2(input_file):
    score = 0
    with open(input_file) as f:
        lines = [line for line in f]
        for elf_group in range(int(len(lines)/3)):
            # figure out what item is in all 3 ruksaks
            first_ruksak = lines[3*elf_group].rstrip()
            second_ruksak = lines[3*elf_group + 1].rstrip()
            third_ruksak = lines[3*elf_group + 2].rstrip()

            shared_item = ''
            for item in first_ruksak:
                if(item in second_ruksak and item in third_ruksak):
                    shared_item = item
                    # print('item: ',item,' elf group: ',elf_group)
            print(f'found item {shared_item} in every ruksak in elf group {elf_group}')
            score = score + score_item(shared_item)
    return score

if __name__ == '__main__':
    print('part 1 answer: ', part_1('input.txt'))
    print('part 2 answer: ', part_2('input.txt'))
    