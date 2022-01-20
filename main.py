'''Main Maze program that will move the robots around'''

from robot import *
from maze import *

hm = HexagonMaze(10, 10)
ag = AnimalGoal(0, 0, 0, 'x')
ar = AnimalRobot(0, 0, 0, 'x')
nar1 = NonAnimalRobot()
nar2 = NonAnimalRobot()

def initialisation():
    # NonAnimalRobot 1
    nar1.set_maze(hm)
    nar1.set_animal_robot(ar)
    nar1.set_platform_robot(nar2)
    # NonAnimalRobot2
    nar2.set_maze(hm)
    nar2.set_animal_robot(ar)
    nar2.set_platform_robot(nar1)
    # AnimalRobot
    ar.set_maze_class(hm)
    ar.set_goal_platform_class(ag)
    # HexagonMaze
    hm.set_animal_robot(ar)
    hm.set_animal_goal(ag)
    hm.set_non_animal_robot_1(nar1)
    hm.set_non_animal_robot_2(nar2)

def main():
    initialisation()
    while ar.check_if_animal_at_goal() == True:

        pass

if __name__ == '__main__':
    main()