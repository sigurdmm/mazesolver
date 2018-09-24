import math
import heapq

_wall_symbol = '#'
_start_symbol = 'A'
_goal_symbol = 'B'


class Node:

    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.parent = None
        self.wall = False
        self.h = 0
        self.g = 0
        self.f = 0

    def __str__(self):
        return str((self.x, self.y))

    def __lt__(self, other):
        return self.f < other.f


class AStar(object):
    def __init__(self, file_path):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.start = None
        self.goal = None
        self.maze = []
        self.maze = self.parse_file(file_path)

    @staticmethod
    def file_loader(file_path):
        """
        :param file_path:the file path to the file of the maze
        :return: list of each row in the maze
        """
        try:
            f = open(file_path)
        except IOError:
            print('Error loading ' + file_path)
            raise
        with f:
            return f.read().splitlines()

    def parse_file(self, file_path):
        loaded_file = self.file_loader(file_path)

        nodes = []

        x = 0
        y = 0

        # Generate nodes for each symbol in file
        for line in loaded_file:
            maze_row = []
            for symbol in line:
                node = Node(x, y, symbol)
                maze_row.append(node)
                if symbol == 'A':
                    self.start = node
                elif symbol == 'B':
                    self.goal = node
                x += 1
            nodes.append(maze_row)
            x = 0
            y += 1

        if self.start is None or self.goal is None:
            raise IOError('A start node and/or goal node wasn\'t detected')

        # Give all nodes an Manhattan Heuristic value
        self.assign_heuristics()

        return nodes

    def assign_heuristics(self):
        for line in self.maze:
            for node in line:
                # If node is an impassable wall, set math.inf as a sentinel heuristic value
                if node == '#':
                    node.wall = True
                else:
                    node.h = self.heuristics(node, self.goal)

    # Generate manhattan heuristic from  coordinates of current node and goal node
    def heuristics(self, node):
        return abs(node.x - self.goal.x) + abs(node.y - self.goal.y)

    # Prints table of the manhattan values
    def print_h_maze(self, file_path):
        loaded_file = self.file_loader(file_path)
        loaded_array, start, end = self.parse_file(loaded_file)
        for line in loaded_array:
            temp_str = ""
            for node in line:
                temp_str += str(node) + " "
            print(temp_str)

    def get_neighbors(self, node):
        neighbors = []

        if node.x >= len(self.maze[0]) or node.x < 0:
            raise ValueError("The nodes x-value is outside of the matrix")
        if node.y >= len(self.maze[0]) or node.y < 0:
            raise ValueError("The nodes y-value is outside of the matrix")

        if node.y > 0:
            # North
            neighbors.append(self.maze[node.y - 1][node.x])
        if node.x < len(self.maze[0]) - 1:
            # East node
            neighbors.append(self.maze[node.y][node.x + 1])
        if node.y < len(self.maze) - 1:
            #South node
            neighbors.append(self.maze[node.y + 1][node.x])
        if node.x > 0:
            #West node
            neighbors.append(self.maze[node.y][node.x - 1])

    # Set or update heuristic value of each neighbor node
    # for neighbor in neighbors:
    #    update_g(node, neighbor)
        return neighbors

    @staticmethod
    def update_node(from_node, to_node):
        to_node.g = from_node.g + 1
        to_node.parent = from_node
        to_node.f = to_node.g + to_node.h
        # print_h_maze("static/board-1-1.txt")

    def process(self):
        # Add start node to heap
        heapq.heappush(self.opened, (self.start.f, self.start))

        while len(self.opened):
            f, node = heapq.heappop(self.opened)
            print(node)
            self.closed.add(node)

            if node is self.goal:
                print('GOOOOOAL, A STAR COMING HOME...')
                break

            neighbors = self.get_neighbors(node)

            for neighbor in neighbors:
                if neighbor is not neighbor.wall and neighbor not in self.closed:
                    if (neighbor.f, neighbor) in self.opened:
                        if neighbor.g > node.g + 1:
                            self.update_node(node, neighbor)
                    else:
                        self.update_node(node, neighbor)
                        heapq.heappush(self.opened, (neighbor.f, neighbor))

a_star = AStar("static/board-1-1.txt")
a_star.process()

    # http://mat.uab.cat/~alseda/MasterOpt/AStar-Algorithm.pdf
    # https://www.redblobgames.com/pathfinding/a-star/introduction.html
    # https://www.laurentluce.com/posts/solving-mazes-using-python-simple-recursivity-and-a-search/
