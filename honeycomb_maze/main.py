# imports
from animal import *
from maze import *
from robot import *

# Start Logging
logging.basicConfig(filename='logs/maze.log', encoding='utf-8')

# INSTANTIATE OBJECTS
# Instantiate maze
hm = HexagonMaze(column_number=15, row_number=15)
# Instantiate robots
robot1 = PlatformRobot(3, 5, -8, 3, 'robot1')
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

def functional_main():
    hm.get_status()

    # changes which animal is the correct animal class
    animal_choice_class = mouse.make_user_choice()  # animal makes choice
    print('animal choice', animal_choice_class.name)
    # print(hm.get_animal_robot_class() == animal_choice_class)
    mouse.change_animal_class(animal_choice_class)  # animal moves to its choice

    hm.get_status()

    # set the animal position
    mouse.set_animal_position()  # change the position of the animal based on its movement

    hm.get_status()

    # method for setting the target and pathfinding target
    # GET THE CLASSES OF THE NON ANIMAL ROBOTS
    nnar = hm.get_non_non_animal_robot_class()
    nar = hm.get_non_animal_robot_class()
    # print(nnar.name)
    # SETTING PATHFINDING TARGETS
    nnar.set_pathfinding_target_position()  # pathfinding position must not be the pathfinding position of the other robot.
    print('nnar\n\n', nnar.target_position)

    nar.set_pathfinding_target_position()
    print('nar\n\n', nar.target_position)

    # NNAR step back from NAR
    nnar.step_back_from_NAR()
    # pathfinding method
    nnar.set_command_list()
    # tell robot to execute command
    nnar.execute_command_list()

    hm.get_status()

    # NAR moves to outer ring of AR
    # print('start', nar.position_vector)
    # print(hm.get_animal_robot_class())
    print(nar.move_to_animal_outer_ring())  # move the animal to the outer ring
    # print('end', nar.position_vector)
    # print(nar.pathfinding_target_position)
    nar.set_command_list()
    # print(nar.command_list)
    # robot executes command
    nar.execute_command_list()

    hm.get_status()

    # BOTH ARE IN THE OUTER RING IN CORRECT RELATIVE POSITION
    nar.move_to_inner_ring_animal()
    nnar.move_to_inner_ring_animal()

    nar.execute_command_list()
    nnar.execute_command_list()
    # EXECUTE COMMAND

    hm.get_status()

    # nar_command_list =

    # hm.get_status()
    pass

    # print(mouse.animal_path)  # return the path of the animal


def uncommented_functional_main():
    hm.get_status()

    # changes which animal is the correct animal class
    animal_choice_class = mouse.make_user_choice()  # animal makes choice
    mouse.change_animal_class(animal_choice_class)  # animal moves to its choice

    hm.get_status()

    # set the animal position
    mouse.set_animal_position()  # change the position of the animal based on its movement

    hm.get_status()

    # GET THE CLASSES OF THE NON ANIMAL ROBOTS
    nnar = hm.get_non_non_animal_robot_class()
    nar = hm.get_non_animal_robot_class()
    # SETTING PATHFINDING TARGETS
    nnar.set_pathfinding_target_position()  # pathfinding position must not be the pathfinding position of the other robot.

    nar.set_pathfinding_target_position()

    # NNAR step back from NAR
    nnar.step_back_from_NAR()
    # pathfinding method
    nnar.set_command_list()
    # tell robot to execute command
    nnar.execute_command_list()

    hm.get_status()

    # NAR moves to outer ring of AR

    print(nar.move_to_animal_outer_ring())  # move the animal to the outer ring

    nar.set_command_list()

    # robot executes command
    nar.execute_command_list()

    hm.get_status()

    # BOTH ARE IN THE OUTER RING IN CORRECT RELATIVE POSITION
    nar.move_to_inner_ring_animal()
    nnar.move_to_inner_ring_animal()
    # EXECUTE COMMAND
    nar.execute_command_list()
    nnar.execute_command_list()

    hm.get_status()

def main():
    # setting up which platform is which type for the path-finding
    robot1.is_animal_robot = 'AR'
    robot2.is_animal_robot = 'NNAR'
    robot3.is_animal_robot = 'NAR'

    # set the animal position one the animal robot is defined
    mouse.set_animal_position()

    hm.get_status()

    # method for setting the target and pathfinding target
    robot2.set_pathfinding_target_position()
    print('ROBOT2:', robot2.target_position, robot2.pathfinding_target_position)

    # non non animal robot step back from non animal robot (NAR)
    print('POSITION_VECTOR (robot2):', robot2.position_vector)
    robot2.step_back_from_NAR()  # step back command needs to added??
    print('POSITION_VECTOR (robot2):', robot2.position_vector)

    # pathfinding method
    robot2.set_command_list()
    print('Path List', robot2.path_list)
    print('Command List:', robot2.command_list)
    robot2.excute_command_list()

    # method for setting the target and pathfinding target
    robot3.set_pathfinding_target_position()
    print('ROBOT3:', robot3.target_position, robot3.pathfinding_target_position)

    # NAR step to outer ring of AR
    print('POSITION_VECTOR (robot3):', robot3.position_vector)
    robot3.move_to_animal_outer_ring()
    print('POSITION_VECTOR (robot3):', robot3.position_vector)

    # pathfinding method
    robot3.set_command_list()
    print('Path List', robot3.path_list)
    print('Command List:', robot3.command_list)
    robot3.excute_command_list()

    # method for stepping into the inner ring
    hm.get_status()

    print('move to inner ring')
    robot2.move_to_inner_ring_animal()
    print(robot2.command_list, robot2.path_list)
    robot3.move_to_inner_ring_animal()

    robot2.excute_command_list()
    robot3.excute_command_list()

    # print('POSITION_VECTOR (robot2):', robot2.position_vector)
    # print('POSITION_VECTOR (robot3):', robot3.position_vector)
    #
    # print(robot2.animal_relative_position(robot2.position_vector))
    # print(robot3.animal_relative_position(robot3.position_vector))

    hm.get_status()



def test():

    # print(robot1.move_no_rotation())
    pass


def run_programe(run_no):
    run = 0
    while run <= run_no:
        print(f"Round {run}")
        functional_main()

        run = run + 1

if __name__ == '__main__':


    # print(hm.get_animal_robot_class().position_vector)
    run_programe(3)
    # print('Mouse Path:', mouse.animal_path)
    # mouse.output_animal_path()
    pass
