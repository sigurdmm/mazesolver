import unittest
from src.main import *


class FileLoadTests(unittest.TestCase):
    def test_non_existing_file_input(self):
        with self.assertRaises(IOError):
            file_loader("nonExistingFileName")



class NodeTests(unittest.TestCase):

    def test_if_goal_node(self):
        node = Node(1,2,'B')
        assert node.is_goal_node()

    # def test_init_node_without_args(self):
    #     with self.assertRaises(TypeError):
    #         node = Node()

class AStarTests(unittest.TestCase):
    node_1 = Node(0, 0, '.')
    node_2 = Node(1, 0, '#')
    node_3 = Node(2, 0, 'A')
    node_4 = Node(0, 1, '.')
    node_5 = Node(1, 1, '.')
    node_6 = Node(2, 1, '#')
    node_7 = Node(0, 2, '.')
    node_8 = Node(1, 2, 'B')
    node_9 = Node(2, 2, '.')

    node_outside_x = Node(3, 1, '.')
    node_outside_y = Node(1, 3, '.')

    nodes = [[node_1, node_2, node_3],
             [node_4, node_5, node_6],
             [node_7, node_8, node_9]]

    def test_find_neighbours(self):
        assert find_neighbours(self.nodes, self.node_5) == \
               [self.node_2, self.node_6, self.node_8, self.node_4]
        assert find_neighbours(self.nodes, self.node_1) == [self.node_2, self.node_4]
        assert find_neighbours(self.nodes, self.node_9) == [self.node_6, self.node_8]
        with self.assertRaises(ValueError):
            find_neighbours(self.nodes, self.node_outside_x)
        with self.assertRaises(ValueError):
            find_neighbours(self.nodes, self.node_outside_y)

if __name__ == '__main__':
    unittest.main()