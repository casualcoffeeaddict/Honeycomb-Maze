# imports
from honeycomb_maze.animal import *
from honeycomb_maze.maze import *
from honeycomb_maze.robot import *

# Start Logging
# logging.basicConfig(filename='../logs/maze.log', encoding='utf-8')

# INSTANTIATE OBJECTS
# Instantiate maze
hm = HexagonMaze(column_number=13, row_number=15)
# Instantiate robots
execute = False
robot1 = PlatformRobot(7, 3, -10, 2, '192.168.0.101', execute, 'robot1')
robot2 = PlatformRobot(6, 3, -9, 0, '192.168.0.103', execute, 'robot2')
robot3 = PlatformRobot(6, 4, -10, 1, '192.168.0.106', execute, 'robot3')

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
    # robot1.ssh_connect(True, '192.168.0.101')
    robot1.coordinate_callibration([0, 0, 0])

    # robot1.execute_command('1 1')
    # robot2.is_animal_robot = 'NAR'
    # print(robot1.direction)
    # robot1.step_back_from_NAR(True)
    # print(robot1.direction)
    pass

def test():
    robot1.is_animal_robot = 'NAR'
    print(robot2.position_vector, robot2.direction)
    robot2.step_back_from_NAR(False)
    print(robot2.position_vector, robot2.direction)


if __name__ == "__main__":
    test()
