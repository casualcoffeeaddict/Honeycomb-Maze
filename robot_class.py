from hexagon_map import *
import random as rand

class PlatformRobot():
    '''Class for moving platform around'''

    def __init__(self, x, y, z, rotation):
        # for rotation change method
        self.dimension_dict = {'x': 0, 'y': 1, 'z': 2}
        # location information about platform
        self.x = x
        self.y = y
        self.z = z
        self.position_vector = [x, y, z]
        self.rotation = self.dimension_dict[rotation]

    def change_rotation(self, change):
        '''change is between 0-2'''
        self.rotation += change
        return self.rotation // 3

    def change_position(self, dimension, step):
        rotation_check = self.dimension_dict[dimension]
        if self.rotation != dimension:
            change = self.dimension_dict[dimension] - self.rotation
            self.change_rotation(change)
        if dimension == 'x' and self.rotation == rotation_check:
            self.y = self.y + step
            self.z = self.z - step
            return [[self.x, self.y, self.z], self.rotation]
        elif dimension == 'y' and self.rotation == rotation_check:
            self.x = self.x - step
            self.z = self.z + step
            return [[self.x, self.y, self.z], self.rotation]
        elif dimension == 'z' and self.rotation == rotation_check:
            self.x = self.x + step
            self.y = self.y - step
            return [[self.x, self.y, self.z], self.rotation]
        else:
            print('select correct dimension: x, y, z')


class AnimalRobot(PlatformRobot):
    '''Class for the platform with the animal on it'''

    def __init__(self, x, y, z, rotation, goal_platform_class):
        super().__init__(x, y, z, rotation)
        self.goal = goal_platform_class

    def check_if_animal_at_goal(self):
        if self.goal.position_vector == self.position_vector:
            return True
        elif self.goal.position_vector != self.position_vector:
            return False


class NonAnimalRobot(PlatformRobot):
    '''Class for the platform without the animal on it'''

    def __init__(self, x, y, z, rotation, animal_robot_class, *platform_robot_class):
        super().__init__(x, y, z, rotation)
        # for encoding position relative to animal robot
        self.animal_robot = animal_robot_class
        self.platform_robot = platform_robot_class
        self.rel_position = self.get_relative_position([self.x, self.y, self.z])
        # for precession method
        self.clockwise_dim = ['x', 'y', 'z', 'x', 'y', 'z']
        self.two_clockwise_step = [-2, -2, -2, 2, 2, 2]
        self.one_clockwise_step = [-1, -1, -1, 1, 1, 1]
        self.anticlockwise_dim = ['z', 'x', 'y', 'z', 'x', 'y']
        self.two_anticlockwise_step = [-2, -2, -2, 2, 2, 2]
        self.one_anticlockwise_step = [1, 1, 1, -1, -1, -1]
        # for moving in and out of outer ring
        self.ring_dim = ['y', 'z', 'x', 'y', 'z', 'x']
        self.inner_ring_steps = [-1, -1, -1, 1, 1, 1]
        self.outer_ring_steps = [-1, -1, -1, 1, 1, 1]

    def get_relative_animal_vector(self):
        '''gets the vector between the animal robot and the platform robot'''
        return (self.x - self.animal_robot.x,
                self.y - self.animal_robot.y,
                self.z - self.animal_robot.z)

    def get_relative_position(self, vector):
        'gets the relative position (encoded) between the animal and platform robot'
        x = vector[0]
        y = vector[1]
        z = vector[2]
        if y == 0 and x > 0:
            return 0
        elif z == 0 and x > 0:
            return 1
        elif x == 0 and z > 0:
            return 2
        elif y == 0 and x < 0:
            return 3
        elif z == 0 and x < 0:
            return 4
        elif x == 0 and z < 0:
            return 5
        else:
            print('Robot is off axis (its position is invalid because it is off axis)')

    def get_platform_rel_position_difference(self, vector):
        '''Gets the difference in rel_position between the non animal platform's position and the rel_position of the
         non animal platform's desired position'''
        platform_rel_position = self.get_relative_position(self.get_relative_animal_vector())
        target_platform_position = self.get_relative_position(vector)
        return target_platform_position - platform_rel_position

    def choose_precess_direction(self, vector):
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

    def change_position(self, dimension, step):
        # self.rel_position = self.get_relative_position()
        return PlatformRobot.change_position(self, dimension, step)

    def move_to_outer_ring(self):
        '''move to outer ring'''
        outer_ring_move = []
        outer_ring_move.append(
            self.change_position(self.ring_dim[self.rel_position], self.outer_ring_steps[self.rel_position])
        )
        return outer_ring_move

    def move_to_inner_ring(self):
        '''move to inner ring'''
        inner_ring_move = []
        inner_ring_move.append(
            self.change_position(self.ring_dim[self.rel_position], self.inner_ring_steps[self.rel_position])
        )
        return inner_ring_move

    def precession(self, clockwise, steps):
        '''direction of precession, start position, and number of steps'''
        precession_values = []
        if clockwise == True:
            # precess clockwise
            for i in range(0, steps):
                precession_values.append(
                    self.change_position(self.clockwise_dim[self.rel_position],
                                         self.two_clockwise_step[self.rel_position])
                )
                self.rel_position += 1
                print(self.rel_position, self.clockwise_dim[self.rel_position], self.two_clockwise_step[self.rel_position])
                if self.rel_position == 6:
                    self.rel_position = 0

        elif clockwise == False:
            # precess anticlockwise
            for i in range(0, steps):
                precession_values.append(
                    self.change_position(self.anticlockwise_dim[self.rel_position],
                                         self.two_anticlockwise_step[self.rel_position])
                )
                self.rel_position -= 1
                if self.rel_position == -1:
                    self.rel_position = 5
        return precession_values

    # Precession anti-clockwise doesnt work
    def get_path(self, target_vector):
        # move to outer ring
        move_to_outer_ring = self.move_to_outer_ring()
        # precess around outer ring
        clockwise = self.choose_precess_direction(target_vector)
        steps = self.get_platform_rel_position_difference(target_vector)
        if clockwise == True:
            steps = steps
        elif clockwise == False:
            steps = 6 - steps
        print('Clockwise:', clockwise,
              '\nSteps:',steps,
              '\nStart:', self.position_vector)
        precess = self.precession(clockwise, steps)
        # move to inner ring
        # *precess, *move_to_inner_ring
        move_to_inner_ring = self.move_to_inner_ring()
        return [*move_to_outer_ring, *precess, *move_to_inner_ring]

    def select_mouse_movement(self):
        '''For testing, select a position mouse chooses to land on around the animal platform'''
        available_moves = [[1, 0, -1], [1, -1, 0], [0, -1, 1], [-1, 0, 1], [-1, 1, 0], [0, 1, -1]] # def adding function between animal robot and this list to get list of available moves
        # available_moves.remove(self.platform_robot.position_vector)
        available_moves.remove(self.position_vector)
        return rand.choice(available_moves)


class AnimalGoal(PlatformRobot):
    '''Class of platform robot with the goal on it'''

    def __init__(self, x, y, z, rotation):
        super().__init__(x, y, z, rotation)


def main():
    ag = AnimalGoal(0, 0, 0, 'x')
    ar = AnimalRobot(0, 0, 0, 'x', ag)
    nar = NonAnimalRobot(1, 0, -1, 'x', ar)
    nar2 = NonAnimalRobot(1, 0, -1, 'x', ar, nar)
    list = [[2, 0, -2], [2, -2, 0], [0, -2, 2], [-2, 0, 2], [-2, 2, 0], [0, 2, -2]]

    print(
        ar.check_if_animal_at_goal()
          )

if __name__ == '__main__':
    main()
