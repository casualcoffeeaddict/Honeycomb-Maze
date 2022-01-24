'''Main Maze program that will move the robots around'''

from robot import *
from maze import *
from animal import *

# instantiate objects from classes
robot1 = MazeRobot(0, 0, 0, 'x')  # instantiate robot1
robot2 = MazeRobot(-1, 1, 0, 'x')  # instantiate robot2
robot3 = MazeRobot(-1, 0, 1, 'x')  # instantiate robot3
mouse = Animal(robot1)  # instantiate animal with the platform it is on
goal = AnimalGoal(2, 0, -2, 'x')  # instantiate animal goal
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
# tell non animal robots about each other
robot2.set_non_animal_robot(robot3)
robot3.set_non_animal_robot(robot2)

# tell animal the which are the animal and non animal robots
mouse.set_animal_robot(robot1)
mouse.set_non_animal_robot_1(robot2)
mouse.set_non_animal_robot_2(robot3)


# animal is on platform
# non animal robots move to platforms so the mouse can choose where to do
# path finding occurs

# animal makes choice
# the animal class and non animal classes are reassigned
# the

def main():
    print(
        # mouse.see_mouse_status(),
        mouse.change_animal_platform(mouse.animal_makes_choice())

    )
    pass


if __name__ == '__main__':
    main()
