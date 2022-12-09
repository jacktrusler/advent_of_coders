"""Treetop Tree House"""

import math
from time import perf_counter
import numpy as np

UPWARDS = (0,1)
DOWNWARDS = (0,-1)
LEFTWARDS = (-1,0)
RIGHTWARDS = (0,1)

def main():
    with open(file="inputs.txt", mode="r", encoding='utf-8') as f_rope:
        movements = f_rope.readlines()
        f_rope.close()
        uniq_coordinates = set([(0,0)])
        head_pos = (0,0)
        tail_pos = (0,0)
        print(f"Head: {head_pos}")
        print(f"Tail: {tail_pos}")
        for head_update in movements:
            dist = int(head_update[2:].strip())
            directionality = head_update[0]
            for step in range(dist):
                if directionality == "L":
                    (new_head, new_tail) = rope_handler(-1,0,head_pos,tail_pos)
                elif directionality == "R":
                    (new_head, new_tail) = rope_handler(1,0,head_pos,tail_pos)
                elif directionality == "U":
                    (new_head, new_tail) = rope_handler(0,1,head_pos,tail_pos)
                elif directionality == "D":
                    (new_head, new_tail) = rope_handler(0,-1,head_pos,tail_pos)
                head_pos = new_head
                tail_pos = new_tail
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