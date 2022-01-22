'''Main Maze program that will move the robots around'''

from robot import *
from maze import *
from animal import *

# instantiate objects from classes
robot1 = MazeRobot(0,0,0,'x') # instantiate robot1
robot2 = MazeRobot(0,-1,1,'x') # instantiate robot2
robot3 = MazeRobot(-1,0,1,'x') # instantiate robot3
mouse = Animal(robot1) # instantiate animal
goal = AnimalGoal(2,0,-2, 'x') # instantiate animal goal
# instantiate maze
hm = HexagonMaze(11, 10)
# instantiate goal

# setting the parameters
# set maze
robot1.set_maze(hm)
robot2.set_maze(hm)
robot3.set_maze(hm)
# set animal robot
robot2.set_animal_robot(robot1)
robot3.set_animal_robot(robot1)
mouse.set_animal_goal(goal)
#

def main():
    print(
        robot2.move_to_outer_ring())
    pass

if __name__ == '__main__':
    main()