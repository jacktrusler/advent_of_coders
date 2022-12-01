def part_1(input_file):
    with open(input_file) as f:
        lines = [line for line in f]

    max = 0
    count = 0
    for line in lines:
        line = line.rstrip()
        # print(line)
        if(line == ''):
            if(count > max):
                max = count
            count = 0
        else:
            count = count + int(line)
    if(count > max):
        max = count
    count = 0

    print(f'max {max}')

class MaxObj:
    def __init__(self):
        self.largest = 0
        self.second = 0
        self.third = 0

    def set_value(self, newVal):
        if(newVal > self.largest):
            self.third = self.second
            self.second = self.largest
            self.largest = newVal
        elif(newVal > self.second):
            self.third = self.second
            self.second = newVal
        elif (newVal > self.third):
            self.third = newVal
        return

    def count(self):
        return self.largest + self.second + self.third

    def __str__(self):
        return f'{self.largest}, {self.second}, {self.third}'


def part_2(input_file):
    with open(input_file) as f:
        lines = [line for line in f]

    maxObj = MaxObj()
    count = 0
    for line in lines:
        line = line.rstrip()
        # print(line)
        if(line == ''):
            maxObj.set_value(count)
            count = 0
        else:
            count = count + int(line)
    maxObj.set_value(count)
    count = 0

    print(f'max boi {maxObj}')
    print(f'Total: {maxObj.count()}')

if __name__ == '__main__':
    part_1('input.txt')
    part_2('input.txt')
    