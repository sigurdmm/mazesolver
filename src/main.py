import math
import sys
import heapq


class Node:
    def __init__(self, x = int, y = int, symbol = str):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.h = None
        self.g = None

    def set_h(self, h):
        self.h = h

    def is_goal_node(self):
        return True if self.symbol == 'B' else False

    def __str__(self):
        return str((self.x, self.y))


def file_loader(filename):
    try:
        f = open(filename)
    except IOError:
        print('Error loading ' + filename)
        raise
    with f:
        return f.read().splitlines()


def parse_file(file):
    nodes = []
    start_node = None
    goal_node = None

    x_value = 0
    y_value = 0

    # Generate nodes for each symbol in file
    for line in file:
        temp_array = []
        for symbol in line:
            node = Node(x_value, y_value, symbol)
            temp_array.append(node)
            if symbol == 'A':
                start_node = node
            elif symbol == 'B':
                goal_node = node
            x_value += 1
        nodes.append(temp_array)

        x_value = 0
        y_value += 1

    if start_node is None or goal_node is None:
        raise IOError('A start node and/or goal node wasn\'t detected')

    # Give all nodes an Manhattan Heuristic value
    assign_heuristics(nodes, goal_node)

    return nodes, start_node, goal_node


def assign_heuristics(nodes, goal_node):
    for line in nodes:
        for node in line:
            # If node is an impassable wall, set math.inf as a sentinel heuristic value
            if node.symbol == '#':
                node.set_h(math.inf)
            else:
                h = heuristics(node.x, node.y, goal_node)
                node.set_h(h)


# Generate manhattan heuristic from  coordinates of current node and goal node
def heuristics(x1, y1, goal_node):
    x2 = goal_node.x
    y2 = goal_node.y

    return abs(x1 - x2) + abs(y1 - y2)


# Prints table of the manhattan values
def h_string(filename):
    file = file_loader(filename)
    loaded_array, start, end = parse_file(file)
    for line in loaded_array:
        temp_str = ""
        for node in line:
            temp_str += str(node) + " "
        print(temp_str)

#h_string("board-1-1.txt")


def find_neighbours(nodes, node):
    neighbours = []
    if node.x >= len(nodes[0]) or node.x < 0:
        raise ValueError("The nodes x-value is outside of the matrix")
    if node.y >= len(nodes[0]) or node.y < 0:
        raise ValueError("The nodes y-value is outside of the matrix")
    if node.y > 0:
        # North node
         neighbours.append(nodes[node.y - 1][node.x])
    if node.x < len(nodes[0]) - 1:
        # East node
        neighbours.append(nodes[node.y][node.x + 1])
    if node.y < len(nodes) - 1:
        #South node
        neighbours.append(nodes[node.y + 1][node.x])
    if node.x > 0:
        #West node
        neighbours.append(nodes[node.y][node.x - 1])

    return neighbours


# Pseudo src from:
# http://mat.uab.cat/~alseda/MasterOpt/AStar-Algorithm.pdf
# https://www.redblobgames.com/pathfinding/a-star/introduction.html
def a_star(node_array, start, goal):
    open_set = set()
    closed_set = set()

    current = start
    open_set.add(current)

    #while len(open_set) > 0:


