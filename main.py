'''Main Maze program that will move the robots around'''

from robot_class import *

ag = AnimalGoal(0, 0, 0, 'x')
ar = AnimalRobot(0, 0, 0, 'x', ag)

def main():
    while ar.check_if_animal_at_goal() == True:
        pass

if __name__ == '__main__':
    main()