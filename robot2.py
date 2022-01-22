'''Robot Class'''
from robot import PlatformRobot

class MazeRobot(PlatformRobot):
    def __init__(self):
        super().__init__(x, y, z, rotation)
        # for defining the boundaries of the maze
        self.maze = None
        # for pointing to other parts of the maze (other robots and goal)
        self.is_animal_robot = None
        self.platform_robot = None
        self.animal_goal = None
        self.goal = None
        self.non_animal_robot_1 = None
        self.non_animal_robot_2 = None

        # non animal robot's next position information
        self.next_platform_goal_1 = None
        self.next_platform_goal_2 = None

        # move list for robot steps
        self.move_list = None

        # rel position of robot for movement of robot
        self.rel_position = self.get_relative_position([self.x, self.y, self.z])

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

    def is_valid_position_change(self):
        x_pos = [4,5,0]
        x_neg = [1,2,3]
        y_pos = [5,0,1]
        y_neg = [2,3,4]
        z_pos = [0,1,2]
        z_neg = [3,4,5]
        if self.rotation == 0:
            # move x dim
            
        elif self.rotation == 1:
            # move y dim
        elif self.rotation == 2:
            # move z dim