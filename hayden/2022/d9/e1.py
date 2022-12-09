"""Wiggler"""

import math
from time import perf_counter
import numpy as np


def main():
    with open(file="inputs.txt", mode="r", encoding='utf-8') as f_rope:
        movements = f_rope.readlines()
        f_rope.close()
        uniq_coordinates = set([(0,0)])
        head_pos = (0,0)
        tail_pos = (0,0)
        for head_update in movements:
            dist = int(head_update[2:].strip())
            directionality = head_update[0]
            step_x = 0
            step_y = 0
            if directionality == "L":
                step_x = -1
            elif directionality == "R":
                step_x = 1
            elif directionality == "U":
                step_y = 1
            elif directionality == "D":
                step_y = -1
            for step in range(dist):
                (head_pos, tail_pos) = rope_handler(step_x, step_y, head_pos,tail_pos)
                uniq_coordinates.add(tail_pos)
        print(len(uniq_coordinates))
        

            
def rope_handler(x, y, head, tail):
    new_head = (head[0] + x, head[1] + y)
    #tail step
    there_diagonally = math.sqrt((new_head[0] - tail[0])**2 + (new_head[1] - tail[1])**2)
    if there_diagonally < 2.0:
        return (new_head, tail)
    return (new_head, head)
    



if __name__ == "__main__":
    t_start = perf_counter()
    main()
    t_end = perf_counter()
    print(f"Elapsed: {(t_end-t_start) * 1000} ms")