import heapq
from render import render_graphics
from parse_maze import parse_file
from main import symbols

class AStar(object):

    def __init__(self, file_path):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()

        self.maze, self.start, self.goal = parse_file(file_path)
        self.assign_heuristics()
        self.file_path = file_path
        self.symbols = symbols


    def assign_heuristics(self):
        """
        Iterates through each node of self.maze and assigns node.h value
        """
        for line in self.maze:
            for node in line:
                node.h = self.heuristics(node)

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


        if node.y > 0:
            # North node
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

        neighbors = self.remove_walls(neighbors)

        return neighbors

    @staticmethod
    def remove_walls(neighbors: list):
        return [node for node in neighbors if not node.wall]

    def update_node(self, from_node, to_node):
        """
        Updates g, f of to_node and sets from_node as to_nodes parent
        :param Node from_node: Parent node
        :param Node to_node: Node to be updated
        """
        to_node.g = from_node.g + self.symbols[to_node.symbol][0]
        to_node.parent = from_node
        to_node.f = to_node.g + to_node.h

    def get_node_cost(self, node):
        """
        :param Node node: node which cost is to be returned
        :return: returns cost of moving past this node. i.e. more costly to move across water than road
        :rtype: int
        """
        return self.symbols[node.symbol][0]


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

                render_graphics(self)

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
