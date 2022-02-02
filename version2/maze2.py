"""Maze class"""
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
        # List of the object names of the robots that are present in the maze
        self.robot_list = []
        self.animal_list = []
        # move list of class
        self.valid_moves = None
        # animal goal
        self.goal = None
        # networkx grid
        self.movement_network = None
        self.temp_movement_network = None
        # pathfinder commands
        self.path = None

    def set_goal(self, goal):
        self.goal = goal

    def add_robot(self, robot):
        self.robot_list.append(robot)

    def add_animal(self, animal):
        self.animal_list.append(animal)

    def generate_hexgrid_network(self):
        """Makes a grid of appropriate size with all the points in it"""
        self.movement_network = nx.triangular_lattice_graph(self.rows, self.columns, False, True)

        # define remapping function
        def remapping(element):
            x = element[0]
            y = element[1]
            return x, y, -(x + y)

        return nx.relabel_nodes(self.movement_network, remapping)

    def set_hexgrid_network(self):
        """Set the movement network hexagonal grid"""
        self.movement_network = self.generate_hexgrid_network()

    def get_consecutive_coordinates(self, position_vector):
        inner_ring = [[1, 0, -1], [1, -1, 0], [0, -1, 1], [-1, 0, 1], [-1, 1, 0], [0, 1, -1]]
        consecutive_coordinate_list = []
        x, y, z = position_vector
        for i in range(len(inner_ring)):
            change_x = inner_ring[i][0]
            change_y = inner_ring[i][1]
            change_z = inner_ring[i][2]

            consecutive_coordinate_list.append([x + change_x, y + change_y, z + change_z])

        return consecutive_coordinate_list

    def get_consecutive_positions(self):
        """From the robot positions, select the consecutive positions from the network"""
        robot_position_list = []
        for robot in self.robot_list:
            robot_position_list.append(robot.position_vector)

        consecutive_position_list = []
        for robot_position in robot_position_list:
            consecutive_position_list.append(self.get_consecutive_coordinates(robot_position))

        return consecutive_position_list

    def remove_consecutive_positions(self, position_list):
        """Remove the positions that are consecutive to the robots and update self.movement_network"""
        for i in range(len(position_list)):
            position = position_list[i]
            if position in list(self.temp_movement_network.nodes):
                self.temp_movement_network.remove_node(position)
            else:
                print('ERROR: A node that is not in the network is trying to be removed')
        print('The positions consecutive to any other robot have been removed from the temp_movement_network')
        return self.temp_movement_network

    def choose_new_non_animal_platform_positions(self):
        """Choose the new positions of the non-animal platforms in the maze; they will be consecutive to the
        animal robot's position (from the inner ring of the animal robot)"""
        pass

    def get_non_animal_class(self):
        """Returns list of the non-animal class objects from self.robot_list"""
        output = []
        for robot in self.robot_list:
            if robot.is_animal_robot == False:
                output.append(robot)
        return output

    def get_animal_robot_position_vector(self):
        for robot in self.robot_list:
            if robot.is_animal_robot == True:
                return robot.position_vector
            # else:
            #     print('ERROR: There is no animal robot in the maze')

    def get_pathfinding_start(self, non_animal_robot):
        """From the actual target, get the pathfinding target"""
        animal_robot_position_vector = self.get_animal_robot_position_vector()
        non_animal_robot_position_vector = non_animal_robot.position_vector
        # get relative position of non-animal robot position vector
        non_animal_robot_rel_position = non_animal_robot.relative_position(animal_robot_position_vector,
                                                                           non_animal_robot_position_vector)
        return non_animal_robot.move_to_outer_ring(non_animal_robot_position_vector, non_animal_robot_rel_position)

    def get_pathfinding_target(self, non_animal_robot):
        """From the actual position of the animal robot pathfinding start"""
        animal_robot_position_vector = self.get_animal_robot_position_vector()
        target_position_vector = non_animal_robot.target_position
        target_relative_position = non_animal_robot.relative_position(animal_robot_position_vector,
                                                                      target_position_vector)
        return non_animal_robot.move_to_outer_ring(target_position_vector, target_relative_position)

    def pathfinder(self, non_animal_robot):
        """Get the list of movements from the pathfinding start to the pathfinding end (using dijkstra pathfining
        algorithm """
        start = self.get_pathfinding_start(non_animal_robot)
        target = self.get_pathfinding_target(non_animal_robot)
        return nx.shortest_path(self.movement_network, source=start, target=target)


def main():
    pass


if __name__ == '__main__':
    main()
