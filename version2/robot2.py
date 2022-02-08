"""Robot Class"""

from random import choice


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
        # Path robot takes
        self.move_list = None
        # Maze robot is placed in
        self.maze = None
        maze = self.maze
        # For moving to and from inner and outer ring
        self.ring_dim = ['y', 'z', 'x', 'y', 'z', 'x']
        self.inner_ring_steps = [-1, -1, 1, 1, 1, -1]
        self.outer_ring_steps = [1, 1, -1, -1, -1, 1]

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

    def change_position(self, axis, step):
        """Move position vector around the board"""
        # rotation_check = self.dimension_dict[dimension]
        # print('change position, self.position_vector', self.position_vector)
        # if self.direction != dimension:
        #     change = self.dimension_dict[dimension] - self.direction
        #     self.change_rotation(change)
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

    def move_no_rotation(self):
        direction_to_axis = {0: 'x', 1: 'y', 2: 'z', 3: 'x', 4: 'y', 5: 'z'}
        axis = direction_to_axis[self.direction]
        # step back and forth for the position vector

        movement_choices = []
        step_list = [1, -2]
        for step in step_list:
            movement_choices.append(self.change_position(axis, step))
        return movement_choices

    def get_target_position(self):
        animal_robot_position_vector = self.maze.get_animal_robot_position_vector()
        choices = self.maze.get_inner_ring_coordinates(animal_robot_position_vector)
        # remove positions of the animal coordinates
        for robot in self.maze.robot_list:
            if robot.position_vector in choices:
                choices.remove(robot.position_vector)
            else:
                print('INFO: Robot position vector not inside choice of target positions')
        print(choices)
        return tuple(choice(choices))

    def set_target_position(self):
        self.target_position = self.get_target_position()

    def animal_relative_position(self, position_vector):
        """Get the relative position between two robots.
         The default for the robot which the rel pos will be calculated against is the animal robot
         """
        animal_robot = self.maze.get_animal_robot_class()
        # subtract the two position vectors to return relative position vector
        # print(animal_robot.position_vector, non_animal_robot.position_vector)
        x, y, z = [a_i - n_i for a_i, n_i in zip(animal_robot.position_vector, position_vector)]
        print(x, y, z)
        if y == 0 and x > 0:
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

    def non_animal_relative_position(self, position_vector):
        """Get the relative position between two robots"""
        non_animal_robot = self.maze.get_non_animal_robot_class()
        # subtract the two position vectors to return relative position vector
        # print(animal_robot.position_vector, non_animal_robot.position_vector)
        x, y, z = [a_i - n_i for a_i, n_i in zip(non_animal_robot.position_vector, position_vector)]
        print(x, y, z)
        if y == 0 and x > 0:
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

    def update_relative_direction(self):
        """Get the direction of the robot (from 0 to 5)"""
        pass

    def move_to_outer_ring(self, direction):
        """Move to outer ring"""
        outer_ring_move = [
            self.change_position(self.ring_dim[direction],
                                 self.outer_ring_steps[direction])]
        return outer_ring_move

    def move_to_inner_ring(self, direction):
        """Move to inner ring"""
        inner_ring_move = [
            self.change_position(self.ring_dim[direction],
                                 self.inner_ring_steps[direction])]
        return inner_ring_move

    def step_back_from_NAR(self):
        """Step backwards (away from the other robots)
        ---
        Since due to the position of the robots, the NNAR robot should always be facing the NAR
        """
        rel_pos = self.non_animal_relative_position(self.position_vector)
        print(rel_pos)
        return self.move_to_inner_ring(rel_pos)

    def move_to_animal_outer_ring(self):
        """return the value (should only be one) that intersects with possible movements without rotation which is in
        the outer ring """
        animal_robot_class = self.maze.get_animal_robot_class()
        # list of coordinates
        animal_movement_choices = self.maze.get_inner_ring_coordinates(animal_robot_class.position_vector)
        # return intersection of lists
        self_movement_choices = self.move_no_rotation()

        def common_elements(list1, list2):
            result = []
            for element in list1:
                if element in list2:
                    result.append(element)
            return result

        return common_elements(animal_movement_choices, self_movement_choices)

    def get_move_list(self):
        """From the maze, get the path, generated from Pathfinder method"""
        if self.maze is not None:
            if self.maze.path is not None:
                return self.maze.path
            else:
                print('Error: Maze path does not exist')
        else:
            print('Error: Maze has not been defined')

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
        if y == 0 and x > 0:
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
        for move in path_list:
            # Handle turns
            if self.direction == self.path_relative_position(move, self.position_vector):
                # no need to turn
                command_list.append(0)
            elif self.direction != self.path_relative_position(move, self.position_vector):
                turns = self.turn_robot(move)
                # make turns more efficient - quick fix
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
                command_list.append(1)
                # update position
                self.position_vector = list(move)

        return command_list

    def send_command_list(self):
        """Send the commands via the ssh import to the self robot"""
        pass
