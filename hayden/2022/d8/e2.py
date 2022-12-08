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
        best_scenic = 0
        for cur_y in range(1,dim_y-1):
            for cur_x in range(1, dim_x-1):
                tree = cartesian_treeline[cur_y][cur_x]
                l_trees = 0
                r_trees = 0
                u_trees = 0
                d_trees = 0
                for look_lx in range(cur_x-1, -1, -1):
                    l_trees += 1
                    if cartesian_treeline[cur_y][look_lx] >= tree:
                        break
                for look_rx in range(cur_x+1, dim_x):
                    r_trees += 1
                    if cartesian_treeline[cur_y][look_rx] >= tree:
                        break
                for look_uy in range(cur_y-1, -1, -1):
                    u_trees += 1
                    if cartesian_treeline[look_uy][cur_x] >= tree:
                        break
                for look_dy in range(cur_y+1, dim_y):
                    d_trees += 1
                    if cartesian_treeline[look_dy][cur_x] >= tree:
                        break
                scenic_score = l_trees * r_trees * u_trees * d_trees
                if scenic_score > best_scenic:
                    best_scenic = scenic_score
        print(best_scenic)


if __name__ == "__main__":
    main()
