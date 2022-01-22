'''Robot classes and their functions for hexagon maze'''
import random as rand

class PlatformRobot():
    '''Base platform class and basic moving functions'''

    def __init__(self, x, y, z, rotation):
        # for rotation change method
        self.dimension_dict = {'x': 0, 'y': 1, 'z': 2}
        # location information about platform
        self.position_vector = [x, y, z]
        self.rotation = self.dimension_dict[rotation]
        # for inner ring function
        self.inner_ring_dim = ['x', 'y', 'z', 'x', 'y', 'z']
        self.inner_ring_steps = [-1, -1, -1, 1, 1, 1]

    def see_status(self):
        '''Get summary information about robot'''
        print(
            '\nStatus:'
            '\nPostion Vector:', self.position_vector,
            '\nRotation:', self.rotation
        )

    def get_inner_ring(self):
        inner_ring_list = []
        self.change_position('y', 1)
        for i in range(len(self.inner_ring_dim)):
            inner_ring_list.append(self.change_position(self.inner_ring_dim[i], self.inner_ring_steps[i]))
        return inner_ring_list

    def select_mouse_movement(self):
        '''For testing, select a position mouse chooses to land on around the animal platform'''
        available_moves = [[1, 0, -1], [1, -1, 0], [0, -1, 1], [-1, 0, 1], [-1, 1, 0], [0, 1,-1]]
        # def adding function between animal robot and this list to get list of available moves
        # available_moves.remove(self.platform_robot.position_vector)
        available_moves.remove(self.position_vector)
        return rand.choice(available_moves)


    def change_rotation(self, change):
        '''Change the encoded orientation of the platform. Is between 0-2'''
        self.rotation += change
        return self.rotation // 3

    def change_position(self, dimension, step):
        '''Move position vector around the board'''
        rotation_check = self.dimension_dict[dimension]
        if self.rotation != dimension:
            change = self.dimension_dict[dimension] - self.rotation
            self.change_rotation(change)
        x, y, z = self.position_vector
        if dimension == 'x' and self.rotation == rotation_check:
            y += step
            z -= step
            self.position_vector = [x, y, z]
            return [self.position_vector, self.rotation]
        elif dimension == 'y' and self.rotation == rotation_check:
            x += step
            z -= step
            self.position_vector = [x, y, z]
            return [self.position_vector, self.rotation]
        elif dimension == 'z' and self.rotation == rotation_check:
            x += step
            y -= step
            self.position_vector = [x, y, z]
            return [self.position_vector, self.rotation]
        else:
            print('ERROR: Select correct dimension, either x, y, z')

class MazeRobot(PlatformRobot):
    '''Class for the platform without the animal on it'''

    def __init__(self, x, y, z, rotation):
        super().__init__(x, y, z, rotation)
        # for defining the boundaries of the maze
        self.maze = None
        # for encoding position relative to animal robot
        self.animal_robot = None
        self.platform_robot = None
        self.animal_goal = None
        self.rel_position = self.get_relative_position(self.position_vector)
        # for precession method
        self.clockwise_dim = ['x', 'y', 'z', 'x', 'y', 'z']
        self.two_clockwise_step = [-2, -2, -2, 2, 2, 2]
        # self.one_clockwise_step = [-1, -1, -1, 1, 1, 1]
        self.anticlockwise_dim = ['z', 'x', 'y', 'z', 'x', 'y']
        self.two_anticlockwise_step = [-2, 2, 2, 2, -2, -2]
        # self.one_anticlockwise_step = [1, 1, 1, -1, -1, -1]
        # for moving in and out of outer ring
        self.ring_dim = ['y', 'z', 'x', 'y', 'z', 'x']
        self.inner_ring_steps = [-1, -1, 1, 1, 1, -1]
        self.outer_ring_steps = [1, 1, -1, -1, -1, 1]
        # move list for robot steps
        self.move_list = None

    def set_platform_robot(self, non_animal_robot_class):
        self.platform_robot = non_animal_robot_class

    def set_animal_robot(self, animal_robot_class):
        self.animal_robot = animal_robot_class

    def set_maze(self, maze_class):
        self.maze = maze_class

    def set_animal_goal(self, animal_goal_class):
        self.animal_goal = animal_goal_class

    def set_move_list(self):
        # self.move_list =
        pass

    def get_relative_animal_vector(self):
        '''Return vector between two the animal_robot and robot'''
        return [a - b for a, b in zip(self.animal_robot.position_vector, self.position_vector)]

    def get_relative_position(self, vector):
        '''gets the relative position (encoded) between the animal and platform robot'''
        x = vector[0]
        y = vector[1]
        z = vector[2]
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
            print('Robot is off axis (its position is invalid because it is off axis), or robot is at origin')

    def change_position(self, dimension, step):
        '''Move position vector around the board'''
        rotation_check = self.dimension_dict[dimension]
        if self.rotation != dimension:
            change = self.dimension_dict[dimension] - self.rotation
            self.change_rotation(change)
        x, y, z = self.position_vector
        if dimension == 'x' and self.rotation == rotation_check:
            y += step
            z -= step
            self.position_vector = [x, y, z]
            return [self.position_vector, self.rotation]
        elif dimension == 'y' and self.rotation == rotation_check:
            x += step
            z -= step
            self.position_vector = [x, y, z]
            return [self.position_vector, self.rotation]
        elif dimension == 'z' and self.rotation == rotation_check:
            x += step
            y -= step
            self.position_vector = [x, y, z]
            return [self.position_vector, self.rotation]
        else:
            print('ERROR: Select correct dimension, either x, y, z')

    def get_platform_rel_position_difference(self, vector):
        '''Gets the difference in rel_position between the non animal platform's position and the rel_position of the
         non animal platform's desired position'''
        platform_rel_position = self.get_relative_position(self.get_relative_animal_vector())
        target_platform_position = self.get_relative_position(vector)
        return target_platform_position - platform_rel_position

    def choose_precess_direction(self, vector):
        '''Deciedes whether to move clockwise or anticlockwise around the maze'''
        clockwise_steps = self.get_platform_rel_position_difference(vector)
        if clockwise_steps == 0:
            print('no movement required')
        elif 0 < clockwise_steps < 3:
            return True
        elif 3 < clockwise_steps < 6:
            return False
        elif clockwise_steps == 3:
            print('choose another way to deicde of direction of precess')
        else:
            print("haven't handled when rel_position < 6")

    def move_to_outer_ring(self):
        '''move to outer ring'''
        outer_ring_move = [
            self.change_position(self.ring_dim[self.rel_position],
                                 self.outer_ring_steps[self.rel_position])]
        return outer_ring_move

    def move_to_inner_ring(self):
        '''move to inner ring'''
        inner_ring_move = [
            self.change_position(self.ring_dim[self.rel_position], self.inner_ring_steps[self.rel_position])]
        return inner_ring_move

    def precession(self, clockwise, steps, ):
        '''direction of precession, start position, and number of steps'''
        precession_values = []
        print('no of steps in precession:', steps)
        if clockwise == True:
            # precess clockwise
            for i in range(0, steps):
                self.position_vector = self.change_position(self.clockwise_dim[self.rel_position],
                                                            self.two_clockwise_step[self.rel_position])
                precession_values.append(self.position_vector)
        elif not clockwise:
            # precess anticlockwise
            for i in range(0, steps):
                self.position_vector = self.change_position(self.anticlockwise_dim[self.rel_position],
                                                            self.two_anticlockwise_step[self.rel_position])
                precession_values.append(self.position_vector)
        else:
            print('select direction of precession')
        return precession_values

    def get_path(self, target_vector):
        '''Gets the path between the current position of the robot to the target position of the robot'''
        # move to outer ring
        move_to_outer_ring = self.move_to_outer_ring()
        self.see_status()
        # precess around outer ring
        clockwise = self.choose_precess_direction(target_vector)
        steps = self.get_platform_rel_position_difference(target_vector)
        if clockwise == True:
            steps = steps
        elif clockwise == False:
            steps = 6 - steps
        print('Clockwise:', clockwise,
              '\nSteps:', steps,
              '\nStart:', self.position_vector)
        precess = self.precession(clockwise, steps)
        # move to inner ring
        # *precess, *move_to_inner_ring
        move_to_inner_ring = self.move_to_inner_ring()
        return [*move_to_outer_ring, *precess, *move_to_inner_ring]

    def see_status(self):
        '''Get summary information about robot'''
        super().see_status()
        print(
            f'Relative Position: {self.rel_position}\n'
        )

    def is_in_maze(self):
        '''Makes sure the movement path does not leave the arena'''
        if self.move_list in self.maze.valid_moves:
            return True
        if self.move_list not in self.maze.valid_moves:
            print('ERROR: Robot Path is out of bounds')
            return False

    def is_not_inside_other_robots(self):
        '''Check if the current position of the robot intersects with the position of another robot'''
        if self.position_vector == self.animal_robot.position_vector:
            print('ERROR: Robot is in Animal Robot')
            return False
        elif self.position_vector == self.platform_robot.postion_vector:
            print('ERROR: Robot is in NonAnimalRobot')
            return False
        elif self.position_vector == self.animal_goal.position_vector:
            print('ERROR: Robot is in AnimalGoal')
            return False
        else:
            return True


class AnimalGoal(PlatformRobot):
    '''Class of platform robot with the goal on it'''

    def __init__(self, x, y, z, rotation):
        super().__init__(x, y, z, rotation)


def main():
    pr = AnimalRobot(0,0,0,'x')
    print(
        # pr.get_inner_ring(),
        pr.get_new_animal_positions())
    inner_ring = [[1, 0, -1], [1, -1, 0], [0, -1, 1], [-1, 0, 1], [-1, 1, 0], [0, 1, -1]]
    outer_list = [[2, 0, -2], [2, -2, 0], [0, -2, 2], [-2, 0, 2], [-2, 2, 0], [0, 2, -2]]


if __name__ == '__main__':
    main()
