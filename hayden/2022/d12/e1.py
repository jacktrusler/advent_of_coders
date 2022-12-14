import random
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
        #print(f"Calculating Adjacent nodes to {node.grid_pos()}")
        if x >= 1:
            left_adj = self.node_at((x-1, y))
            if left_adj.elevation() - node.elevation() <= 1:
                node_adj.append(left_adj)
        if x < self.width:
            right_adj = self.node_at((x+1,y))
            if right_adj.elevation() - node.elevation() <= 1:
                node_adj.append(right_adj)
        if y >= 1:
            up_adj = self.node_at((x,y-1))
            if up_adj.elevation() - node.elevation() <= 1:
                node_adj.append(up_adj)
        if y < self.height:
            down_adj = self.node_at((x,y+1))
            if down_adj.elevation()- node.elevation() <= 1:
                node_adj.append(down_adj)
        return node_adj

    def node_at(self, node_coord):
        (x, y) = node_coord
        return self.grid[y][x]

    def manhattan(self, node1, node2):
        (x1, y1) = node1.grid_pos()
        (x2, y2) = node2.grid_pos()
        return abs(x2-x1) + abs(y2-y1)

def main():
    with open(file="inputs.txt", mode="r", encoding="utf-8") as f_elevation:
        elevations = f_elevation.readlines()
        (the_grid, start_node, end_node) = build_elevation_nodes(elevations)
        paths = breath_first_search(the_grid, start_node, end_node)
        paths = djikstra(the_grid, start_node, end_node)
        paths = jostar(the_grid, start_node, end_node)

def breath_first_search(the_grid, start_node, end_node):
    the_list = set()
    to_examine = queue.Queue()
    comes_from = dict()
    to_examine.put(start_node)
    the_list.add(start_node.grid_pos())
    steps = 1
    while not to_examine.empty():
        examine_node = to_examine.get()
        steps += 1
        if examine_node.grid_pos() == end_node.grid_pos():
            break
        #print(f"Visiting node {examine_node.grid_pos()}")
        adjacents = the_grid.get_adjacent(examine_node)
        for adjacency in adjacents:
            if adjacency.grid_pos() not in the_list:
                the_list.add(adjacency.grid_pos())
                to_examine.put(adjacency)
                comes_from[adjacency.grid_pos()] = examine_node
    cursor = end_node 
    path_back = []
    while cursor.grid_pos() != start_node.grid_pos(): 
        path_back.append(cursor.grid_pos())
        cursor = comes_from[cursor.grid_pos()]
    print(len(path_back), "in ", steps, " steps")

def djikstra(the_grid, start_node, end_node):
    the_list = set()
    to_examine = queue.PriorityQueue();
    comes_from = dict()
    steps = 1
    to_examine.put((0, random.random(), start_node))
    the_list.add(start_node.grid_pos())
    while not to_examine.empty():
        (cost, _,examine_node) = to_examine.get()
        steps += 1
        adjacents = the_grid.get_adjacent(examine_node)
        for adjacent in adjacents:
            if adjacent.grid_pos() not in the_list:
                the_list.add(adjacent.grid_pos())
                adj_cost = cost +1 
                to_examine.put((adj_cost, random.random(), adjacent))
                comes_from[adjacent.grid_pos()] = examine_node
    cursor = end_node 
    path_back = []
    while cursor.grid_pos() != start_node.grid_pos(): 
        path_back.append(cursor.grid_pos())
        cursor = comes_from[cursor.grid_pos()]
    print(len(path_back), "in ", steps, " steps")

def jostar(the_grid, start_node, end_node):
    the_list = set()
    to_examine = queue.PriorityQueue();
    comes_from = dict()
    steps = 1
    manhattan = the_grid.manhattan(start_node, end_node)
    to_examine.put((manhattan, random.random(), start_node))
    the_list.add(start_node.grid_pos())
    while not to_examine.empty():
        (cost , _, examine_node) = to_examine.get()
        steps += 1
        if examine_node.grid_pos() == end_node.grid_pos():
            break
        adjacents = the_grid.get_adjacent(examine_node)
        for adjacent in adjacents:
            if adjacent.grid_pos() not in the_list:
                the_list.add(adjacent.grid_pos())
                manhattan = the_grid.manhattan(adjacent, end_node)
                to_examine.put((manhattan + cost, random.random(), adjacent))
                comes_from[adjacent.grid_pos()] = examine_node
        cursor = end_node 
        path_back = []
    while cursor.grid_pos() != start_node.grid_pos(): 
        path_back.append(cursor.grid_pos())
        cursor = comes_from[cursor.grid_pos()]
    print(len(path_back), "in ", steps, " steps")



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
    #print(f"Elapsed: {(t_end-t_start) * 1000} ms")