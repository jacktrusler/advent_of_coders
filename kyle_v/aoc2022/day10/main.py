def increment_cycle_num(cycle_num, signal_strength,total_strength, x):

    cycle_num = cycle_num + 1
    if(not ((cycle_num - 20) % 40)):
        signal_strength = cycle_num * x
        total_strength = total_strength + signal_strength
        print('signal strength set to',signal_strength)
    return cycle_num, signal_strength, total_strength

def part_1(input_file):
    with open(input_file) as f:
        x = 1
        # noop 1 cycle of doing nothing
        # addx num takes 2 cycles to add num to x
        # signal strength is x * cycle number. updates each 20 + 40*n cycles
        signal_strength = None
        total_strength = 0

        cycle_num = 0
        print('cycle_num:',cycle_num)
        lines = [line for line in f]
        for line in lines:
            line = line.strip()
            instruction = line.split()[0]
            if len(line.split()) > 1:
                # add instruction
                add_num = int(line.split()[1])
            # print(instruction)
            # if instruction != 'noop':
            #     print(add_num)

            if instruction == 'noop':
                cycle_num, signal_strength,total_strength = increment_cycle_num(cycle_num,signal_strength,total_strength,x)
                print('cycle_num:',cycle_num)
            if instruction == 'addx':
                cycle_num, signal_strength,total_strength = increment_cycle_num(cycle_num,signal_strength,total_strength,x)
                print('cycle_num:',cycle_num)
                cycle_num, signal_strength,total_strength = increment_cycle_num(cycle_num,signal_strength,total_strength,x)
                print('cycle_num:',cycle_num)
                x = x + add_num
                print('x assigned to',x)

        print('total_strength:', total_strength)
            
    return total_strength

def get_render(x, cycle_num):
    if(x == (cycle_num%40) or (x-1) == (cycle_num%40) or (x+1) == (cycle_num%40)):
        return '#'
    else:
        return'.'

def part_2(input_file):
    with open(input_file) as f:
        lines = [line for line in f]
        x = 1
        # noop 1 cycle of doing nothing
        # addx num takes 2 cycles to add num to x
        # signal strength is x * cycle number. updates each 20 + 40*n cycles
        signal_strength = None
        total_strength = 0

        render = []

        cycle_num = 0
        print('cycle_num:',cycle_num)
        for line in lines:
            line = line.strip()
            instruction = line.split()[0]
            if len(line.split()) > 1:
                # add instruction
                add_num = int(line.split()[1])
            # print(instruction)
            # if instruction != 'noop':
            #     print(add_num)


            if instruction == 'noop':
                render.append(get_render(x,cycle_num))
                cycle_num, signal_strength,total_strength = increment_cycle_num(cycle_num,signal_strength,total_strength,x)
                print('cycle_num:',cycle_num)
                # render # if x, x-1 or x+1 lines up with the cycle number, otherwise draw .

            if instruction == 'addx':
                render.append(get_render(x,cycle_num))
                cycle_num, signal_strength,total_strength = increment_cycle_num(cycle_num,signal_strength,total_strength,x)
                print('cycle_num:',cycle_num)

                render.append(get_render(x,cycle_num))
                cycle_num, signal_strength,total_strength = increment_cycle_num(cycle_num,signal_strength,total_strength,x)
                print('cycle_num:',cycle_num)


                x = x + add_num
                print('x assigned to',x)

        print(len(render), 'render')
        render_lines = [render[i:i+40] for i in range(0, len(render), 40)]
        for line in render_lines:
            linestring = ''
            for character in line:
                linestring += character
            print(linestring)

        print('total_strength:', total_strength)
            
    return total_strength

if __name__ == '__main__':
    # print('part 1 answer: ', part_1('testiinput.txt'))
    print('part 2 answer: ', part_2('input.txt'))
    