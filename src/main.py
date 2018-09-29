import heapq
from PIL import Image, ImageDraw
import os

#Global variables for changing layout and preferences
_wall_symbol = '#'
_start_symbol = 'A'
_goal_symbol = 'B'
_scale = 50
_circle_size = 20
_circle_color = (0,0,0)

# Dictionary storing what cost symbols maps to and which color they are to be rendered in
# {symbol : [cost, (R,G,B)]}
_symbols = {
    "w" : [100, (0, 0, 255)],
    "m" : [50, (128, 128, 128)],
    "f" : [10, (11, 102, 35)],
    "g" : [5, (76, 187, 23)],
    "r" : [1, (155, 118, 83)],
    _wall_symbol : [1, (70, 70, 70)],
    "." : [1, (255, 255, 255)],
    " " : [1, (255, 255, 255)],
    _start_symbol : [1, (0, 255, 0)],
    _goal_symbol : [1, (255, 0, 0)],
}

class Node:

    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.parent = None
        self.wall = False
        self.is_in_path = False
        self.h = 0
        self.g = 0
        self.f = 0
        self.task_type = None

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
        self.file_path = file_path


    @staticmethod
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

    def parse_file(self, file_path: str):
        """
        :param str file_path: File path to the file containing the maze
        :return: A list containing a list of nodes for each row in maze
        :rtype: list(list(Node))
        :raises IOError: on start node and/or goal node not found in maze
        """
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
                if symbol == _start_symbol:
                    self.start = node
                elif symbol == _goal_symbol:
                    self.goal = node
                elif symbol == _wall_symbol:
                    node.wall = True
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
        """
        Iterates through each node of self.maze and assigns node.h value
        """
        for line in self.maze:
            for node in line:
                node.h = self.heuristics(node, self.goal)

    # Generate manhattan heuristic from  coordinates of current node and goal node
    def heuristics(self, node):
        """
        :param Node node: Node which is to be calculated heuristic values for
        :return: Manhattan heuristic value of node
        :rtype: int
        """
        return abs(node.x - self.goal.x) + abs(node.y - self.goal.y)

    def get_neighbors(self, node):
        """
        :param Node node: Node whose neighbors is to be found
        :return: List of nodes that are adjacent(neighbors) to the param node
        :rtype: list(Node)
        """

        neighbors = []

        if node.x >= len(self.maze[0]) or node.x < 0:
            raise ValueError("The nodes x-value is outside of the matrix")
        if node.y >= len(self.maze[0]) or node.y < 0:
            raise ValueError("The nodes y-value is outside of the matrix")

        if node.y > 0 and not self.maze[node.y - 1][node.x].wall:
            # North node
            neighbors.append(self.maze[node.y - 1][node.x])
        if node.x < len(self.maze[0]) - 1 and not self.maze[node.y][node.x + 1].wall:
            # East node
            neighbors.append(self.maze[node.y][node.x + 1])
        if node.y < len(self.maze) - 1 and not self.maze[node.y + 1][node.x].wall:
            #South node
            neighbors.append(self.maze[node.y + 1][node.x])
        if node.x > 0 and not self.maze[node.y][node.x - 1].wall:
            #West node
            neighbors.append(self.maze[node.y][node.x - 1])

        return neighbors

    @staticmethod
    def update_node(from_node, to_node):
        """
        Updates g, f of to_node and sets from_node as to_nodes parent
        :param Node from_node: Parent node
        :param Node to_node: Node to be updated
        """
        to_node.g = from_node.g + _symbols[to_node.symbol][0]
        to_node.parent = from_node
        to_node.f = to_node.g + to_node.h

    def render_graphics(self):
        """ Renders the maze with shortest solution graphically
        :raises: ValueError: on symbols which can't be determined because it's not in _symbols
        """
        img = Image.new('RGB', (len(self.maze[0])*_scale, len(self.maze)*_scale), "white")
        pixels = img.load()
        drawing = ImageDraw.Draw(img)

        # enumerate through each node of self.maze
        for i, row in enumerate(self.maze):
            for j, node in enumerate(row):
                if node.symbol in _symbols:
                    color_code = self.get_node_color(node)
                    self.draw_node(pixels, i, j, color_code)
                else:
                    raise ValueError("Illegal symbol detected in file")
                # Draw circles on nodes that are in the solution path
                if node.is_in_path:
                    self.draw_circles(drawing, i, j)
        img.save(f'./solved_mazes/{self.file_path.replace("mazes/", "").replace(".txt", ".png")}')

    @staticmethod
    def get_node_cost(node):
        """
        :param Node node: node which cost is to be returned
        :return: returns cost of moving past this node. i.e. more costly to move across water than road
        :rtype: int
        """
        return _symbols[node.symbol][0]

    @staticmethod
    def get_node_color(node):
        """
        Find what color is to be rendered for given node
        :param Node node: Node which is to be rendered
        :return: RGB color code for node
        :rtype: int
        """
        return _symbols[node.symbol][1]

    @staticmethod
    def draw_circles(drawing, y, x):
        """
        Draw circles on given positions of given a Drawing object
        :param Drawing drawing: PIL.ImageDraw.Draw
        :param int y: y value of node when maze is scaled to be 1px for each node.
        :param int x: x value of node when maze is scaled to be 1px for each node.
        """
        padding = (_scale - _circle_size) / 2
        x1 = x * _scale + padding
        y1 = y * _scale + padding
        x2 = x * _scale + _scale + (1 - padding)
        y2 = y * _scale + _scale + (1 - padding)
        drawing.ellipse((x1, y1, x2, y2), _circle_color)


    @staticmethod
    def draw_node(pixels, y, x, color):
        """
        Iterate through range of pixels and color them in a given color
        :param PIL.Image.Pixels pixels: pixel schema
        :param y: y value of node when maze is scaled to be 1px for each node.
        :param x: x value of node when maze is scaled to be 1px for each node.
        :param (int,int,int) color: RGB color code to paint given pixels with
        """
        for n in range(_scale):
            for m in range(_scale):
                pixels[_scale * x + n, _scale * y + m] = color

    @staticmethod
    def trace_shortest_path(node):
        """
        :param Node node: The goal node of the maze
        :return: returns an ordered list of the nodes in the optimal path through maze
        :rtype: list(Node)
        """
        path = []
        p = node
        # Trace back path
        while p is not None:
            p.is_in_path = True
            path.append(p)
            p = p.parent
        path.reverse()

        return path

    def process(self):
        """
        The "engine" running the a star algorithm
        """
        # Add start node to heap
        heapq.heappush(self.opened, (self.start.f, self.start))

        # While there are nodes in opened
        while len(self.opened):
            f, node = heapq.heappop(self.opened)
            self.closed.add(node)

            # If node is the goal node
            if node is self.goal:
                self.trace_shortest_path(node)
                print("Rendering " + self.file_path.split('/')[-1])
                self.render_graphics()

            neighbors = self.get_neighbors(node)

            for neighbor in neighbors:
                # If node is not visited or a wall
                if not neighbor.wall and neighbor not in self.closed:
                    # If node is already opened, but not visited
                    if (neighbor.f, neighbor) in self.opened:
                        # If this path to neighbor is shorter than previously found
                        if neighbor.g > node.g + self.get_node_cost(node):
                            #Update neighbor with node as parent and update f and g
                            self.update_node(node, neighbor)
                    # Node is not earlier visited
                    else:
                        # Give neighbor an f and g value and set node as parent
                        self.update_node(node, neighbor)
                        heapq.heappush(self.opened, (neighbor.f, neighbor))


if __name__ == '__main__':
    """
    Executing the program
    """

    maze_files = os.listdir(os.getcwd() + '/mazes')
    # For each file in mazes/ solve maze
    if maze_files:
        for filename in maze_files:
            if filename.endswith('.txt'):
                a_star = AStar('mazes/' + filename)
                a_star.process()
    else:
        print("No mazes found in the directory mazesolver/mazes/")

    print("All files rendered successfully")