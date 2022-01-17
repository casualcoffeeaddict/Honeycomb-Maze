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

    def rel_rotation_change(self, change):
        '''change is between 0-2'''
        self.rotation += change
        return self.rotation // 3

    def move_position(self, dimension, step):
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



    # def find_path(self, fx, fy, fz):
    #     # move to outer ring
    #     outer_ring_move = self.move_to_outer_ring()
    #     # Precession
    #     clockwise_steps = len(self.clockwise_step(True, ))
    #     anticlockwise_steps = len(self.clockwise_step(False, ))
    #     # decide on clockwise or anticlockwise movement
    #     if clockwise_steps < anticlockwise_steps:
    #         direction_of_precess = True
    #     elif clockwise_steps > anticlockwise_steps:
    #         direction_of_precess = False
    #     elif clockwise_steps == anticlockwise_steps:
    #     ## The direction must be opposite to the other robots
    #         precess_steps = int(final_rel_position - self.rel_position)
    #     # Final position needs its own rel position to the animal platform
    #     # From this the precess steps can be calculated
    #     # Moving clockwise around 4 is the same as anticlockwise 2
    #     # Therefore clockwise
    #     precesssion_values = self.precession(clockwise=direction_of_precess, steps=precess_steps)
    #     inner_ring_move = self.move_to_inner_ring()

        # combine move list
        # return [*outer_ring_move, *precesssion_values, *inner_ring_move]


class AnimalRobot(PlatformRobot):
    '''Class for the platform with the animal on it'''
    def __init__(self):
        pass


class NonAnimalRobot(PlatformRobot):
    '''Class for the platform without the animal on it'''
    def __init__(self, AnimalRobot, rel_position):
        # for encoding position relative to animal robot
        self.rel_position = rel_position  # position around the hexagonal ring of the animal robot: between 0-5 where 0 = NE, 1 = E ...
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

    def position(self):
        return self.animalrobot

    def find_ainimal_platform(self):
        '''takes position of animal robot, converts it to start position, a number in the range 0-5, which are the
        verticies of a hexagon'''
        self.rel_position = start

    def move_to_outer_ring(self):
        '''move to outer ring'''
        outer_ring_move = []
        outer_ring_move.append(
            self.move(self.ring_dim[self.rel_position], self.outer_ring_steps[self.rel_position])
        )
        return outer_ring_move

    def move_to_inner_ring(self):
        '''move to inner ring'''
        inner_ring_move = []
        inner_ring_move.append(
            self.move(self.ring_dim[self.rel_position], self.inner_ring_steps[self.rel_position])
        )
        return inner_ring_move

    def precession(self, clockwise, steps):
        '''direction of precession, start position, and number of steps'''
        precession_values = []
        if clockwise == True:
            # precess clockwise
            for i in range(0, steps):
                precession_values.append(
                    self.move_position(self.clockwise_dim[self.rel_position], self.clockwise_step[self.rel_position])
                )
                self.rel_position += 1
                if self.rel_position == 6:
                    self.rel_position = 0

        elif clockwise == False:
            # precess anticlockwise
            for i in range(0, steps):
                precession_values.append(
                    self.move_position(self.anticlockwise_dim[self.rel_position], self.anticlockwise_step[self.rel_position])
                )
                self.rel_position += 1
                if self.rel_position == 6:
                    self.rel_position = 0

        return precession_values


class AnimalGoal(PlatformRobot):
    '''Class with the goal on it'''
    def __init__(self):
        pass

def main():
    ar = AnimalRobot(0,0,0,'x',)
    nar = NonAnimalRobot()

    print(nar.position())

if __name__ == '__main__':
    main()