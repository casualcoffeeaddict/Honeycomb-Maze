"""Robot Class"""
import logging
import random
import paramiko
import time

from honeycomb_maze.static_methods import *


class PlatformRobot:

    def __init__(self, x, y, z, direction, ip_address, execute, *name):
        # (Optional) identity of Robot
        self.name = name
        self.ssh_connect(execute, ip_address)
        # Position of robot
        self.position_vector = [x, y, z]
        # Orientation of robot
        self.direction = direction
        # Identifies robot with animal on it
        self.is_animal_robot = None
        # Target positions on the network
        self.target_position = None
        self.pathfinding_target_position = None
        # Path robot takes
        self.path_list = None
        self.command_list = None
        # Maze robot is placed in
        self.maze = None
        # For moving to and from inner and outer ring
        self.ring_dim = ['y', 'z', 'x', 'y', 'z', 'x']
        self.outer_ring_steps = [1, 1, -1, -1, -1, 1]
        self.inner_ring_steps = [-1, -1, -1, 1, 1, 1]

        self.rel_inner_ring = [[1, 0, -1], [1, -1, 0], [0, -1, 1], [-1, 0, +1], [-1, 1, 0], [0, 1, -1]]

        self.direction_to_axis = {0: 'y', 1: 'z', 2: 'x', 3: 'y', 4: 'z', 5: 'x'}

    def set_maze(self, maze_class):
        """Set the maze in which the robot is in"""
        self.maze = maze_class
        self.maze.add_robot(self)

    def set_animal_robot(self, bool):
        """Set the robot which has the animal on it and sets the other robots to 2
        ---
        AR = is animal robot
        NAR = in move t-1 was animal robot
        NNAR = in move t-1 was not animal robot

        """
        if bool == True:
            self.is_animal_robot = 'AR'
        # also set the non-animal robot to self.is_animal_robot to 2
        for robot in self.maze.robot_list:
            if robot is not self:
                robot.is_animal_robot = 'NNAR'

                # Write function makes non animal robot with 2 consecutive robots the NAR
                # and the non consecutive non animal robot NNAR

    def get_relative_direction(self, position_vector, ):
        """get the direction of the robot with respect to the grid (i.e. relative to the North)"""
        pass

    def get_change_position(self, axis, step):
        """
        Move position vector around the board
        The positivon vector of the robot would not be updated, however
        ------
        :return [x, y, z]: Coordinates of the position vector that the robot would move to
        """
        x = self.position_vector[0]
        y = self.position_vector[1]
        z = self.position_vector[2]
        return self.movement(axis, step, x, y, z)

    def change_position(self, axis, step):
        """
        Move position vector around the board
        """
        x = self.position_vector[0]
        y = self.position_vector[1]
        z = self.position_vector[2]
        self.position_vector = self.movement(axis, step, x, y, z)
        return self.position_vector

    @staticmethod
    def movement(axis, step, x, y, z):
        """
        :param axis: axis (as a letter) for the direction of movement
        :param step: the number of steps taken in this direction
        :param x: x-coord
        :param y: y-coord
        :param z: z-coord
        :return position_vector:  the new position_vector of this movement
        """
        if axis == 'x':
            y += step
            z -= step
            position_vector = [x, y, z]
            return position_vector
        elif axis == 'y':
            x = x + step
            z -= step
            position_vector = [x, y, z]
            return position_vector
        elif axis == 'z':
            x += step
            y -= step
            position_vector = [x, y, z]
            return position_vector
        else:
            print('ERROR: Select correct dimension, either x, y, z')
            logging.error('Select correct dimension, either x, y, z')

    def get_relative_position(self, x, y, z):
        """
        Original Definition for relative position in the robot class
        :param x: x-coordinate of relative position vector
        :param y: y-coordinate of relative position vector
        :param z: z-coordinate of relative position vector
        :return: relative position of relative position vector
        """
        print('Debugging: Relative Position Vector', x, y, z)
        logging.debug('Debugging: Relative Position Vector', x, y, z)
        if x == 0 and y == 0 and z == 0:
            print(f'ERROR: The robot {self.name} is itself the animal robot so relative position is undefined')
            logging.error(f'ERROR: The robot {self.name} is itself the animal robot so relative position is undefined')
        elif y == 0 and x > 0:
            return 0
        elif z == 0 and x > 0:
            return 1
        elif x == 0 and y < 0:
            return 2
        elif y == 0 and x < 0:
            return 3
        elif z == 0 and x < 0:
            return 4
        elif x == 0 and y > 0:
            return 5
        else:
            print(f'The robot {self.name} is off axis (its position is invalid because it is off axis),'
                  f' or robot is at origin.')
            logging.info(f'The robot {self.name} is off axis (its position is invalid because it is off axis),'
                         f' or robot is at origin.')

    def move_no_rotation(self):
        """
        For the robot self, this function will return the position vectors of the movements
        that are possible for the robot to make without any rotation.
        NOTE: this will not change the value of the position vector for robot.
        :return movement choices: list of position vectors that are valid
        """

        axis = self.direction_to_axis[self.direction]
        # step back and forth for the position vector
        print(self.position_vector)
        movement_choices = []
        step_list = [0, 1, -1]
        for step in step_list:
            movement_choices.append(self.get_change_position(axis, step))

        return movement_choices

    def get_step_back(self):
        """

        ---
        :param robot_class: class of the robot that is moving back
        :return: position_vector of the robot once it has stepped back one step
        """
        direction = self.direction
        direction_axis = self.direction_to_axis[direction]
        return self.get_relative_position(direction_axis, -1)  # return the position of one step back from the robot

    def get_target_position(self, manual=False):
        """
        Least well design part of the code. Requires a better implementation
        ---
        Get a target position vector which is valid in the following ways:
        1. It must not be the current position of a robot
        2. It must be in the outer ring of the AR and a valid relative position
        3. It must not be in the current pathfinding target position of the other non animal robot
        4. The pathfinding_target for NNAR must not be in the inner ring of the NAR
        """
        animal_robot = self.maze.get_animal_robot_class()
        non_animal_robot = self.maze.get_non_animal_robot_class()
        choices = self.maze.get_inner_ring_coordinates(animal_robot.position_vector)
        # 1. It must not be the current position of a robot
        # remove positions of the animal coordinates
        for robot in self.maze.robot_list:
            # remove the position of the robots from the 'choices' list
            if robot.position_vector in choices:
                choices.remove(robot.position_vector)
            else:
                print('INFO: Robot position vector not inside choice of target positions')
                logging.info('INFO: Robot position vector not inside choice of target positions')

            # 3. remove the position of the other robot's target position
            if robot.target_position != None:
                if list(robot.target_position) in choices:
                    choices.remove(list(robot.target_position))
                else:
                    print(
                        f"INFO: The robot,{robot.name}'s target position was not in the list of choices. It was {robot.target_position}")

        # 4. The pathfinding_target for NNAR must not be in the inner ring of the NAR after it steps back
        # if the robot which is selecting a target is the NNAR
        # if self.is_animal_robot == 'NNAR':
        #     # get the position of the NAR once it steps back
        #     nar_step_back_position = non_animal_robot.get_step_back()
        #     # get in the inner ring of that position
        #     inner_ring_list_nar = self.inner_ring_positions(nar_step_back_position)
        #     # remove any of the positions in this list from the choices list
        #     for position in inner_ring_list_nar:
        #         if position in choices:
        #             choices.remove(position)

        print(choices)
        logging.info(choices)
        # 2. It must be in the outer ring and a valid relative position

        # For debugging, making choices manual or not
        if manual == False:
            return tuple(random.choice(choices))
        elif manual == True:
            while True:
                try:
                    index = int(input('What is the index of the position you would like to choose from this list?'))
                    break
                except ValueError:
                    print(f'Please input an integer in the range {len(choices)}')
            return choices[index - 1]

    # def set_pathfinding_source_position(self):
    #
    #     # get the source position
    #     source_position = self.position_vector
    #     # get the pathfinding source position
    #     source_rel_position = self.animal_relative_position(source_position)
    #     move = self.rel_inner_ring[source_rel_position]
    #     source_target_position = [a_i + n_i for a_i, n_i in zip(source_position, move)]

    def set_pathfinding_target_position(self, manual=False):
        """Based on the target position, the pathfinding target position also has to be set
        INFO:
        self.target_position is the place where the robot wants to go
        self.pathfinding_target_position is the place where the pathfinding for networkx will aim for
        """
        # get the target position
        target_position = self.get_target_position(manual)
        # get relative position of target
        target_rel_position = self.animal_relative_position(target_position)
        # get the opposite index (ie plus 3)
        target_rel_movement = (target_rel_position + 3) % 6
        print('target position:', target_position)
        print('target rel movement:', target_rel_movement)
        move = self.rel_inner_ring[target_rel_movement]
        # get position of target based on relative position
        pathfinding_target_position = [a_i + n_i for a_i, n_i in zip(target_position, move)]

        # set give the robot the target and the pathfinding target position
        self.target_position = target_position
        self.pathfinding_target_position = tuple(pathfinding_target_position)
        return target_position, target_rel_position

    def set_target_position(self):
        self.target_position = self.get_target_position()
        # self.set_pathfinding_target_position()

    def get_relative_position_NEW(self, x, y, z):
        """
        UNIMPLEMENTED
        ---
        NEW Definition for relative position in the robot class
        :param x: x-coordinate of relative position vector
        :param y: y-coordinate of relative position vector
        :param z: z-coordinate of relative position vector
        :return: relative position of relative position vector
        """
        print('Debugging: Relative Position Vector', x, y, z)
        logging.debug('Debugging: Relative Position Vector', x, y, z)
        if x == 0 and y == 0 and z == 0:
            print(f'ERROR: The robot {self.name} is itself the animal robot so relative position is undefined')
            logging.error(f'ERROR: The robot {self.name} is itself the animal robot so relative position is undefined')
        elif x == 0 and y > 0:
            return 0
        elif y == 0 and x > 0:
            return 1
        elif z == 0 and y < 0:
            return 2
        elif x == 0 and y < 0:
            return 3
        elif y == 0 and x < 0:
            return 4
        elif z == 0 and y > 0:
            return 5
        else:
            print(f'The robot {self.name} is off axis (its position is invalid because it is off axis),'
                  f' or robot is at origin.')
            logging.info(f'The robot {self.name} is off axis (its position is invalid because it is off axis),'
                         f' or robot is at origin.')

    def animal_relative_position(self, position_vector):
        """
        Get the relative position between a position vector and the animal robot.
        ---
        Input: position vector = (x, y, z)
        """

        animal_robot = self.maze.get_animal_robot_class()

        if animal_robot.position_vector == position_vector:
            # if the animal robot wants to find the position vector relative to itself
            print('ERROR: relative_position of the animal robot can not be found w.r.t itself')
            logging.error('ERROR: relative_position of the animal robot can not be found w.r.t itself')
        # subtract the two position vectors to return relative position vector
        print('DEBUGGING: animal robot position vector:', animal_robot.position_vector, 'position vector',
              position_vector)
        logging.debug('DEBUGGING: animal robot position vector:', animal_robot.position_vector, 'position vector',
                      position_vector)
        x, y, z = [a_i - n_i for a_i, n_i in zip(animal_robot.position_vector, position_vector)]
        return self.get_relative_position(x, y, z)

    def non_animal_relative_position(self, position_vector):
        """Get the relative position between two robots"""
        non_animal_robot = self.maze.get_non_animal_robot_class()
        # subtract the two position vectors to return relative position vector
        # print(animal_robot.position_vector, non_animal_robot.position_vector)
        x, y, z = [a_i - n_i for a_i, n_i in zip(position_vector, non_animal_robot.position_vector)]
        return self.get_relative_position(x, y, z)

    def update_relative_direction(self):
        """Get the direction of the robot (from 0 to 5)"""
        pass

    def inner_ring_positions(self, position_vector):

        inner_ring = []
        for coord in self.rel_inner_ring:
            consecutive_position = [a_i + b_i for a_i, b_i in zip(coord, position_vector)]
            inner_ring.append(consecutive_position)
        return inner_ring

    def get_inner_ring_position(self):
        """
        Get the positions that are in the inner ring of the robot's current position
        ---
        :return inner_ring: list of adjacent positions of the robot
        """
        # inner_ring = []
        # for coord in self.rel_inner_ring:
        #     consecutive_position = [a_i + b_i for a_i, b_i in zip(coord, self.position_vector)]
        #     inner_ring.append(consecutive_position)
        # return inner_ring
        return self.inner_ring_positions(self.position_vector)

    def get_outer_ring_position(self):
        """Get the positions that are in the inner ring of the robot's current position"""
        outer_ring = []
        for coord in self.rel_inner_ring:
            consecutive_position = [2 * a_i + b_i for a_i, b_i in zip(coord, self.position_vector)]
            outer_ring.append(consecutive_position)
        return outer_ring

    def move_to_outer_ring(self, rel_pos):
        """
        Moves to the outer ring of the animal robot based on the self.robot's relative position to the animal robot
        :param rel_pos: Relative position
        :return outer_ring_move:
        """
        outer_ring_move = [
            self.change_position(self.ring_dim[rel_pos],
                                 self.outer_ring_steps[rel_pos])]
        return outer_ring_move

    def move_to_inner_ring(self, rel_pos):
        """
        Moves to the inner ring of the animal robot based on the self.robot's relative position to the animal robot
        :param rel_pos: Relative position
        :return inner_ring_move:
        """
        inner_ring_move = [
            self.change_position(self.ring_dim[rel_pos],
                                 self.inner_ring_steps[rel_pos])]
        return inner_ring_move

    def step_back_from_NAR(self, execute=True):
        """
        Step backwards (away from the other robots)
        ---
        Since due to the position of the robots, the NNAR robot should always be facing the NAR
        """
        print(f'The robot {self.name}, has position {self.position_vector}')
        rel_pos = self.non_animal_relative_position(self.position_vector)
        print('DEBUGGING: relative position:', rel_pos)
        logging.debug('DEBUGGING: relative position', rel_pos)

        # Robot turns around
        # new position of the robot (back one step)
        new_position = self.move_to_outer_ring(rel_pos)
        self.position_vector = tuple(flatten(new_position))

        # new direction of robot since the robot turns around (flip)
        self.direction = (self.direction + 3) % 6

        # send commands to ssh to do this
        print('Turn around command:', [1, 1])
        if execute == True:
            self.execute_command('1, 1')

        return new_position

    # def step_back_from_NAR_execute(self):
    #     """
    #     Execute the 'turn around' command which the robot requires to 'see' where it is going with the IR sensor at the
    #     front
    #     ------
    #     :return: Commands required for the 'turn around' SSH command to be executed
    #     """
    #     self.execute_command('1, 1')

    # def move_to_animal_outer_ring(self):
    #     """
    #     Method for the NAR robot
    #     ---
    #     return the value (should only be one) that intersects with possible movements
    #     without rotation with the outer ring
    #     """
    #     # list of coordinates
    #     ar_class = self.maze.get_animal_robot_class()
    #     animal_movement_choices = self.maze.get_outer_ring_coordinates(ar_class.position_vector)
    #     # return intersection of lists
    #     self_movement_choices = self.move_no_rotation()
    #     print(f'The AR {ar_class.name}, is in position {ar_class.position_vector} has choices',
    #           animal_movement_choices)
    #     print(f'The NAR {self.name}, is in position {self.position_vector} has choices',
    #           self_movement_choices)
    #
    #     # get common element (ie the option that is available for the robot to move to
    #     common_element = common_elements(animal_movement_choices, self_movement_choices)
    #     # assign this as the new position vector
    #     print('COMMON ELEMENT', common_element)
    #     self.position_vector = common_element[0]
    #     return self.position_vector

    def move_to_robot_outer_ring(self, stationary_robot):
        """
        ---
        :return position_vector: the value (should only be one) that intersects with possible movements
        without rotation with the outer ring
        """
        # list of coordinates
        animal_movement_choices = self.maze.get_outer_ring_coordinates(stationary_robot.position_vector)
        # return intersection of lists
        self_movement_choices = self.move_no_rotation()
        print(f'The AR {stationary_robot.name}, is in position {stationary_robot.position_vector} has choices',
              animal_movement_choices)
        print(f'The NAR {self.name}, is in position {self.position_vector} has choices',
              self_movement_choices)

        # get common element (ie the option that is available for the robot to move to
        common_element = common_elements(animal_movement_choices, self_movement_choices)
        # assign this as the new position vector
        print('COMMON ELEMENT', common_element)
        self.position_vector = common_element[0]
        return self.position_vector

    def move_to_non_animal_outer_ring(self, execute=True):
        """
        Method for NNAR Robot
        ---
        :param execute:
        :return:
        """
        # Get the movement position
        nar_class = self.maze.get_non_animal_robot_class()
        self.move_to_robot_outer_ring(nar_class)

        # Due to line_follow_robot11, flip the direction of the robot
        self.direction = (self.direction + 3) % 6

        if execute == True:
            self.execute_command('1, 1')
            time.sleep(11)

    def move_to_animal_outer_ring(self, execute=True):
        """
        Method for the NAR robot
        ---
        return the value (should only be one) that intersects with possible movements
        without rotation with the outer ring
        """
        # list of coordinates
        ar_class = self.maze.get_animal_robot_class()
        self.move_to_robot_outer_ring(ar_class)

        # Due to line_follow_robot11, flip the direction of the robot
        self.direction = (self.direction + 3) % 6

        # send SSH Command to turn around
        print('Turn around command:', [1, 1])
        if execute == True:
            self.execute_command('1, 1')

    def get_move_to_inner_ring(self, rel_pos):
        """

        :param rel_pos:
        :return inner_ring_move:
        """
        inner_ring_move = self.get_change_position(self.ring_dim[rel_pos],
                                                   self.outer_ring_steps[rel_pos])
        return inner_ring_move

    def move_to_inner_ring_animal(self):
        """
        Method for the both robots
        ---
        return the value (should only be one) that intersects with possible movements
        without rotation with the outer ring
        """
        self.path_list = [self.position_vector]  # initial position of

        rel_pos = self.animal_relative_position(self.position_vector)  # get relative position of animal robot
        move = self.get_move_to_inner_ring(rel_pos)
        print('rel_pos', rel_pos)
        print('move', move)
        print(self.position_vector)

        self.path_list.append(list(move))
        print(self.path_list)
        self.command_list = self.make_command_list(self.path_list)

    def get_move_list(self):
        """From the maze, get the path, generated from Pathfinder method"""
        if self.maze is not None:
            if self.maze.path is not None:
                return self.maze.path
            else:
                print('ERROR: Maze path does not exist')
                logging.error('ERROR: Maze path does not exist')
        else:
            print('ERROR: Maze has not been defined')
            logging.error('ERROR: Maze has not been defined')

    def set_move_list(self):
        self.move_list = self.get_move_list()

    def path_relative_position(self, path_position_vector, current_position_vector, ):
        """
        :param path_position_vector:
        :param current_position_vector:
        :return relative_position: Relative position of the self robot compared with the position vector
        """
        # subtract the two position vectors to return relative position vector
        # print(animal_robot.position_vector, non_animal_robot.position_vector)
        x, y, z = [p_i - m_i for p_i, m_i in zip(path_position_vector, current_position_vector)]
        return self.get_relative_position(x, y, z)

    def turn_robot(self, move, clockwise=True):
        """
        Method for make_command_list: returns the number of turns required to get to point in the correct direction
        """
        # Method for defining the axis in the clockwise relative positions or the anticlockwise relative positions
        if clockwise == True:
            modulus = 6
        elif clockwise == False:
            modulus = -6

        # from self.direction, return the number of turns required to get the correct direction
        direction_difference = self.path_relative_position(move, self.position_vector) - self.direction
        turns = direction_difference % modulus
        return abs(turns)

    def make_command_list(self, path_list, clockwise=True):
        """
        From the move list convert it to a set of commands to be sent to the associated robot

        First element of path-list will be next position vector of the robot,
        and then the moves it will make come sequentially after

        Format for output: [Turn around (0, 1)] [steps] [turns, steps, turns, steps...] for the number of elements in the list

        Since no turning around takes place the first command will be 0 AND the sequence will start with asking
        how many turns are required second command (for steps) will be 0
        ------
        :param path_list: The list of coordinates that the robot passes through
        :return command_list: The commands the robot will need to excute to get to follow the path of coordinates


        """
        # Chirality of the surface, should be clockwise (like the relative position it)
        if clockwise == True:
            modulus = 6
        elif clockwise == False:
            modulus = -6

        # starting command
        command_list = []
        for move in path_list[1:]:  # starts at second entry in list as the first entry is the
            # print(self.direction, self.path_relative_position(move, self.position_vector))
            # Handle turns
            print(
                f'Next move:{move}, '
                f'self.direction = {self.direction} , '
                f'path_relative_position: {self.path_relative_position(move, self.position_vector)}'
            )
            if self.direction == self.path_relative_position(move, self.position_vector):
                # no need to turn
                print('INFO: Direction the same, 0 added')
                logging.info('INFO: 0 added')
                command_list.append(0)
            elif self.direction != self.path_relative_position(move, self.position_vector):
                turns = self.turn_robot(move, clockwise)
                # make turns more efficient - quick fix
                print(f'INFO: {turns} turns added')
                command_list.append(turns)
                # update the direction of the robot (ie add the number of turns it makes to the direction
                # then remainder 6)
                print(f'Initial {self.direction}')
                self.direction = turns + self.direction
                self.direction = abs(self.direction % modulus)
                print(f'Final {self.direction}')

            # Handle steps
            if self.position_vector == list(move):
                # No moves required - this should not happen
                pass
            elif self.position_vector != list(move):
                # step forward 1
                print('INFO: 1 step added')
                logging.info('INFO: 1 added')
                command_list.append(1)
                # update position
                self.position_vector = list(move)

        return [0, 0] + self.remove_zeros(command_list)

    @staticmethod
    def remove_zeros(command_list):
        """
        remove the '0 1' entries from the list and replace them with '2' in the correct place
        ---
        :param command_list:
        :return command_list: without '0 1' in the command list
        """
        flag = True
        while flag == True:
            length_of_list = len(command_list) - 1
            # print('length_of_list', length_of_list)
            for index in range(length_of_list):
                # print('length', length_of_list)
                # print('index:', index)
                # if index > 1:
                # print('command',command_list[index])
                if command_list[index] == 0:
                    # update the value (to 2)
                    command_list[index - 1] = command_list[index - 1] + command_list[index + 1]
                    # remove the 0 1 from the list
                    command_list.pop(index)
                    length_of_list = length_of_list - 1
                    command_list.pop(index)
                    length_of_list = length_of_list - 1
                    # print('length_of_list', length_of_list)
                    # print(command_list)
                    break
                elif command_list.count(0) == 0:
                    # stop the loop at this point
                    flag = False
        return command_list

    def set_command_list(self):
        # get path from pathfinder function
        self.path_list = self.maze.pathfinder(self)
        print(self.path_list)
        # make command list from path list
        command_list = self.make_command_list(self.path_list)
        print(command_list)
        # set the path list
        self.command_list = command_list

    # Methods for Secure Shell (SSH)

    def ssh_connect(self, execute, ip_address, username='root', password=''):
        """
        Connects the robot via ssh
        ------
        :param execute: Boolean to determine if the commands will be executed
        :param ip_address: IP address of robot
        :param username: Username of the robot
        :param password: Password of the robot

        """
        if execute == True:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(ip_address, port=22, username=username, password=password,
                             pkey=None, key_filename=None, timeout=None, allow_agent=True,
                             look_for_keys=True, compress=False)

    def execute_command_list(self, execute, sim=False):
        """
        Before this command is run, the command list must by the self.ssh_connect() command which is done in the
        __init__ function

        WILL MOVE ROBOTS!
        Send the commands to the robot to move
        """
        if execute == True:
            if self.command_list == None:
                print('The command list is empty')
            elif self.command_list != None:
                # make list into string of numbers
                command_string = ' '.join(map(str, self.command_list))
                # send command
                self.execute_command(command_string, sim)
                # to prevent commands being executed twice, clear the command list
                self.command_list = None
                # reset the target position
                self.target_position = None

    def execute_command(self, command_string, sim=False):
        # send command
        complete_command = f'./lineFollowJunction11 {command_string}'
        stdin, stdout, sterr = self.ssh.exec_command(complete_command)
        print(complete_command)

        # Timing
        run_time = self.get_run_time(command_string)
        if sim == True:
            # skip timing
            pass
        elif sim == False:
            print(f'Waiting {run_time} seconds')
            time.sleep(run_time)
            print('Waiting Complete')

    def get_run_time(self, command_string):
        """
        get the time required to execute the command
        :return run_time: the time requires to complete the command string
        """

        time_per_turn = 2
        time_per_step = 3.5
        time_per_half_turn_around = 4

        turn_around = []

        step_list = []
        turn_list = []
        index = 0
        for command in command_string[::2]:
            # turn around or not at the start
            if index <= 1:
                if command == '1':
                    turn_around.append(1)  # time taken for the turn around to take place
                if command == '0':
                    turn_around.append(0)

            # odd numbers
            if index % 2 == 1 and index > 1:
                step_list.append(int(command))
            # even numbers
            if index % 2 == 0 and index > 1:
                turn_list.append(int(command))

            index += 1

        run_time = sum(step_list) * time_per_step + sum(turn_list) * time_per_turn + sum(
            turn_around) * time_per_half_turn_around
        return run_time

    def coordinate_callibration(self, position_vector):
        """
        UNFINISHED AND DOESN'T WORK
        Go through relative position 0 - 5 in order to show the axis on the space
        :param position_vector: The position from which the calibration takes place
        :return:
        """
        position_vector = tuple(position_vector)
        command_list = [position_vector]

        for position in self.rel_inner_ring:
            new_position = tuple([a_i + b_i for a_i, b_i in zip(position_vector, position)])
            command_list.append(new_position)
            command_list.append(position_vector)

        print(command_list)
        command = self.make_command_list(command_list)

        command_string = ' '.join(map(str, command))
        print(command_string)
        self.execute_command(command_string)
