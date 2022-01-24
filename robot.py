'''Robot classes and their functions for hexagon maze'''
# import random as rand
#
class PlatformRobot():
    '''Base platform class and basic moving functions'''

    def __init__(self, x, y, z, rotation):
        # for rotation change method
        self.dimension_dict = {'x': 0, 'y': 1, 'z': 2}
        # location information about platform
        self.position_vector = [x, y, z]
        self.rotation = self.dimension_dict[rotation]

    def see_status(self):
        '''Get summary information about robot'''
        print(
            '\nStatus:'
            '\nPostion Vector:', self.position_vector,
            '\nRotation:', self.rotation
        )

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

    def __init__(self, x, y, z, rotation, name):
        super().__init__(x, y, z, rotation)
        self.name = name
        # for defining the boundaries of the maze
        self.maze = None
        # for encoding position relative to animal robot
        self.animal_robot = None
        self.non_animal_robot = None
        self.animal_goal = None
        self.rel_position = self.get_relative_position(self.position_vector)
        # for precession method
        self.precession_direction = None
        self.clockwise_dim = ['x', 'y', 'z', 'x', 'y', 'z']
        self.clockwise_step = [-1, -1, -1, 1, 1, 1]
        self.anticlockwise_dim = ['z', 'x', 'y', 'z', 'x', 'y']
        self.anticlockwise_step = [-1, 1, 1, 1, -1, -1]
        # for moving in and out of outer ring
        self.ring_dim = ['y', 'z', 'x', 'y', 'z', 'x']
        self.inner_ring_steps = [-1, -1, 1, 1, 1, -1]
        self.outer_ring_steps = [1, 1, -1, -1, -1, 1]
        # move list for robot steps
        self.move_list = None

    def set_non_animal_robot(self, non_animal_robot_class):
        self.non_animal_robot = non_animal_robot_class

    def set_animal_robot(self, animal_robot_class):
        self.animal_robot = animal_robot_class

    def set_maze(self, maze_class):
        self.maze = maze_class

    def set_animal_goal(self, animal_goal_class):
        self.animal_goal = animal_goal_class

    def set_move_list(self):
        # self.move_list =
        pass

    def add_initial_position_to_list(self):
        return self.move_list.append(0, self.position_vector)

    def get_relative_animal_vector(self):
        '''Return vector between two the animal_robot and robot'''
        return [a - b for a, b in zip(self.animal_robot.position_vector, self.position_vector)]

    def get_relative_position(self, vector):
        '''gets the relative position (encoded) between the animal and platform robot'''
        if self.animal_robot != None:
            x = vector[0] - self.animal_robot.position_vector[0]
            y = vector[1] - self.animal_robot.position_vector[1]
            z = vector[2] - self.animal_robot.position_vector[2]
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
                print(f'The robot {self} is off axis (its position is invalid because it is off axis), or robot is at origin.')

    def platform_is_in_maze(self):
        '''Check if the position of the platform robot is inside the maze the robot is in'''
        print()
        if self.maze != None:
            if self.position_vector in self.maze.valid_moves:
                return True
            if self.position_vector not in self.maze.valid_moves:
                print(f'ERROR: The platform, {self}, is not in the maze')
                return False

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
        platform_rel_position = self.get_relative_position(self.position_vector)
        target_platform_position = self.get_relative_position(vector)
        print('target_platform_position', target_platform_position, 'platform_rel_position', platform_rel_position)
        return (target_platform_position - platform_rel_position)%6

    def choose_precess_direction(self, vector):
        '''Deciedes whether to move clockwise or anticlockwise around the maze'''
        clockwise_steps = self.get_platform_rel_position_difference(vector)
        print(clockwise_steps)
        if clockwise_steps == 0:
            print('no movement required, however other non-animal robot must move opposite the long way around')
            # self.non_animal_robot.precession_direction = self.non_animal_robot.choose_precess_direction
        elif 0 < clockwise_steps < 3:
            self.precession_direction = True
        elif 3 < clockwise_steps < 6:
            self.precession_direction = False
        elif clockwise_steps == 3:
            print('must not be what the other robot has to do')
            self.precession_direction = not self.non_animal_robot.choose_precess_direction
        else:
            print("haven't handled when rel_position < 6")
        return self.precession_direction

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

    def precession(self, clockwise, precess_steps, precess_radius):
        '''direction of precession, start position, and number of steps'''
        precession_values = []
        print('no of steps in precession:', precess_steps)
        if clockwise == True:
            # precess clockwise
            for i in range(0, precess_steps):
                self.position_vector = self.change_position(self.clockwise_dim[self.rel_position],
                                                            self.clockwise_step[self.rel_position * precess_radius])
                precession_values.append(self.position_vector)
        elif not clockwise:
            # precess anticlockwise
            for i in range(0, precess_steps):
                self.position_vector = self.change_position(self.anticlockwise_dim[self.rel_position],
                                                            self.anticlockwise_step[self.rel_position * precess_radius])
                precession_values.append(self.position_vector)
        else:
            print('select direction of precession')
        return precession_values

    def get_inner_ring_path(self, target_position):
        '''Gets the path between the inner ring of the robot to the target position '''
        # move to outer ring
        move_to_outer_ring = self.move_to_outer_ring()
        # precess around outer ring
        clockwise = self.choose_precess_direction(target_position)
        precess_steps = self.get_platform_rel_position_difference(target_position)
        if clockwise == True:
            precess_steps = precess_steps
        elif clockwise == False:
            precess_steps = 6 - precess_steps
        print('Clockwise:', clockwise,
              '\nSteps:', precess_steps,
              '\nStart:', self.position_vector)
        precess = self.precession(clockwise, precess_steps, precess_radius=2)
        # move to inner ring
        move_to_inner_ring = self.move_to_inner_ring()
        return [*move_to_outer_ring, *precess, *move_to_inner_ring]

    def get_outer_ring_path(self, target_position):
        '''Get's path from outer ring to the desired position'''
        # precess around outer ring
        clockwise = self.choose_precess_direction(target_position)
        precess_steps = self.get_platform_rel_position_difference(target_position)
        if clockwise == True:
            precess_steps = precess_steps
        elif clockwise == False:
            precess_steps = 6 - precess_steps
        print('Clockwise:', clockwise,
              '\nSteps:', precess_steps,
              '\nStart:', self.position_vector)
        precess = self.precession(clockwise, precess_steps, precess_radius=2)
        # move to inner ring
        move_to_inner_ring = self.move_to_inner_ring()
        return [*precess, *move_to_inner_ring]

    def get_path(self):
        '''chooses between going from the inner ring and the outer ring based on the current location '''
        animal_vector = self.get_relative_animal_vector()
        inner_ring = [[1, 0, -1], [1, -1, 0], [0, -1, 1], [-1, 0, 1], [-1, 1, 0], [0, 1, -1]]
        outer_list = [[2, 0, -2], [2, -2, 0], [0, -2, 2], [-2, 0, 2], [-2, 2, 0], [0, 2, -2]]
        if animal_vector in inner_ring:
            self.get_inner_ring_path()
        elif animal_vector in outer_list:
            self.get_outer_ring_path()
        else:
            print('ERROR: The animal is outside the a radius of two from the animal robot')
            
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
        elif self.position_vector == self.non_animal_robot.postion_vector:
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

    inner_ring = [[1, 0, -1], [1, -1, 0], [0, -1, 1], [-1, 0, 1], [-1, 1, 0], [0, 1, -1]]
    outer_list = [[2, 0, -2], [2, -2, 0], [0, -2, 2], [-2, 0, 2], [-2, 2, 0], [0, 2, -2]]


if __name__ == '__main__':
    main()
