# [N]     [Q]         [N]            
# [R]     [F] [Q]     [G] [M]        
# [J]     [Z] [T]     [R] [H] [J]    
# [T] [H] [G] [R]     [B] [N] [T]    
# [Z] [J] [J] [G] [F] [Z] [S] [M]    
# [B] [N] [N] [N] [Q] [W] [L] [Q] [S]
# [D] [S] [R] [V] [T] [C] [C] [N] [G]
# [F] [R] [C] [F] [L] [Q] [F] [D] [P]
#  1   2   3   4   5   6   7   8   9 

def part_1(input_file):
    with open(input_file) as f:
        lines = [line for line in f]
        # initialize stacks with starting amounts
        stack_1 = ['F','D','B','Z','T','J','R','N']
        stack_2 = ['R','S','N','J','H']
        stack_3 = ['C','R','N','J','G','Z','F','Q']
        stack_4 = ['F','V','N','G','R','T','Q']
        stack_5 = ['L','T','Q','F']
        stack_6 = ['Q','C','W','Z','B','R','G','N']
        stack_7 = ['F','C','L','S','N','H','M']
        stack_8 = ['D','N','Q','M','T','J']
        stack_9 = ['P','G','S']
        
        stacks = [stack_1,stack_2,stack_3,stack_4,stack_5,stack_6,stack_7,stack_8,stack_9]
        # execute instructions to move around the stacks

        for instruction in lines:
            _,num_movements,_, stack_id_from,_, stack_id_to = instruction.split(' ')
            num_movements = int(num_movements)
            stack_id_from = int(stack_id_from) - 1
            stack_id_to = int(stack_id_to) - 1
            # print(num_movements,' ',stack_id_from,' ',stack_id_to)
            for x in range(num_movements):
                package = stacks[stack_id_from].pop()
                stacks[stack_id_to].append(package)
        
        for index,stack in enumerate(stacks):
            print('stack',index,'has',stack.pop())
    return

def part_2(input_file):
    with open(input_file) as f:
        lines = [line for line in f]
        # initialize stacks with starting amounts
        stack_1 = ['F','D','B','Z','T','J','R','N']
        stack_2 = ['R','S','N','J','H']
        stack_3 = ['C','R','N','J','G','Z','F','Q']
        stack_4 = ['F','V','N','G','R','T','Q']
        stack_5 = ['L','T','Q','F']
        stack_6 = ['Q','C','W','Z','B','R','G','N']
        stack_7 = ['F','C','L','S','N','H','M']
        stack_8 = ['D','N','Q','M','T','J']
        stack_9 = ['P','G','S']
        
        stacks = [stack_1,stack_2,stack_3,stack_4,stack_5,stack_6,stack_7,stack_8,stack_9]
        # execute instructions to move around the stacks

        for instruction in lines:
            _,num_movements,_, stack_id_from,_, stack_id_to = instruction.split(' ')
            num_movements = int(num_movements)
            stack_id_from = int(stack_id_from) - 1
            stack_id_to = int(stack_id_to) - 1
            # print(num_movements,' ',stack_id_from,' ',stack_id_to)
            packages = []
            for x in range(num_movements):
                package = stacks[stack_id_from].pop()
                packages.append(package)
            
            for x in range(num_movements):
                package = packages.pop()
                stacks[stack_id_to].append(package)
        
        for index,stack in enumerate(stacks):
            print('stack',index,'has',stack.pop())
    return

if __name__ == '__main__':
    print('part 1 answer: ', part_1('input.txt'))
    print('part 2 answer: ', part_2('input.txt'))
    