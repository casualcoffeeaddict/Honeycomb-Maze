"""Maze class for the robot to move around in"""
import networkx as nx

class HexagonGrid:
    """Base maze class which defines the area of the maze"""

    def __init__(self, column_number, row_number):
        self.columns = column_number
        self.rows = row_number


class HexagonMaze(HexagonGrid):
    """Maze area for hexagonal platform"""

    def __init__(self, column_number, row_number):
        super().__init__(column_number, row_number)
        # self.animal_robot = None
        # self.animal_goal = None
        # self.non_animal_robot_1 = None
        # self.non_animal_robot_2 = None
        # object lists
        self.robot_list = []
        self.animal_list = []
        # move list of class
        self.valid_moves = None
        # networkx grid
        self.movement_network = None

    # def set_animal_robot(self, animal_robot_class):
    #     self.animal_robot = animal_robot_class
    #
    # def set_animal_goal(self, animal_goal_class):
    #     self.animal_goal = animal_goal_class
    #
    # def set_non_animal_robot_1(self, non_animal_robot_class_1):
    #     self.non_animal_robot_1 = non_animal_robot_class_1
    #
    # def set_non_animal_robot_2(self, non_animal_robot_class_2):
    #     self.non_animal_robot_1 = non_animal_robot_class_2

    def add_robot(self, robot):
        self.robot_list.append(robot)

    def add_animal(self, animal):
        self.animal_list.append(animal)

    def hexagonal_useable_area(self):
        """Maze are that can be used for hexagon style movement"""

        def get_range(num):
            if num % 2 == 1:
                # odd numbers
                x = num // 2
                return -x, x
            elif num % 2 == 0:
                # even numbers
                x = 4 // 2
                return 1 - x, x

        def generate_coordinates(row, col):
            cubic_coordinates = []
            row_start, row_end = get_range(row)
            column_start, column_end = get_range(col)
            for y in range(row_start, row_end + 1):
                for x in range(column_start, column_end + 1):
                    cubic_coordinates.append([x, y])
            return cubic_coordinates

        def cube_to_axial_conversion(cube_coordinate_list):
            hexagonal_coordinates = []
            for i in range(len(cube_coordinate_list)):
                x1 = cube_coordinate_list[i][0]
                y1 = cube_coordinate_list[i][1]
                x = int(y1)
                y = int(x1 - (y1 - (y1 & 1)) / 2)
                hexagonal_coordinates.append([x, y, -x - y])
            return hexagonal_coordinates

        cubic_coordinate_list = generate_coordinates(self.rows, self.columns)
        return cube_to_axial_conversion(cubic_coordinate_list)

    def generate_hexgrid_network(self):
        """Makes a grid of appropriate size with all the points in it"""
        self.movement_network = nx.triangular_lattice_graph(self.rows, self.columns, False, True)

    def get_consecutive_positions(self):
        """From the robot positions, select the consecutive positions from the network"""
        pass

    def remove_consecutive_positions(self):
        """Remove the positions that are consecutive to the robots and update self.movement_network"""
        pass

    def choose_new_non_animal_platform_positions(self):
        """Choose the new positions of the non-animal platforms in the maze; they will be consecutive to the
        animal robot's position (from the inner ring of the animal robot"""
        pass

    def get_pathfinding_target(self):
        """From the actual target, get the pathfinding target"""
        return [x,y]

    def get_pathfinding_start(self):
        """From the actual position of the animal robot pathfinding start"""
        return [x,y]

    def pathfinder(self):
        """get the list of movements from the pathfinding start to the pathfinding end (using dijkstra pathfining
        algorithm """
        start = self.get_pathfinding_start()
        target = self.get_pathfinding_target()
        return nx.shortest_path(self.movement_network, source=start, target=target)

def main():
    pass


if __name__ == '__main__':
    main()
