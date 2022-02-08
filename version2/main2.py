from animal2 import *
from maze2 import *
from robot2 import *

# INSTANTIATE OBJECTS
# Instantiate maze
hm = HexagonMaze(column_number=15, row_number=15)
# Instantiate robots
robot1 = PlatformRobot(4, 6, -10, 1, 'robot1')
robot2 = PlatformRobot(3, 5, -8, 2, 'robot2')
robot3 = PlatformRobot(3, 6, -9, 1, 'robot3')

# Instantiate animal with its maze
mouse = Animal(hm)

# Set the maze (and add robots to maze class)
robot1.set_maze(hm)
robot2.set_maze(hm)
robot3.set_maze(hm)

# Set initial animal robot - this should be automated
robot1.set_animal_robot(True)

mouse.set_maze(hm)
mouse.set_animal_position()


def move_robot(maze, robot):
    maze.make_temp_movement_network()
    robot.set_target_position()
    maze.pathfinder(robot)


def loop(maze):
    for robot in maze.robot_list:
        if robot.is_animal_robot == 'NNAR':
            # move first
            pass
        if robot.is_animal_robot == 'NAR':
            move_robot(maze, robot)
        # pathfind
        pass
    pass


def flatten(t):
    return [item for sublist in t for item in sublist]


def main():
    robot3.is_animal_robot = 'NAR'
    robot2.target_position = (5, 6, -11)
    move = hm.pathfinder_loop_1(robot2)
    print(
        # hm.make_temp_movement_network(robot2),
        # robot2.set_target_position(),
        # hm.get_pathfinding_target(robot2)
        # hm.pathfinder(robot2)
        # move,
        # robot2.make_command_list(move)
        robot2.position_vector
        # hm.pathfinder_loop_2(robot2)
        # robot2.animal_relative_position(robot2.target_position)
    )


if __name__ == '__main__':
    main()
