from time import perf_counter
import time
import numpy as np

CAVE_Y = 600
CAVE_X = 600
def main():
    with open(file="inputs.txt", mode="r", encoding="utf-8") as f_cave:
        mapped = np.zeros((CAVE_Y,CAVE_X), dtype=np.unicode_)
        mapped.fill('.')
        cave = f_cave.readlines()
        f_cave.close()
        for d_vein in cave:
            points = d_vein.split("->")
            pen_start = None
            for point in points:
                print(f"Pen is at {pen_start}")
                [x, y] = point.strip().split(",")
                (x, y) = (int(x), int(y))
                if not pen_start:
                    print(f"Initially placing pen at ({x},{y})")
                    pen_start = (x, y)
                else:
                    if x != pen_start[0]:
                        x_start = min(pen_start[0], x)
                        x_stop = max(pen_start[0], x)
                        for x_pos in range(x_start, x_stop+1):
                            print(f"Pen moving to ({x_pos}, {y})")
                            mapped[y,x_pos] = "#"
                    else:
                        y_start = min(pen_start[1], y)
                        y_stop = max(pen_start[1], y)
                        for y_pos in range(y_start, y_stop+1):
                            print(f"Pen moving to {x},{y_pos}")
                            mapped[y_pos,x] = "#"
                    print(f"Placing pen at ({x},{y})")
                    pen_start = (x,y)
        print_that_shit(mapped)
        full_af = False
        sand_in = 0
        while not full_af:
            sand_in += 1
            print(f"Dropping sand {sand_in}")
            sand_y = 0
            sand_x = 500
            resting = False
            while not resting:
                # Attempt to fall downward
                if mapped[sand_y+1, sand_x] == ".":
                    sand_y += 1
                    continue
                else:
                    if mapped[sand_y+1, sand_x-1] == ".":
                    #We've hit something. Can we go left?
                        sand_x -= 1
                        sand_y += 1
                        continue
                    elif mapped[sand_y+1, sand_x+1] == ".":
                    #How about right?
                        sand_x += 1
                        sand_y += 1
                        continue
                    else:
                    # We must stop
                        resting = True
            mapped[sand_y, sand_x] = "@"


def print_that_shit(mapped):
    array = mapped[0:10,494:504]
    for row in array:
        for cel in row:
            print(cel, sep="", end="")
        print()





if __name__ == "__main__":
    t_start = perf_counter()
    main()
    t_end = perf_counter()
    print(f"Elapsed: {(t_end-t_start) * 1000} ms")