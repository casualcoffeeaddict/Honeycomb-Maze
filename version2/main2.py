from animal2 import *
from maze2 import *
from robot2 import *

# INSTANTIATE OBJECTS
# Instantiate maze
hm = HexagonMaze(column_number=15, row_number=15)
# Instantiate robots
robot1 = PlatformRobot(3, 5, -8, 1, 'robot1')
robot2 = PlatformRobot(2, 5, -7, 2, 'robot2')
robot3 = PlatformRobot(3, 4, -7, 1, 'robot3')

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
    robot2.target_position = (5, 4, -9)
    robot3.target_position = (4, 4, -8)

    # print(hm.get_animal_robot_class().position_vector)
    # print(hm.get_non_animal_robot_class().position_vector)
    # print(hm.get_non_non_animal_robot_class().position_vector)
    # print('1', robot2.position_vector)
    # robot2.step_back_from_NAR()
    # robot2.move_to_inner_ring(0)
    # print('2', robot2.position_vector)
    print(robot2.position_vector)
    # robot3.step_back_from_NAR()
    print(robot2.position_vector)
    path = hm.pathfinder(robot2)
    print(path)
    command_list = robot3.make_command_list(path)

    print(command_list)



# move = hm.pathfinder_loop_1(robot2),
# print(move)


if __name__ == '__main__':
    main()
