"""Third Income Dominator"""
from time import perf_counter
import numpy as np


def main():
    with open(file="inputs.txt", mode="r", encoding="utf-8") as f_twisted_treeline:
        twisted_treeline = f_twisted_treeline.readlines()
        f_twisted_treeline.close()
        dim_y = len(twisted_treeline)
        dim_x = len(twisted_treeline[0]-1)
        cartesian_treeline = np.empty((dim_y, dim_x) , type=np.uint8)
        cur_x = 0
        cur_y = 0
        bigboys_row = [dict() for x in range(dim_y)]
        bigboys_col = [dict() for x in range(dim_x)]
        for treeline in twisted_treeline:
            for tree in treeline.strip():
                t_h = int(tree)
                if t_h >= 5:
                    bigboys_row[cur_y][cur_x] = t_h
                    bigboys_col[cur_x][cur_y] = t_h
                cartesian_treeline[cur_y][cur_x] = t_h
                cur_x += 1
            cur_x = 0
            cur_y += 1
        # Icky math
        #print(bigboys_col)
        # The bidness
        visible_trees = 2*dim_y + 2*(dim_x-2)
        for cur_y in range(1,dim_y-1):
            for cur_x in range(1, dim_x-1):
                occluded_left = False
                occluded_right = False
                occluded_up = False
                occluded_down = False
                tree = cartesian_treeline[cur_y][cur_x]
                #print(f'{cur_x},{cur_y} height {tree}')
                for y_cord, val in bigboys_col[cur_x].keys():
                    if y_cord == cur_y:
                        continue
                    if y_cord < cur_y and val >= tree:
                        #print(f"Yes by {cur_x},{y_cord} above {val}")
                        occluded_up = True
                        break
                    if y_cord > cur_x and val >= tree:
                        #print(f'Yes by {cur_x},{y_cord} below {val}')
                        occluded_down = True
                        break
                for x_cord, val in bigboys_row[cur_y].items():
                    if x_cord == cur_x:
                        continue
                    if x_cord < cur_x and val >= tree:
                        #print(f'Yes by {x_cord},{cur_y} left {val}')
                        occluded_left = True
                        break
                    if x_cord > cur_x and val >= tree:
                        #print(f'Yes by {x_cord},{cur_y} right {val}')
                        occluded_right = True
                        break
                if not occluded_left:
                    #print("Slow Left")
                    for look_lx in range(cur_x-1, -1, -1):
                        if cartesian_treeline[cur_y][look_lx] >= tree:
                            occluded_left = True
                            break
                if not occluded_right:
                    #print("Slow Right")
                    for look_rx in range(cur_x+1, dim_x):
                        if cartesian_treeline[cur_y][look_rx] >= tree:
                            occluded_right = True
                            break                    
                if not occluded_up:
                    #print("Slow Up")
                    for look_uy in range(cur_y-1, -1, -1):
                        if cartesian_treeline[look_uy][cur_x] >= tree:
                            occluded_up = True
                            break
                if not occluded_down:
                    #print("Slow Down")
                    for look_dy in range(cur_y+1, dim_y):
                        if cartesian_treeline[look_dy][cur_x] >= tree:
                            occluded_down = True
                            break
                if not (occluded_down and occluded_up and occluded_left and occluded_right):
                    visible_trees += 1
                    #print("Not Occluded")
        print(visible_trees)


if __name__ == "__main__":
    t_start = perf_counter()
    main()
    t_end = perf_counter()
    print(f"Elapsed: {(t_end-t_start) * 1000} ms")
