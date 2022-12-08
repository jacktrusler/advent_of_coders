def check_visible(column_index, row_index, trees):
    # look to the left and right, top and bottom of index to see if bigger tree exists, if no retrun True
    side_length = len(trees)
    tree_height = trees[column_index][row_index]
    # print(tree_height)
    # trees should be accessed by (y,x)

    above_blocked, below_blocked, left_blocked, right_blocked = False, False, False, False
    # check trees in row
    for x in range(side_length):
        # print(f'checking {column_index,row_index} against {column_index,x}. {tree_height} vs {trees[column_index][x]}')
        if (trees[column_index][x] >= tree_height):
            # invisible from this axis keep going
            # print('type: ',type(row_index), type(x), 'value: ',row_index,x)
            if (x > row_index):
                # print(f'right blocked because {trees[column_index][x]} > {tree_height}')
                right_blocked = True
            elif (x < row_index):
                # print(f'right blocked because {trees[column_index][x]} > {tree_height}')
                left_blocked = True

    # check trees in column
    for y in range(side_length):
        # print(f'checking {column_index,row_index} against {y,row_index}. {tree_height} vs {trees[y][row_index]}')
        if (trees[y][row_index] >= tree_height):
            # invisible from this axis keep going
            if (y > column_index):
                above_blocked = True
            elif (y < column_index):
                below_blocked = True

    if above_blocked and below_blocked and left_blocked and right_blocked:
        return False
    return True


def get_scenic_score(column_index, row_index, trees):
    column_length = len(trees)
    row_length = len(trees[0])
    tree_height = trees[column_index][row_index]
    # trees should be accessed by (y,x)

    above_trees_seen, below_trees_seen, left_trees_seen, right_trees_seen = 0, 0, 0, 0
    trees_to_right = row_length - row_index - 1
    trees_to_left = row_length - trees_to_right - 1

    trees_below = column_length - column_index - 1
    trees_above = column_length - trees_below - 1

    # check trees going to the left
    for x in range(trees_to_left):
        compare_row_index = row_index - (x + 1)

        if (trees[column_index][compare_row_index] < tree_height):
            left_trees_seen = left_trees_seen + 1
        if (trees[column_index][compare_row_index] >= tree_height):
            left_trees_seen = left_trees_seen + 1
            break

    for x in range(trees_to_right):
        compare_row_index = row_index + (x + 1)

        if (trees[column_index][compare_row_index] < tree_height):
            right_trees_seen = right_trees_seen + 1
        if (trees[column_index][compare_row_index] >= tree_height):
            right_trees_seen = right_trees_seen + 1
            break

    # check trees going up
    for y in range(trees_above):
        compare_column_index = column_index - (y + 1)
        if (trees[compare_column_index][row_index] < tree_height):
            above_trees_seen = above_trees_seen + 1
        if (trees[compare_column_index][row_index] >= tree_height):
            above_trees_seen = above_trees_seen + 1
            break

    # check trees going down
    for y in range(trees_below):
        compare_column_index = column_index + (y + 1)
        if (trees[compare_column_index][row_index] < tree_height):
            below_trees_seen = below_trees_seen + 1
        if (trees[compare_column_index][row_index] >= tree_height):
            below_trees_seen = below_trees_seen + 1
            break

    return above_trees_seen * below_trees_seen * left_trees_seen * right_trees_seen


def part_1(input_file):
    with open(input_file) as f:
        lines = [line for line in f]
        trees = []
        # populate treeline
        for line in lines:
            line = line.strip()
            treeline = []
            for tree in line:
                treeline.append(int(tree))
            trees.append(treeline)

        # fill in if each tree is visible
        visible_trees = []
        visible_count = 0
        for column_index, treeline in enumerate(trees):
            visible_treeline = []
            for row_index, tree in enumerate(treeline):
                visible = check_visible(column_index, row_index, trees)
                if (visible):
                    visible_count = visible_count + 1
                visible_treeline.append(visible)
            visible_trees.append(visible_treeline)

        # print trees and visible values
        # for treeline in trees:
        #     print(treeline)
        # print()
        # for visibleline in visible_trees:
        #     print(visibleline)

    return visible_count


def part_2(input_file):
    with open(input_file) as f:
        lines = [line for line in f]
        trees = []
        # populate treeline
        for line in lines:
            line = line.strip()
            treeline = []
            for tree in line:
                treeline.append(int(tree))
            trees.append(treeline)

        # fill in if each tree is visible
        max_scenic_score = 0
        for column_index, treeline in enumerate(trees):
            for row_index, tree in enumerate(treeline):
                scenic_score = get_scenic_score(column_index, row_index, trees)
                if scenic_score > max_scenic_score:
                    max_scenic_score = scenic_score

    return max_scenic_score


if __name__ == '__main__':
    print('part 1 answer: ', part_1('input.txt'))
    print('part 2 answer: ', part_2('input.txt'))
