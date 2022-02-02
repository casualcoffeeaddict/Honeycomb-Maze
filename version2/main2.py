from animal2 import *
from maze2 import *
from robot2 import *

# INSTANTIATE OBJECTS
# Instantiate maze
hm = HexagonMaze(column_number=10, row_number=11)
# Instantiate robots
robot1 = PlatformRobot(4, 6, -10, 1, 'robot1')
robot2 = PlatformRobot(3, 5, -8, 1, 'robot2')
robot3 = PlatformRobot(3, 6, -9, 1, 'robot3')
# Instantiate animal
mouse = Animal()

# Set the maze (and add robots to maze class)
robot1.set_maze(hm)
robot2.set_maze(hm)
robot3.set_maze(hm)

mouse.set_maze(hm)




def main():
    print(hm.get_consecutive_positions())

if __name__ == '__main__':
    main()