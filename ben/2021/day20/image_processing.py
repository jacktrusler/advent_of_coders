import numpy as np
from numpy.typing import NDArray


def expand_array(ar:NDArray, left:int=0, right:int=0, up:int=0, down:int=0) -> NDArray:
    x_expansion, y_expansion = left + right, up + down
    if x_expansion:
        ar = np.concatenate((ar, np.full((ar.shape[0], x_expansion), '.')), axis=1)
        ar = np.roll(ar, left, axis=1)
    if y_expansion:
        ar = np.concatenate((ar, np.full((y_expansion, ar.shape[1]), '.')), axis=0)
        ar = np.roll(ar, up, axis=0)
    return ar


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


with open('2021/day20/image.txt') as f:
    image_input = f.read().splitlines()
    algorithm, image = np.array(list(image_input[0])), image_input[2:]

image = np.array([list(x) for x in image])
image = expand_array(image, left=60, right=60, up=60, down=60)

# Expand twice
for _ in range(50):
    image = enhance_image(image, algorithm)

lit_pixels = len(image[image == '#'])
print(lit_pixels)