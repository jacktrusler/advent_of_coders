def apply_dir(direction, head, tail):
    # Check if tail is touching

    # Move Head
    if (direction == 'R'):
        head[0] = head[0] + 1
    elif(direction == 'L'):
        head[0] = head[0] - 1
    elif(direction == 'D'):
        head[1] = head[1] - 1
    elif(direction =='U'):
        head[1] = head[1] + 1

    no_move_required = abs(head[0] - tail[0]) <= 1 and abs(head[1] - tail[1]) <= 1

    if no_move_required:
        # print('no tail move required')
        return head,tail

    # if(head[0] == tail[0] or head[1] == tail[1] ):
    #     print("head and tail share at least 1 axis")
    # else:
    #     print('NO AXIS')
    # Check if head and tail share at least 1 axis
    diag_move_required = not (head[0] == tail[0] or head[1] == tail[1])

    if(diag_move_required):
        pass
        if (head[0] > tail[0]):
            tail[0] = tail[0] + 1
        else:
            tail[0] = tail[0] - 1
        if (head[1] > tail[1]):
            tail[1] = tail[1] + 1
        else:
            tail[1] = tail[1] - 1
    else:
        # normal move
        # Move Tail
        if((head[0] - tail[0]) > 1):
            # case, head is too far to right
            tail[0] = tail[0] + 1
        elif((tail[0] - head[0]) > 1):
            # case, head is too far to the left
            tail[0] = tail[0] - 1
        if((head[1] - tail[1]) > 1):
            # case, head is too far up
            tail[1] = tail[1] + 1
        elif((tail[1] - head[1]) > 1):
            # case, head is too far down
            tail[1] = tail[1] - 1

    return head,tail

def head_move(direction, head):
    # Move Head
    if (direction == 'R'):
        head[0] = head[0] + 1
    elif(direction == 'L'):
        head[0] = head[0] - 1
    elif(direction == 'D'):
        head[1] = head[1] - 1
    elif(direction =='U'):
        head[1] = head[1] + 1
    return head


def tail_move(direction, head, tail):
    no_move_required = abs(head[0] - tail[0]) <= 1 and abs(head[1] - tail[1]) <= 1

    if no_move_required:
        # print('no tail move required')
        return head,tail

    # if(head[0] == tail[0] or head[1] == tail[1] ):
    #     print("head and tail share at least 1 axis")
    # else:
    #     print('NO AXIS')
    # Check if head and tail share at least 1 axis
    diag_move_required = not (head[0] == tail[0] or head[1] == tail[1])

    if(diag_move_required):
        pass
        if (head[0] > tail[0]):
            tail[0] = tail[0] + 1
        else:
            tail[0] = tail[0] - 1
        if (head[1] > tail[1]):
            tail[1] = tail[1] + 1
        else:
            tail[1] = tail[1] - 1
    else:
        # normal move
        # Move Tail
        if((head[0] - tail[0]) > 1):
            # case, head is too far to right
            tail[0] = tail[0] + 1
        elif((tail[0] - head[0]) > 1):
            # case, head is too far to the left
            tail[0] = tail[0] - 1
        if((head[1] - tail[1]) > 1):
            # case, head is too far up
            tail[1] = tail[1] + 1
        elif((tail[1] - head[1]) > 1):
            # case, head is too far down
            tail[1] = tail[1] - 1
    return head, tail


def part_1(input_file):
    with open(input_file) as f:
        # [x,y]
        head = [0,0]
        tail = [0,0]
        tail_locations = {}

        lines = [line for line in f]
        for line in lines:

            line = line.strip()
            direction, magnitude = line.split()
            for _ in range(int(magnitude)):
                head,tail = apply_dir(direction, head, tail)
                # print('head:',head)
                # print('tail:',tail)
                # print()
                tail_locations[f'{tail[0],tail[1]}'] = True
            # print('end of instruction')

        print(len(tail_locations))
            
    return len(tail_locations)

def part_2(input_file):
    with open(input_file) as f:
        # [x,y]
        # rope[0] is head rope [9] is tail
        rope = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
        tail_locations = {}

        lines = [line for line in f]
        for line in lines:

            line = line.strip()
            direction, magnitude = line.split()
            for _ in range(int(magnitude)):
                # move head
                rope[0] = head_move(direction, rope[0])
                # move all tails
                for index, _ in enumerate(range(len(rope) - 1)):
                    rope[index], rope[index+1] = tail_move(direction, rope[index], rope[index+1])
                tail_locations[f'{rope[9][0],rope[9][1]}'] = True

        print(len(tail_locations))
    return

if __name__ == '__main__':
    print('part 1 answer: ', part_1('testinput.txt'))
    print('part 2 answer: ', part_2('input.txt'))
    