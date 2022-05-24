"""
Robots positioned in a triangle
"""

# imports
from honeycomb_maze.animal import *
from honeycomb_maze.maze import *
from honeycomb_maze.robot import *

# Start Logging
logging.basicConfig(filename='../logs/maze.log', encoding='utf-8')

# INSTANTIATE OBJECTS
# Instantiate maze
hm = HexagonMaze(column_number=13, row_number=15)
# Instantiate robots
execute = False
robot1 = PlatformRobot(7, 3, -10, 2, '192.168.0.101', execute, 'robot1')
robot2 = PlatformRobot(6, 3, -9, 0, '192.168.0.103', execute, 'robot2')
robot3 = PlatformRobot(6, 4, -10, 1, '192.168.0.106', execute, 'robot3')

# Instantiate animal with its maze
mouse = Animal(hm, 'mouse')

# Set the maze (and add robots to maze class)
robot1.set_maze(hm)
robot2.set_maze(hm)
robot3.set_maze(hm)

mouse.set_maze(hm)

# Set initial animal robot - this can be automated
robot2.set_animal_robot(True)
mouse.set_animal_position()


def functional_main(execute=False, manual=False):
    # Starting Status of the Maze
    hm.get_status()
    # Animal Makes Movement Choice
    animal_choice_class = mouse.make_user_choice()
    # Change the robot classes based on the choice
    mouse.change_animal_class(animal_choice_class)
    mouse.set_animal_position()

    hm.get_status()
    pause()

    # Method for setting target and parhfinding targets for the robots
    nnar = hm.get_non_non_animal_robot_class()
    nar = hm.get_non_animal_robot_class()

    # Set the Pathfinding Targets
    nnar.set_pathfinding_target_position(manual)

    nar.set_pathfinding_target_position(manual)

    hm.get_status()
    pause()

    # NNAR step back from NAR
    nnar.move_to_animal_outer_ring(execute)
    # NNAR pathfinds to pathfinding target
    nnar.set_command_list()
    nnar.execute_command_list(execute)
    hm.get_status()
    pause()

    # NAR step back from AR
    nar.move_to_animal_outer_ring(execute)
    # NAR pathfinds to pathfinding target
    nar.set_command_list()
    nar.execute_command_list(execute)

    hm.get_status()
    pause()
    # Both non animal robots move to the inner ring
    nar.move_to_inner_ring_animal()
    nnar.move_to_inner_ring_animal()

    nar.execute_command_list(execute)
    nnar.execute_command_list(execute)
    pass


if __name__ == '__main__':
    functional_main()
    pass
