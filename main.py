'''Main Maze program that will move the robots around'''

from robot import *
from maze import *
from animal import *

# instantiate robots
robot1 = MazeRobot(0,0,0,'x')
robot2 = MazeRobot(0,-1,1,'x')
robot3 = MazeRobot(-1,0,1,'x')
mouse = Animal(robot1)
# instantiate maze
hm = HexagonMaze
# instantiate goal

# setting the parameters
# set maze
robot1.set_maze(hm)
robot2.set_maze(hm)
robot3.set_maze(hm)
# set animal robot
robot2.set_animal_robot(robot1)
robot3.set_animal_robot(robot1)
#

def main():
    print(
        robot2.move_to_outer_ring())
    pass

if __name__ == '__main__':
    main()