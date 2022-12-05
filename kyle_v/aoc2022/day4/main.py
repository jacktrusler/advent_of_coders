def check_contained(first_group_start,first_group_end,second_group_start,second_group_end):
    first_group_start = int(first_group_start)
    first_group_end = int(first_group_end)
    second_group_start = int(second_group_start)
    second_group_end = int(second_group_end)

    if(first_group_start >= second_group_start and first_group_end <= second_group_end):
        return True
    if(second_group_start >= first_group_start and second_group_end <= first_group_end):
        return True

    return False

def part_1(input_file):
    with open(input_file) as f:
        count = 0
        lines = [line for line in f]
        # print(check_contained('12','80','8','86')) This did not work when check_contained did not convert to integers
        for pair in lines:
            first_group = pair.split(',')[0]
            second_group = pair.split(',')[1]

            first_group_start = first_group.split('-')[0]
            first_group_end = first_group.split('-')[1]
            second_group_start = second_group.split('-')[0]
            second_group_end = second_group.split('-')[1]

            if(check_contained(first_group_start,first_group_end,second_group_start,second_group_end)):
                count = count + 1

    return count

def check_overlap(first_group_start,first_group_end,second_group_start,second_group_end):
    first_group_start = int(first_group_start)
    first_group_end = int(first_group_end)
    second_group_start = int(second_group_start)
    second_group_end = int(second_group_end)

    if(first_group_start >= second_group_start and first_group_start <= second_group_end):
        return True
    if(first_group_end >= second_group_start and first_group_end <= second_group_end):
        return True
    
    if(second_group_start >= first_group_start and second_group_start <= first_group_end):
        return True
    if(second_group_end >= first_group_start and second_group_end <= first_group_end):
        return True

    return False

def part_2(input_file):
    with open(input_file) as f:
        count = 0
        lines = [line for line in f]
        for pair in lines:
            first_group = pair.split(',')[0]
            second_group = pair.split(',')[1]

            first_group_start = first_group.split('-')[0]
            first_group_end = first_group.split('-')[1]
            second_group_start = second_group.split('-')[0]
            second_group_end = second_group.split('-')[1]

            if(check_overlap(first_group_start,first_group_end,second_group_start,second_group_end)):
                count = count + 1
    return count

if __name__ == '__main__':
    print('part 1 answer: ', part_1('input.txt'))
    print('part 2 answer: ', part_2('input.txt'))
    