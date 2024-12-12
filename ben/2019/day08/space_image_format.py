import aoc


def parse_pixel(pixel: str) -> str:
    return next(x for x in pixel if x < '2')

@aoc.register(__file__)
def answers():
    image_data = aoc.read_data()
    shape = (25, 6)

    area = shape[0] * shape[1]
    layers = [image_data[i:i+area] for i in range(0, len(image_data), area)]

    _, fewest_zero_layer = min((l.count('0'), l) for l in layers)
    yield fewest_zero_layer.count('1') * fewest_zero_layer.count('2')

    pixels = [parse_pixel(x) for x in zip(*layers)]
    image = [pixels[i:i+shape[0]] for i in range(0, len(pixels), shape[0])]
    image = '\n'.join(''.join(x) for x in image).replace('0', ' ')
    yield f'\n{image}'

if __name__ == '__main__':
    aoc.run()
