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
    nar1.set_animal_goal(ag)
    # NonAnimalRobot2
    nar2.set_maze(hm)
    nar2.set_animal_robot(ar)
    nar2.set_platform_robot(nar1)
    nar2.set_animal_goal(ag)
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
    # get the position of the animal
    # based on this assign the robot classes (for animal and nonanimal robots)
    # get the positions to the new platform positions
    # get the path to the new platform positions (haven't made function for making sure oppsoite paths)
    # timing???
    # send paths to robots
    # check if animal robot it at goal

if __name__ == '__main__':
    main()