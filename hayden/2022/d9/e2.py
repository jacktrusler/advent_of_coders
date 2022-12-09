"""Big Wiggler"""

import math
from time import perf_counter
import numpy as np

ROPE_KNOTS = 10
ROPE_HEAD = 0
ROPE_TAIL = 9


def main():
    with open(file="inputs.txt", mode="r", encoding='utf-8') as f_rope:
        movements = f_rope.readlines()
        f_rope.close()
        uniq_coordinates = set([(0,0)])
        rope = np.empty(ROPE_KNOTS, dtype=object)
        for idx in range(ROPE_KNOTS):
            rope[idx] = (0,0)
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
                print("Begin Step")
                head = tuple(rope[ROPE_HEAD])
                new_head = (head[0] + step_x, head[1] + step_y)
                print(f"Updated Head Position {new_head}")
                rope[ROPE_HEAD] = new_head
                wiggle_handler(head, rope=rope)
                uniq_coordinates.add(rope[ROPE_TAIL])
                print(brainlet_print(rope))
            print(rope)
        print(len(uniq_coordinates))
        

            
def wiggle_handler(previous_head, rope, index=1):
    current_head = tuple(rope[index-1])
    current_knot = tuple(rope[index])
    there_diagonally = real_distance(current_head, current_knot)
    print(f"Head moved to {current_head} from {previous_head}")
    print(f"I am at {current_knot} and my distance is {there_diagonally}")
    if there_diagonally < 2:
        print(f"I do not need to move position")
        return
    print(f"I am moving to {previous_head}")
    rope[index] = previous_head
    if index == ROPE_TAIL:
        return
    print(f"I am calling down chain")
    wiggle_handler(current_knot, rope, index+1)
    
    
def real_distance(point1 , point2):
    (x1,y1) = point1
    (x2,y2) = point2
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

if __name__ == "__main__":
    t_start = perf_counter()
    main()
    t_end = perf_counter()
    print(f"Elapsed: {(t_end-t_start) * 1000} ms")