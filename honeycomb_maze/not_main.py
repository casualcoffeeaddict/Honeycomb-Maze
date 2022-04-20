# imports
from animal import *
from maze import *
from robot import *
from static_methods import *


# Start Logging
logging.basicConfig(filename='logs/maze.log', encoding='utf-8')

# INSTANTIATE OBJECTS
# Instantiate maze
hm = HexagonMaze(column_number=13 , row_number=15)
# Instantiate robots
robot1 = PlatformRobot(3, 5, -8, 1, '192.168.0.101', 'robot1')
robot2 = PlatformRobot(2, 5, -7, 1, '192.168.0.103', 'robot2')
robot3 = PlatformRobot(3, 4, -7, 1, '192.168.0.106', 'robot3')

# Instantiate animal with its maze
mouse = Animal(hm, 'mouse')

# Set the maze (and add robots to maze class)
robot1.set_maze(hm)
robot2.set_maze(hm)
robot3.set_maze(hm)

# Set initial animal robot - this should be automated
robot1.set_animal_robot(True)

mouse.set_maze(hm)


def main():
    robot2.is_animal_robot = 'NAR'
    print(robot1.direction)
    robot1.step_back_from_NAR(False)
    print(robot1.direction)
    pass

if __name__ == "__main__":
    main()