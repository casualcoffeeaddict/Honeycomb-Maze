# imports
from animal import *
from maze import *
from robot import *
from static_methods import *


# INSTANTIATE OBJECTS
# Instantiate maze
hm = HexagonMaze(column_number=15, row_number=15)
# Instantiate robots
robot1 = PlatformRobot(3, 5, -8, 3, '192.168.0.101', 'robot1')




def main():
    # robot1.step_back_from_NAR_execute()
    # robot1.execute_command('1 1')
    robot1.execute_command('0 0 0 2 1 5 1 1 1 0 1')
    pass

if __name__ == "__main__":
    main()