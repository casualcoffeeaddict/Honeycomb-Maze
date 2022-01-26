"""Main Maze program that will move the robots around"""

from robot import *
from maze import *
from animal import *

# instantiate objects from classes
robot1 = MazeRobot(0, 0, 0, 'x', 'robot1')  # instantiate robot1
robot2 = MazeRobot(-1, 1, 0, 'x', 'robot2')  # instantiate robot2
robot3 = MazeRobot(-1, 0, 1, 'x', 'robot3')  # instantiate robot3
mouse = Animal(robot1, 'mouse')  # instantiate animal with the platform it is on
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


def main_loop():
    # animal is on platform - done in instantiation
    # platform moves to new position
    # non-animal robots move to platforms so the mouse can choose where to do
    # path finding occurs

    # animal makes choice
    # the animal class and non-animal classes are reassigned
    # the
    pass


def main():
    robot2.update_relative_position()
    print(
        # robot2.relative_position,
        # robot2.animal_robot.position_vector,
        # robot2.relative_position,
        # robot2.animal_robot.position_vector[1],
        robot2.get_path(),  # or animal choice 2 - how will this decision be made?
        # mouse.change_animal_platform(mouse.makes_random_choice())

    )
    pass


if __name__ == '__main__':
    main()
