from PIL import Image, ImageDraw

_scale = 50
_circle_size = 20
_circle_color = (0,0,0)

def render_graphics(astar):
    """ Renders the maze with shortest solution graphically
    :raises: ValueError: on symbols which can't be determined because it's not in _symbols
    """
    img = Image.new('RGB', (len(astar.maze[0]) * _scale, len(astar.maze) * _scale), "white")
    drawing = ImageDraw.Draw(img)

    # enumerate through each node of self.maze
    for row in astar.maze:
        for node in row:
            if node.symbol in astar.symbols:
                color = get_node_color(node, astar.symbols)
                draw_node(drawing, node, color)
            else:
                raise ValueError("Illegal symbol detected in file")
            # Draw circles on nodes that are in the solution path
    img.save(f'./solved_mazes/{astar.file_path.replace("mazes/", "").replace(".txt", ".png")}')

def get_node_color(node, symbols):
    """
    Find what color is to be rendered for given node
    :param Node node: Node which is to be rendered
    :return: RGB color code for node
    :rtype: int
    """
    return symbols[node.symbol][1]

def draw_circles(drawing, y, x):
    """
    Draw circles on given positions of given a Drawing object
    :param Drawing drawing: PIL.ImageDraw.Draw
    :param int y: y value of node when maze is scaled to be 1px for each node.
    :param int x: x value of node when maze is scaled to be 1px for each node.
    """
    padding = (_scale - _circle_size) / 2
    x1 = x + padding
    y1 = y + padding
    x2 = x + _scale + (1 - padding)
    y2 = y + _scale + (1 - padding)
    drawing.ellipse((x1, y1, x2, y2), _circle_color)

def draw_node(drawing, node, color):
    """
    Iterate through range of pixels and color them in a given color
    :param PIL.Image.Pixels pixels: pixel schema
    :param y: y value of node when maze is scaled to be 1px for each node.
    :param x: x value of node when maze is scaled to be 1px for each node.
    :param (int,int,int) color: RGB color code to paint given pixels with
    """
    x = node.x * _scale
    y = node.y * _scale
    drawing.rectangle((x, y , x + _scale, y +_scale), color)

    if node.is_in_path:
        draw_circles(drawing, y, x)