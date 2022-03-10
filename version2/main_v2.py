from animal2 import *
from maze_v2 import *
from robot_v2 import *

# INSTANTIATE OBJECTS
# Instantiate maze
hm = HexagonMaze(column_number=15, row_number=15)
# Instantiate robots
robot1 = PlatformRobot(3, 5, -8, 1, 'robot1')
robot2 = PlatformRobot(2, 5, -7, 2, 'robot2')
robot3 = PlatformRobot(3, 4, -7, 1, 'robot3')

# Instantiate animal with its maze
mouse = Animal(hm, 'mouse')

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


def functional_main():
    # changes which animal is the correct animal class
    animal_choice = mouse.make_random_movement_choice()
    mouse.change_animal_class()

    pass


def main():
    # setting up which platform is which type for the path-finding
    robot1.is_animal_robot = 'AR'
    robot2.is_animal_robot = 'NNAR'
    robot3.is_animal_robot = 'NAR'

    # set the animal position one the animal robot is defined
    mouse.set_animal_position()

    hm.see_status()

    # method for setting the target and pathfinding target
    robot2.set_pathfinding_target_position()
    print('ROBOT2:', robot2.target_position, robot2.pathfinding_target_position)

    # non non animal robot step back from non animal robot (NAR)
    print('POSITION_VECTOR (robot2):', robot2.position_vector)
    robot2.step_back_from_NAR()  # step back command needs to added??
    print('POSITION_VECTOR (robot2):', robot2.position_vector)

    # pathfinding method
    path = hm.pathfinder(robot2)
    print(path)
    # make command list
    command_list = robot2.make_command_list(path)
    robot2.set_command_list(command_list)
    print('Command List', command_list)

    # method for setting the target and pathfinding target
    robot3.set_pathfinding_target_position()
    print('ROBOT3:', robot3.target_position, robot3.pathfinding_target_position)

    # NAR step to outer ring of AR
    print('POSITION_VECTOR (robot3):', robot3.position_vector)
    robot3.move_to_animal_outer_ring()
    print('POSITION_VECTOR (robot3):', robot3.position_vector)

    # pathfinding method
    path = hm.pathfinder(robot3)
    print(path)
    # make command list
    command_list = robot3.make_command_list(path)
    robot3.set_command_list(command_list)
    print('Command List', command_list)

    # method for stepping into the inner ring
    print('POSITION_VECTOR (robot2):', robot2.position_vector)
    print('POSITION_VECTOR (robot3):', robot3.position_vector)

    robot2.move_to_inner_ring(robot1)
    robot3.move_to_inner_ring(robot1)

    print('POSITION_VECTOR (robot2):', robot2.position_vector)
    print('POSITION_VECTOR (robot3):', robot3.position_vector)

# move = hm.pathfinder_loop_1(robot2),
# print(move)


if __name__ == '__main__':
    main()
