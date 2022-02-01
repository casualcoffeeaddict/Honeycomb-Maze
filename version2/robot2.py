"""Robot Class"""


class PlatformRobot:
    def __init__(self, x, y, z, direction, *name):
        # (Optional) identity of Robot
        self.name = name
        # Orientation of robot
        self.position_vector = [x, y, z]
        self.direction = direction
        # Identifies robot with animal on it
        self.is_animal_robot = None
        # Target positions on the network
        self.target_position = None
        # Path robot takes
        self.move_list = None
        # Maze robot is placed in
        self.maze = None

        # For moving to and from inner and outer ring
        self.ring_dim = ['y', 'z', 'x', 'y', 'z', 'x']
        self.inner_ring_steps = [-1, -1, 1, 1, 1, -1]
        self.outer_ring_steps = [1, 1, -1, -1, -1, 1]

    def set_maze(self, maze_class):
        """Set the maze in which the robot is in"""
        self.maze = maze_class
        self.maze.add_robot(self)

    def set_animal_robot(self, bool):
        """Set the robot which has the animal on it"""
        self.is_animal_robot = bool
        # also set the non-animal robot to self.is_animal_robot to no bool
        for robot in range(len(self.maze.robot_list)):
            if robot is not self:
                robot.is_animal_robot = not bool

    def change_direction(self):
        """Change the direction of the robot, based on whether this movement is allowed by maze"""
        # If positions consecutive to the robot , in the maze class, are available,
        # then a rotation change can take place
        pass

    def change_position(self, dimension, step):
        """Move position vector around the board"""
        rotation_check = self.dimension_dict[dimension]
        print('change position, self.position_vector', self.position_vector)
        if self.rotation != dimension:
            change = self.dimension_dict[dimension] - self.rotation
            self.change_rotation(change)
        x = self.position_vector[0]
        y = self.position_vector[1]
        z = self.position_vector[2]
        if dimension == 'x' and self.rotation == rotation_check:
            y += step
            z -= step
            self.position_vector = [x, y, z]
            return self.position_vector
        elif dimension == 'y' and self.rotation == rotation_check:
            x += step
            z -= step
            self.position_vector = [x, y, z]
            return self.position_vector
        elif dimension == 'z' and self.rotation == rotation_check:
            x += step
            y -= step
            self.position_vector = [x, y, z]
            return self.position_vector
        else:
            print('ERROR: Select correct dimension, either x, y, z')

    def get_target_position(self):
        animal_robot_position_vector = self.maze.get_animal_robot_position_vector()
        choices = self.maze.get_consecutive_coordinates(animal_robot_position_vector)

        # remove positions of the animal coordinates

        choices.choose()


    def relative_position(self, ar_position_vector, nar_position_vector):
        """Get the relative position between two points"""


    def update_relative_direction(self):
        """Get the direction of the robot (from 0 to 5)"""
        pass

    def move_to_outer_ring(self):
        """Move to outer ring"""
        outer_ring_move = [
            self.change_position(self.ring_dim[self.relative_position],
                                 self.outer_ring_steps[self.relative_position])]
        return outer_ring_move

    def move_to_inner_ring(self):
        """Move to inner ring"""
        inner_ring_move = [
            self.change_position(self.ring_dim[self.relative_position], self.inner_ring_steps[self.relative_position])]
        return inner_ring_move

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

    def make_command_list(self):
        """From the move list convert it to a set of commands to be sent to the associated robot"""
        pass

    def send_command_list(self):
        """Send the commands via the ssh import to the self robot"""
        pass