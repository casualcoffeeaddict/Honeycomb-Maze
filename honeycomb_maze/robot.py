"""Robot Class"""
import logging
from random import choice

import paramiko


# from connect import *


class PlatformRobot:

    def __init__(self, x, y, z, direction, *name):
        # (Optional) identity of Robot
        self.name = name
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
        self.inner_ring_steps = [-1, -1, 1, 1, 1, -1]
        self.outer_ring_steps = [1, 1, -1, -1, -1, 1]

    # def ssh_connect(self, ip_address, username, password):
    #     self.name = paramiko.SSHClient()
    #     self.name.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #     self.name.connect(ip_address, username, password)

    def set_maze(self, maze_class):
        """Set the maze in which the robot is in"""
        self.maze = maze_class
        self.maze.add_robot(self)

    def set_animal_robot(self, bool):
        """Set the robot which has the animal on it and sets the other robots to 2
        ---
        AR = is animal robot
        NAR = in t-1 was animal robot
        NNAR = in t-1 was not animal robot

        """
        if bool == True:
            self.is_animal_robot = 'AR'
        # also set the non-animal robot to self.is_animal_robot to 2
        for robot in self.maze.robot_list:
            if robot is not self:
                robot.is_animal_robot = 'NNAR'

                # Write function makes non animal robot with 2 consecutive robots the NAR
                # and the non consecutive non animal robot NNAR

    def relative_direction(self, position_vector, ):
        """get the direction of the robot with respect to the grid (i.e. relative to the North)"""
        pass

    def get_change_position(self, axis, step):
        """Move position vector around the board"""
        x = self.position_vector[0]
        y = self.position_vector[1]
        z = self.position_vector[2]
        if axis == 'x':
            y += step
            z -= step
            return [x, y, z]
        elif axis == 'y':
            x += step
            z -= step
            return [x, y, z]
        elif axis == 'z':
            x += step
            y -= step
            return [x, y, z]
        else:
            print('ERROR: Select correct dimension, either x, y, z')
            logging.error('Select correct dimension, either x, y, z')

    def change_position(self, axis, step):
        """Move position vector around the board"""
        x = self.position_vector[0]
        y = self.position_vector[1]
        z = self.position_vector[2]
        if axis == 'x':
            y += step
            z -= step
            self.position_vector = [x, y, z]
            return self.position_vector
        elif axis == 'y':
            x += step
            z -= step
            self.position_vector = [x, y, z]
            return self.position_vector
        elif axis == 'z':
            x += step
            y -= step
            self.position_vector = [x, y, z]
            return self.position_vector
        else:
            print('ERROR: Select correct dimension, either x, y, z')
            logging.error('Select correct dimension, either x, y, z')

    def move_no_rotation(self):
        direction_to_axis = {0: 'x', 1: 'y', 2: 'z', 3: 'x', 4: 'y', 5: 'z'}
        axis = direction_to_axis[self.direction]
        # step back and forth for the position vector

        movement_choices = []
        step_list = [1, -2]
        for step in step_list:
            movement_choices.append(self.get_change_position(axis, step))
        return movement_choices

    def get_target_position(self):
        """
        Get a target position vector which is valid in the following ways:
        1. It must not be the current position of a robot
        2. It must be in the outer ring and a valid relative position
        3. It must not be in the current pathfinding target position of the other non animal robot
        """
        animal_robot = self.maze.get_animal_robot_class()
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

            # remove the position of the other robot's target position

            if robot.target_position != None:
                if list(robot.target_position) in choices:
                    choices.remove(list(robot.target_position))
                else:
                    print(f"INFO: The robot,{robot.name}'s target position was not in the list of choices. It was {robot.target_position}")

        print(choices)
        logging.info(choices)
        # 2. It must be in the outer ring and a valid relative position

        return tuple(choice(choices))

    def set_pathfinding_target_position(self, ):
        """Based on the target position, the pathfinding target position also has to be set
        INFO:
        self.target_position is the place where the robot wants to go
        self.pathfinding_target_position is the place where the pathfinding for networkx will aim for
        """
        target_position = self.get_target_position()  # get target position
        target_rel_position = self.animal_relative_position(target_position)  # get relative position of target

        rel_inner_ring = [[-1, 0, +1], [-1, 1, 0], [0, 1, -1], [1, 0, -1], [1, -1, 0], [0, -1, 1]]
        move = rel_inner_ring[target_rel_position]
        # get position of target based on relative position
        pathfinding_target_position = [a_i + n_i for a_i, n_i in zip(target_position, move)]

        # set give the robot the target and the pathfinding target position
        self.target_position = target_position
        self.pathfinding_target_position = tuple(pathfinding_target_position)
        return target_position, target_rel_position

    def set_target_position(self):
        self.target_position = self.get_target_position()
        # self.set_pathfinding_target_position()

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

    def non_animal_relative_position(self, position_vector):
        """Get the relative position between two robots"""
        non_animal_robot = self.maze.get_non_animal_robot_class()
        # subtract the two position vectors to return relative position vector
        # print(animal_robot.position_vector, non_animal_robot.position_vector)
        x, y, z = [a_i - n_i for a_i, n_i in zip(non_animal_robot.position_vector, position_vector)]
        print('NAR Relative position vector', x, y, z)
        logging.info('NAR Relative position vector', x, y, z)
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
            print(f'The robot {non_animal_robot.name} is off axis (its position is invalid because it is off axis),'
                  f' or robot is at origin.')
            logging.error(
                f'The robot {non_animal_robot.name} is off axis (its position is invalid because it is off axis),'
                f' or robot is at origin.')

    def update_relative_direction(self):
        """Get the direction of the robot (from 0 to 5)"""
        pass

    def get_consecutive_position(self):
        """Get the positions that are in the inner ring of the robot's current position"""
        rel_inner_ring = [[-1, 0, +1], [-1, 1, 0], [0, 1, -1], [1, 0, -1], [1, -1, 0], [0, -1, 1]]
        inner_ring = []
        for coord in rel_inner_ring:
            consecutive_position = [a_i + b_i for a_i, b_i in zip(coord, self.position_vector)]
            inner_ring.append(consecutive_position)
        return inner_ring

    def get_outer_ring_position(self):
        """Get the positions that are in the inner ring of the robot's current position"""
        rel_inner_ring = [[-1, 0, +1], [-1, 1, 0], [0, 1, -1], [1, 0, -1], [1, -1, 0], [0, -1, 1]]
        outer_ring = []
        for coord in rel_inner_ring:
            consecutive_position = [2 * a_i + b_i for a_i, b_i in zip(coord, self.position_vector)]
            outer_ring.append(consecutive_position)
        return outer_ring

    def move_to_outer_ring(self, direction):
        """Move to outer ring"""
        outer_ring_move = [
            self.change_position(self.ring_dim[direction],
                                 self.outer_ring_steps[direction])]
        return outer_ring_move

    def move_to_inner_ring(self, direction):
        """Move to inner ring"""
        # print('DEBUGGING', self.ring_dim[direction],
        #       self.inner_ring_steps[direction])
        # logging.debug('DEBUGGING', self.ring_dim[direction],
        #       self.inner_ring_steps[direction])
        inner_ring_move = [
            self.change_position(self.ring_dim[direction],
                                 self.outer_ring_steps[direction])]
        return inner_ring_move

    def step_back_from_NAR(self):
        """
        Step backwards (away from the other robots)
        ---
        Since due to the position of the robots, the NNAR robot should always be facing the NAR
        """
        print(self.name, 'position vector', self.position_vector)
        rel_pos = self.non_animal_relative_position(self.position_vector)
        print('DEBUGGING: relative position', rel_pos)
        logging.debug('DEBUGGING: relative position', rel_pos)
        # add

        return self.move_to_inner_ring(rel_pos)

    def move_to_animal_outer_ring(self):
        """
        Method for the NAR robot
        ---
        return the value (should only be one) that intersects with possible movements
        without rotation with the outer ring
        """
        # list of coordinates
        animal_robot_class = self.maze.get_animal_robot_class()
        animal_movement_choices = self.maze.get_outer_ring_coordinates(animal_robot_class.position_vector)
        # return intersection of lists
        self_movement_choices = self.move_no_rotation()
        print('animal_movement_choices', animal_movement_choices)
        print('self_movement_choices', self_movement_choices)

        def common_elements(list1, list2):
            result = []
            for element in list1:
                if element in list2:
                    result.append(element)
            return result

        # get common element
        common_element = common_elements(animal_movement_choices, self_movement_choices)
        # assign new position vector
        self.position_vector = common_element[0]
        return self.position_vector

    def get_move_to_inner_ring(self, direction):

        inner_ring_move = self.get_change_position(self.ring_dim[direction],
                                                    self.outer_ring_steps[direction])

        return inner_ring_move

    def move_to_inner_ring_animal(self):
        """
        Method for the both robots
        ---
        return the value (should only be one) that intersects with possible movements
        without rotation with the outer ring
        """
        self.path_list = [self.position_vector]

        rel_pos = self.animal_relative_position(self.position_vector)  # get relative position of animal robot
        move = self.get_move_to_inner_ring(rel_pos)
        print('rel_pos', rel_pos)
        print('move', move)
        print(self.position_vector)

        def flatten(t):
            return [item for sublist in t for item in sublist]

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

    def turn_robot(self, move):
        """Method for make_command_list: returns the number of turns required to get to the next move"""
        # from self.direction, return the number of turns required to get the correct direction
        direction_difference = self.path_relative_position(move, self.position_vector) - self.direction
        turns = direction_difference % 6
        return turns

    def path_relative_position(self, path_position_vector, current_position_vector):
        """Get the relative position between two robots"""
        # subtract the two position vectors to return relative position vector
        # print(animal_robot.position_vector, non_animal_robot.position_vector)
        x, y, z = [p_i - m_i for p_i, m_i in zip(path_position_vector, current_position_vector)]
        if x == 0 and y == 0 and z == 0:
            print(f'The robot {self.name} is itself the animal robot so relative position is undefined')
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
            print(f'The robot {self.name} can not move to this position ')

    def make_command_list(self, path_list):
        """
        From the move list convert it to a set of commands to be sent to the associated robot

        First element of path-list will be next position vector of the robot,
        and then the moves it will make come sequentially after

        Format for output: [turns, steps, turns, steps...] for the number of elements in the list

        """
        command_list = []
        for move in path_list[1:]:
            # Handle turns
            if self.direction == self.path_relative_position(move, self.position_vector):
                # no need to turn
                print('INFO: 0 added')
                logging.info('INFO: 0 added')
                command_list.append(0)
            elif self.direction != self.path_relative_position(move, self.position_vector):
                turns = self.turn_robot(move)
                # make turns more efficient - quick fix
                print(f'INFO: {turns} turns added')
                logging.info(f'INFO: {turns} turns added')
                command_list.append(turns)
                # update the direction of the robot (ie add the number of turns it makes to the direction
                # then remainder 6)
                self.direction += turns
                self.direction = self.direction % 6

            # Handle steps
            if self.position_vector == list(move):
                # No moves required - this should not happen
                pass
            elif self.position_vector != list(move):
                # step forward 1
                print('INFO: 1 added')
                logging.info('INFO: 1 added')
                command_list.append(1)
                # update position
                self.position_vector = list(move)

        return command_list

    def set_command_list(self):
        # get path from pathfinder function
        self.path_list = self.maze.pathfinder(self)
        # make command list from path list
        command_list = self.make_command_list(self.path_list)
        # set the path list
        self.command_list = command_list

    def execute_command_list(self):
        """
        Before this command is run, the command list must be initialised

        WILL MOVE ROBOTS!
        Send the commands to the robot to move
        """
        if self.command_list == None:
            print('The command list is empty')
        elif self.command_list != None:
            # make list into string of numbers
            command_string = ' '.join(map(str, self.command_list))
            # send command
            # stdin, stdout, sterr = self.name.exec_command(f'./lineFollowJunction4 {command_string}')
            print(f'./lineFollowJunction4 {command_string}')
            # to prevent commands being executed twice, clear the command list
            self.command_list = None

            # reset the target position
            self.target_position = None
