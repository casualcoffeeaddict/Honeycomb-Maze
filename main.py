'''Main Maze program that will move the robots around'''

from hexagon_map import *

class PlatformRobot():
    def __init__(self, x, y, z, rotation,  rel_position):
        # location information about platform
        self.x = x
        self.y = y
        self.z = z
        self.rotation = rotation
        self.rel_position = rel_position
        # for rotation change method
        self.dimension_dict = {'x': 0, 'y':1, 'z':2}
        # for precession method
        self.clockwise_dim = ['x', 'y', 'z', 'x', 'y', 'z']
        self.clockwise_step = [-2, -2, -2, 2, 2, 2]
        self.anticlockwise_dim = ['z', 'x', 'y', 'z', 'x', 'y']
        self.anticlockwise_step = [2, 2, 2, -2, -2, -2]
        # for moving in and out of outer ring
        self.ring_dim = ['y', 'z', 'x', 'y', 'z', 'x']
        self.outer_ring_steps = [1, 1, 1, -1, -1, -1]
        self.inner_ring_steps = [-1, -1, -1, 1, 1, 1]

    def find_ainimal_platform(self):
        '''takes position of animal robot, converts it to start position, a number in the range 0-5, which are the
        verticies of a hexagon'''
        self.rel_position =  start

    def rel_rotation_change(self, change):
        '''change is between 0-2'''
        self.rotation += change
        return self.rotation//3

    def move(self, dimension, step):
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
            #error!

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
                    self.move(self.clockwise_dim[self.rel_position], self.clockwise_step[self.rel_position])
                )
                self.rel_position += 1
                if self.rel_position == 6:
                    self.rel_position = 0

        elif clockwise == False:
            # precess anticlockwise
            for i in range(0, steps):
                precession_values.append(
                    self.move(self.anticlockwise_dim[self.rel_position], self.anticlockwise_step[self.rel_position])
                )
                self.rel_position += 1
                if self.rel_position == 6:
                    self.rel_position = 0

        return precession_values

    def find_path(self, final_position):
        outer_ring_move = self.move_to_outer_ring()
        # decide on clockwise or anticlockwise movement
        if steps
        direction_of_precess = bool()
        steps = int(final_rel_position - self.rel_position)
        precesssion_values = self.precession(clockwise=direction_of_precess, steps=steps)
        inner_ring_move = self.move_to_inner_ring()

        # combine move list
        return [*outer_ring_move, *precesssion_values, *inner_ring_move]




# Check whether the intersection between the rings (list) are part of the target platform

# def intersection(platform_robot1, platform_robot2):
#     '''check the paths of the platform robots do not intersect'''
#     if path_between_points is in :
#         # robot paths do not intersect
#         return True
#     else:
#         # robot paths do intersect
#         return False

def reassign_robots():
    '''Changes the names of the robots to work with the program'''
    # animal_robot =
    # platform_robot1 =
    # platform_robot2 =
    pass

outer_ring_movement_vectors = [Hex(2,0,-2), Hex(2,-2,0), Hex(0,-2,2), Hex(-2,0,2), Hex(-2,2,0), Hex(0,2,-2)]







# def main():
#     '''Main loop of code'''
#     # STARTING POSITIONS
#     animal_robot = Hex(0,0,0)
#     platform_robot1 = Hex(-1,0,1)
#     platform_robot2 = Hex(0,-1,1)
#     while animal_robot != goal_platform:
#         # get the new locations (from the inner ring from the location of the animal's choice)
#         newplatform1, newplatform2 = select_target_location(animal_robot, platform_robot1, platform_robot2).split()
#         # send the robot from the inner ring to the outer ring
#         movement_direction_robot1 = hex_subtract(animal_robot, platform_robot1)
#         outer_ring_position_robot1 = hex_add(platform_robot1, movement_direction_robot1)
#
#         movement_direction_robot2 = hex_subtract(animal_robot, platform_robot2)
#         outer_ring_position_robot2 = hex_add(platform_robot2, movement_direction_robot2)
#         # get the path from location in the outer ring to the required location in the outer ring
#         # travel around middle rings to the desired location
#         # Check whether the intersection between the rings of both the paths that exist intersect
#         if intersection(platform_robot1, platform_robot2) == False:
#             # send the code to ssh
#         # get input from the DLC reassignment
#     pass

def object_main():
    pr = PlatformRobot(0 , 0 , 0, rel_position=0)
    print(pr.precession(clockwise=True, 7))

if __name__ == '__main__':
    object_main()