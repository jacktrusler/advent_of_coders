"""Treetop Tree House"""


def main():
    with open(file="inputs.txt", mode="r", encoding="utf-8") as f_twisted_treeline:
        twisted_treeline = f_twisted_treeline.readlines()
        f_twisted_treeline.close()
        dim_y = len(twisted_treeline)
        dim_x = len(twisted_treeline[0].strip())
        cartesian_treeline = [[0 for x in range(dim_x)] for y in range(dim_y)]
        cur_x = 0
        cur_y = 0
        for treeline in twisted_treeline:
            for tree in treeline.strip():
                cartesian_treeline[cur_y][cur_x] = int(tree)
                cur_x += 1
            cur_x = 0
            cur_y += 1
        visible_trees = 2*dim_y + 2*(dim_x-2)
        for cur_y in range(1,dim_y-1):
            for cur_x in range(1, dim_x-1):
                occluded_left = False
                occluded_right = False
                occluded_up = False
                occluded_down = False
                tree = cartesian_treeline[cur_y][cur_x]
                for look_lx in range(cur_x-1, -1, -1):
                    if cartesian_treeline[cur_y][look_lx] >= tree:
                        occluded_left = True
                        break
                for look_rx in range(cur_x+1, dim_x):
                    if cartesian_treeline[cur_y][look_rx] >= tree:
                        occluded_right = True
                        break
                for look_uy in range(cur_y-1, -1, -1):
                    if cartesian_treeline[look_uy][cur_x] >= tree:
                        occluded_up = True
                        break
                for look_dy in range(cur_y+1, dim_y):
                    if cartesian_treeline[look_dy][cur_x] >= tree:
                        occluded_down = True
                        break
                if not (occluded_down and occluded_up and occluded_left and occluded_right):
                    visible_trees += 1
        print(visible_trees)


if __name__ == "__main__":
    main()