import aoc


@aoc.register(__file__)
def answers():
    instructions = [tuple(line.split()) for line in aoc.read_lines()]

    x = 1
    signals = [x]
    pixels = ''
    for inst in instructions:
        sprite = [x-1, x, x+1]
        pos = len(pixels)

        if inst[0] == 'addx':
            new_val = x + int(inst[1])
            signals.extend([x, new_val])

            pixels += '#' if pos % 40 in sprite else '.'
            pixels += '#' if (pos + 1) % 40 in sprite else '.'
            x = new_val
        elif inst[0] == 'noop':
            signals.append(x)
            pixels += '#' if pos % 40 in sprite else '.'

    signal_strength = [signals[cycle-1] * cycle for cycle in range(20, len(signals), 40)]
    yield sum(signal_strength)

    rows = [pixels[i:i+39] for i in range(0, len(pixels), 40)]
    image = '\n'.join(rows)
    print(image)

if __name__ == '__main__':
    aoc.run()
