#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of Code 2020
adventofcode.com

Day 11
"""

import time
import numpy as np
from scipy.ndimage import convolve

print('* DAY 11 *')

start = time.process_time()

grid_converter = str.maketrans('.L#','012')
with open('2020/day11/data.txt') as layout:
    grid = np.array([[int(x) for x in list(r.translate(grid_converter))]
                     for r in layout.read().splitlines()])

# Part 1
kernel = np.array([[1,1,1],[1,0,1],[1,1,1]])
curr_seats = np.copy(grid)
while True:
    prev_seats = np.copy(curr_seats)
    res = convolve(np.where(curr_seats == 2, 1, 0), kernel, mode='constant')
    curr_seats[(curr_seats == 1) & (res == 0)] = 2
    curr_seats[(curr_seats == 2) & (res >= 4)] = 1
    if (prev_seats == curr_seats).all(): break
                
part1 = np.count_nonzero(curr_seats == 2)

# Part 2
def closest_seat_coord(coord, offset):
    curr_loc = (coord[0] + offset[0], coord[1] + offset[1])
    while 0 <= curr_loc[0] < len(grid) and 0 <= curr_loc[1] < len(grid[curr_loc[0]]) and grid[curr_loc] == 0:
        curr_loc = (curr_loc[0] + offset[0], curr_loc[1] + offset[1])
    return curr_loc
    
directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
neighbours = np.array([[[closest_seat_coord((x, y), d) for d in directions]
                        for y, c in enumerate(r)] for x, r in enumerate(grid)])
neighbours = np.rollaxis(neighbours + 1, -1)
padded_seats = np.zeros((grid.shape[0] + 2, grid.shape[1] + 2))

while True:
    prev_seats = np.copy(grid)
    padded_seats[1:-1, 1:-1] = grid
    neighbour_vals = np.take(padded_seats,
                             np.ravel_multi_index(neighbours,
                                                  padded_seats.shape)
                             )
    res = np.sum(neighbour_vals == 2, axis=2)
    grid[(grid == 1) & (res == 0)] = 2
    grid[(grid == 2) & (res >= 5)] = 1
    if (prev_seats == grid).all(): break

part2 = np.count_nonzero(grid == 2)

end = time.process_time()

print('PART 1:', part1)
print('PART 2:', part2)

print('Time:', round((end - start) * 1000, 3), 'ms')
print()