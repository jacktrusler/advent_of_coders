def buffer_has_4_diff_characters(buffer):
    if len(buffer) > 3:
        if buffer[-1] == buffer[-2] or buffer[-1] == buffer[-3] or buffer[-1] == buffer[-4] or buffer[-2] == buffer[-3] or buffer[-2] == buffer[-4] or buffer[-3] == buffer[-4]:
            return False
        else:
            return True
    else:
        return False

def part_1(input_file):
    with open(input_file) as f:
        lines = [line for line in f]
        count = 0
        buffer = []
        for character in lines[0]:
            count = count + 1
            buffer.append(character)
            if buffer_has_4_diff_characters(buffer):
                return count
    return

# better way to do this for this problem would be to keep track of comparisons then you only need to check newest character against each option, but I'm lazy and input is small enough for n^2 algorithm
def buffer_has_n_diff_characters(buffer,n):
    if len(buffer) < n:
        return False
    else:
        for index in range(n):
            for index_2 in range(n):
                if index == index_2:
                    continue
                if buffer[-(index+1)] == buffer[-(index_2+1)]:
                    return False
        return True

def part_2(input_file):
    with open(input_file) as f:
        lines = [line for line in f]
        count = 0
        buffer = []
        for character in lines[0]:
            count = count + 1
            buffer.append(character)
            if buffer_has_n_diff_characters(buffer,14):
                return count
    return

if __name__ == '__main__':
    print('part 1 answer: ', part_1('input.txt'))
    print('part 2 answer: ', part_2('input.txt'))
    