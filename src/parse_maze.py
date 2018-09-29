from node import Node
from main import start_symbol, goal_symbol, wall_symbol
#import main

def file_loader(file_path):
    """
    :param str file_path: File path to open
    :return: List of each row with symbols of the file opened
    :rtype: list(list(str))
    :raises IOError: On exception from opening file at file_path

    """
    try:
        f = open(file_path)
    except IOError:
        print('Error loading ' + file_path)
        raise
    with f:
        return f.read().splitlines()

def parse_file(file_path):
    """
    :param str file_path: File path to the file containing the maze
    :return: A list containing a list of nodes for each row in maze
    :rtype: list(list(Node))
    :raises IOError: on start node and/or goal node not found in maze
    """
    loaded_file = file_loader(file_path)

    nodes = []

    x = 0
    y = 0
    start = None
    goal = None

    # Generate nodes for each symbol in file
    for line in loaded_file:
        maze_row = []
        for symbol in line:
            node = Node(x, y, symbol)
            maze_row.append(node)
            if symbol == start_symbol:
                start = node
            elif symbol == goal_symbol:
                goal = node
            elif symbol == wall_symbol:
                node.wall = True
            x += 1
        nodes.append(maze_row)
        x = 0
        y += 1

    if start is None or goal is None:
        raise IOError('A start node and/or goal node wasn\'t detected')

    return nodes, start, goal