import os
import astar

#Global variables for changing layout and preferences
wall_symbol = '#'
start_symbol = 'A'
goal_symbol = 'B'

# Dictionary storing what cost symbols maps to and which color they are to be rendered in
# {symbol : [cost, (R,G,B)]}
symbols = {
    "w" : [100, (0, 0, 255)],
    "m" : [50, (128, 128, 128)],
    "f" : [10, (11, 102, 35)],
    "g" : [5, (76, 187, 23)],
    "r" : [1, (155, 118, 83)],
    wall_symbol : [1, (70, 70, 70)],
    "." : [1, (255, 255, 255)],
    " " : [1, (255, 255, 255)],
    start_symbol : [1, (0, 255, 0)],
    goal_symbol : [1, (255, 0, 0)],
}


if __name__ == '__main__':
    """
    Executing the program
    """

    maze_files = os.listdir(os.getcwd() + '/mazes')
    # For each file in mazes/ solve maze
    if maze_files:
        for filename in maze_files:
            if filename.endswith('.txt'):
                a_star = astar.AStar('mazes/' + filename)
                a_star.process()
    else:
        print("No mazes found in the directory mazesolver/mazes/")

    print("All files rendered successfully")