
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

    def __str__(self):
        return str((self.x, self.y))

    def __lt__(self, other):
        return self.f < other.f
