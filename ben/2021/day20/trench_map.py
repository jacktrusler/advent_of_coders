import aoc
import numpy as np
from numpy.typing import NDArray


def enhance_image(image:NDArray, algorithm:NDArray) -> NDArray:
    center = np.where(image == '#', 1, 0)
    up, down = np.roll(center, 1, axis=0), np.roll(center, -1, axis=0)
    left, right = np.roll(center, 1, axis=1), np.roll(center, -1, axis=1)
    up_left, up_right = np.roll(up, 1, axis=1), np.roll(up, -1, axis=1)
    down_left, down_right = np.roll(down, 1, axis=1), np.roll(down, -1, axis=1)
    adjacent = [
        up_left, up, up_right,
        left, center, right,
        down_left, down, down_right
    ]

    indices = sum(np.power(2, i) * ar for i, ar in enumerate(reversed(adjacent)))
    return algorithm[indices]


@aoc.register(__file__)
def answers():
    algorithm, image = aoc.read_chunks('data')
    algorithm = np.array(list(algorithm))
    image = np.array([list(x) for x in image.splitlines()])

    # Expand the image
    EXPAND = 60
    image = np.concatenate((image, np.full((image.shape[0], 2*EXPAND), '.')), axis=1)
    image = np.roll(image, EXPAND, axis=1)
    image = np.concatenate((image, np.full((2*EXPAND, image.shape[1]), '.')), axis=0)
    image = np.roll(image, EXPAND, axis=0)

    # Expand twice
    image1 = image.copy()
    for _ in range(2):
        image1 = enhance_image(image1, algorithm)
    yield len(image1[image1 == '#'])

    # Expand 50 times
    image2 = image.copy()
    for _ in range(50):
        image2 = enhance_image(image2, algorithm)
    yield len(image2[image2 == '#'])

if __name__ == '__main__':
    aoc.run()