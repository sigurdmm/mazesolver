import heapq
import math
from PIL import Image, ImageDraw

_wall_symbol = '#'
_start_symbol = 'A'
_goal_symbol = 'B'
_scale = 50
_circle_size = 20
_circle_color = (0,0,0)

# symbol : [cost, (R,G,B)]
_symbols = {
    "w" : [100, (0, 0, 255)],
    "m" : [50, (128, 128, 128)],
    "f" : [10, (11, 102, 35)],
    "g" : [5, (76, 187, 23)],
    "r" : [1, (155, 118, 83)],
    _wall_symbol : [1, (70, 70, 70)],
    "." : [1, (255, 255, 255)],
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
        self.game_type = None
        

    @staticmethod
    def file_loader(file_path):
        try:
            f = open(file_path)
        except IOError:
            print('Error loading ' + file_path)
            raise
        with f:
            return f.read().splitlines()

    def parse_file(self, file_path):
        loaded_file = self.file_loader(file_path)

        print(file_path.split('-'))

        if file_path.split('-')[1] == '1':
            self.game_type = 1
        elif file_path.split('-')[1] == '2':
            self.game_type = 2
        else:
            raise ValueError("Invalid filename. File cant be associated with a game mode")


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
        for line in self.maze:
            for node in line:
                node.h = self.heuristics(node, self.goal)

    # Generate manhattan heuristic from  coordinates of current node and goal node
    def heuristics(self, node):
        return abs(node.x - self.goal.x) + abs(node.y - self.goal.y)

    def get_neighbors(self, node):
        neighbors = []

        if node.x >= len(self.maze[0]) or node.x < 0:
            raise ValueError("The nodes x-value is outside of the matrix")
        if node.y >= len(self.maze[0]) or node.y < 0:
            raise ValueError("The nodes y-value is outside of the matrix")

        if node.y > 0 and not self.maze[node.y - 1][node.x].wall:
            # North
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
        to_node.g = from_node.g + _symbols[to_node.symbol][0]
        to_node.parent = from_node
        to_node.f = to_node.g + to_node.h

    def render_terminal(self):
        for row in self.maze:
            string = ""
            for node in row:
                if node.is_in_path:
                    string += '*'
                else:
                    string += node.symbol
            print(string)

    def render_graphics(self):

        img = Image.new('RGB', (len(self.maze[0])*_scale, len(self.maze)*_scale), "white")
        pixels = img.load()
        drawing = ImageDraw.Draw(img)
        for i, row in enumerate(self.maze):
            for j, node in enumerate(row):
                if node.symbol in _symbols:
                    color_code = self.get_node_color(node)
                    self.draw_node(pixels, i, j, color_code)
                else:
                    raise ValueError("Illegal symbol detected in file")
                if node.is_in_path:
                    self.draw_circles(drawing, i, j)
        img.show()

    @staticmethod
    def get_node_cost(node):
        return _symbols[node.symbol][0]

    @staticmethod
    def get_node_color(node):
        return _symbols[node.symbol][1]

    @staticmethod
    def draw_circles(drawing, i, j):
        padding = (_scale - _circle_size) / 2
        x1 = j * _scale + padding
        y1 = i * _scale + padding
        x2 = j * _scale + _scale + (1 - padding)
        y2 = i * _scale + _scale + (1 - padding)
        drawing.ellipse((x1, y1, x2, y2), _circle_color)


    @staticmethod
    def draw_node(pixels, i, j, color):
        for n in range(_scale):
            for m in range(_scale):
                pixels[_scale * j + n, _scale * i + m] = color

    def process(self):
        # Add start node to heap
        heapq.heappush(self.opened, (self.start.f, self.start))

        while len(self.opened):
            f, node = heapq.heappop(self.opened)
            self.closed.add(node)

            if node is self.goal:
                path = []
                p = node
                while p is not None:
                    p.is_in_path = True
                    path.append(p)
                    p = p.parent

                path.reverse()
                self.render_terminal()
                self.render_graphics()

            neighbors = self.get_neighbors(node)

            for neighbor in neighbors:
                if not neighbor.wall and neighbor not in self.closed:
                    if (neighbor.f, neighbor) in self.opened:
                        if neighbor.g > node.g + _symbols[neighbor.symbol][0]:
                            self.update_node(node, neighbor)
                    else:
                        self.update_node(node, neighbor)
                        heapq.heappush(self.opened, (neighbor.f, neighbor))


if __name__ == '__main__':
    a_star = AStar("static/board-2-2.txt")
    a_star.process()

    # http://mat.uab.cat/~alseda/MasterOpt/AStar-Algorithm.pdf
    # https://www.redblobgames.com/pathfinding/a-star/introduction.html
    # https://www.laurentluce.com/posts/solving-mazes-using-python-simple-recursivity-and-a-search/
