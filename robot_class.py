from hexagon_map import *

class PlatformRobot():
    '''Class for moving platform around'''
    def __init__(self, x, y, z, rotation):
        # for rotation change method
        self.dimension_dict = {'x': 0, 'y': 1, 'z': 2}
        # location information about platform
        self.x = x
        self.y = y
        self.z = z
        self.rotation = self.dimension_dict[rotation]

    def change_rotation(self, change):
        '''change is between 0-2'''
        self.rotation += change
        return self.rotation // 3

    def change_position(self, dimension, step):
        rotation_check = self.dimension_dict[dimension]
        if self.rotation != dimension:
            change = self.dimension_dict[dimension] - self.rotation
            self.rel_rotation_change(change)
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
    def __init__(self, x, y, z, rotation):
        super().__init__(x, y, z, rotation)


class NonAnimalRobot(PlatformRobot):
    '''Class for the platform without the animal on it'''
    def __init__(self, x, y, z, rotation, AnimalRobot, rel_position, ):
        super().__init__(x, y, z, rotation)
        # for encoding position relative to animal robot
        self.rel_position_dict = {'NE':0, 'E':1, 'SE':2, 'SW':3, 'W':4, 'NW':5}
        self.rel_position = self.rel_position_dict[rel_position]  # position around the hexagonal ring of the animal robot:
        self.animalrobot = AnimalRobot
        # for precession method
        self.clockwise_dim = ['x', 'y', 'z', 'x', 'y', 'z']
        self.clockwise_step = [-2, -2, -2, 2, 2, 2]
        self.anticlockwise_dim = ['z', 'x', 'y', 'z', 'x', 'y']
        self.anticlockwise_step = [2, 2, 2, -2, -2, -2]
        # for moving in and out of outer ring
        self.ring_dim = ['y', 'z', 'x', 'y', 'z', 'x']
        self.outer_ring_steps = [1, 1, 1, -1, -1, -1]
        self.inner_ring_steps = [-1, -1, -1, 1, 1, 1]

    def get_relative_animal_vector(self):
        return (self.x-self.animalrobot.x,
                self.y-self.animalrobot.y,
                self.z-self.animalrobot.z)

    def get_relative_position(self):
        vector_to_cardinal = {(1,0,-1): 0, (1,-1,0): 1, (0,-1,1):2, (-1,0,1):3, (-1, 1, 0):4, (0,1,-1):5}
        return vector_to_cardinal[self.get_relative_animal_vector()]

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
                    self.change_position(self.clockwise_dim[self.rel_position], self.clockwise_step[self.rel_position])
                )
                self.rel_position += 1
                if self.rel_position == 6:
                    self.rel_position = 0

        elif clockwise == False:
            # precess anticlockwise
            for i in range(0, steps):
                precession_values.append(
                    self.change_position(self.anticlockwise_dim[self.rel_position], self.anticlockwise_step[self.rel_position])
                )
                self.rel_position += 1
                if self.rel_position == 6:
                    self.rel_position = 0

        return precession_values


class AnimalGoal(PlatformRobot):
    '''Class of platform robot with the goal on it'''
    def __init__(self, x, y, z, rotation):
        super().__init__(x, y, z, rotation)


def main():
    ar = AnimalRobot(0,0,0,'x')
    nar = NonAnimalRobot(0,-1,1,'x', ar, 'NE')

    print(nar.get_relative_position())

if __name__ == '__main__':
    main()