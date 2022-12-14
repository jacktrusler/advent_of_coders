from time import perf_counter
import numpy as np
import queue
class node:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def grid_pos(self):
        return (self.x,self.y)
    def elevation(self):
        return self.z

class grid:
    def __init__(self, grid):
        self.grid = grid
        self.width = len(grid[0])-1
        self.height = len(grid)-1
    
    def get_adjacent(self, node):
        (x, y) = node.grid_pos()
        node_adj = []
        if x >= 1:
            left_adj = self.node_at((x-1, y))
            if node.elevation() - left_adj.elevation() <= 1:
                node_adj.append(left_adj)
        if x < self.width:
            right_adj = self.node_at((x+1,y))
            if node.elevation() - right_adj.elevation() <= 1:
                node_adj.append(right_adj)
        if y >= 1:
            up_adj = self.node_at((x,y-1))
            if node.elevation() - up_adj.elevation() <= 1:
                node_adj.append(up_adj)
        if y < self.height:
            down_adj = self.node_at((x,y+1))
            if node.elevation() - down_adj.elevation() <= 1:
                node_adj.append(down_adj)
        return node_adj

    def node_at(self, node_coord):
        (x, y) = node_coord
        return self.grid[y][x]

def main():
    with open(file="inputs.txt", mode="r", encoding="utf-8") as f_elevation:
        elevations = f_elevation.readlines()
        (the_grid, start_node, end_node) = build_elevation_nodes(elevations)
        paths = breath_first_search(the_grid, start_node, end_node)

def breath_first_search(the_grid, start_node, end_node):
    the_list = set()
    to_examine = queue.Queue()
    comes_from = dict()
    to_examine.put(end_node)
    the_list.add(end_node.grid_pos())
    while not to_examine.empty():
        examine_node = to_examine.get()
        if examine_node.elevation() == 1:
            start_node = examine_node
            break
        adjacents = the_grid.get_adjacent(examine_node)
        for adjacency in adjacents:
            if adjacency.grid_pos() not in the_list:
                the_list.add(adjacency.grid_pos())
                to_examine.put(adjacency)
                comes_from[adjacency.grid_pos()] = examine_node
    cursor = start_node
    path_back = []
    while cursor.grid_pos() != end_node.grid_pos(): 
        path_back.append(cursor.grid_pos())
        cursor = comes_from[cursor.grid_pos()]
    print(len(path_back))

    
def build_elevation_nodes(elevations):
    elev_width = len(elevations[0])-1
    elev_height = len(elevations)
    start_node = None
    end_node = None
    elevation_nodes = np.empty([elev_height, elev_width], dtype=object)
    for y in range(len(elevations)):
        for x in range(elev_width):
            elevation = elevations[y][x]
            working_node = node(x=x, y=y, z=-1)
            if elevation == "S":
                start_node = working_node
                working_node.z = 1
            elif elevation == "E":
                end_node = working_node
                working_node.z = 26
            else:
                working_node.z = ord(elevation)-96
            elevation_nodes[y][x] = working_node
    the_grid = grid(elevation_nodes)
    return (the_grid, start_node, end_node)



if __name__ == "__main__":
    t_start = perf_counter()
    main()
    t_end = perf_counter()
    print(f"Elapsed: {(t_end-t_start) * 1000} ms")