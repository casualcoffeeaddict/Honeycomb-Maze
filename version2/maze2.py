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
        self.consecutive_positions = []
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

        # Creates hexgrid network
        self.set_hexgrid_network()

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

    def get_inner_ring_coordinates(self, position_vector):
        inner_ring = [[1, 0, -1], [1, -1, 0], [0, -1, 1], [-1, 0, 1], [-1, 1, 0], [0, 1, -1]]
        consecutive_coordinate_list = []
        print('position vector', position_vector)
        x, y, z = list(position_vector)
        for i in range(len(inner_ring)):
            change_x = inner_ring[i][0]
            change_y = inner_ring[i][1]
            change_z = inner_ring[i][2]

            consecutive_coordinate_list.append([x + change_x, y + change_y, z + change_z])

        return consecutive_coordinate_list

    def get_outer_ring_coordinates(self, position_vector):
        inner_ring = [[2, 0, -2], [2, -1, -1], [2, -2, 0], [1, -2, 1], [0, -2, 2], [-1, -1, 2], [-2, 0, 2], [-2, 1, 1],
                      [-2, 2, 0], [-1, 2, -1], [0, 2, -2]]
        outer_ring_coordinates = []
        x, y, z = position_vector
        for i in range(len(inner_ring)):
            change_x = inner_ring[i][0]
            change_y = inner_ring[i][1]
            change_z = inner_ring[i][2]

            outer_ring_coordinates.append([x + change_x, y + change_y, z + change_z])

        return outer_ring_coordinates

    def get_consecutive_positions(self, moving_robot_class):
        """From the robot positions, select the positions and consecutive positions of the non-moving robots
        from the network
        and
        returns a list of tuples that are consecutive to the robots in the network"""
        # Non-moving robots position list
        robot_position_list = []
        for robot in self.robot_list:
            if robot != moving_robot_class:
                robot_position_list.append(robot.position_vector)
            else:
                pass

        # Non-moving robot position list
        consecutive_position_list = []
        for robot_position in robot_position_list:
            consecutive_coordinate_list = self.get_inner_ring_coordinates(robot_position)
            for c in consecutive_coordinate_list:
                consecutive_position_list.append(c)
        consecutive_position_list.sort()

        # Formatting

        def remove_duplicates(coordinate_list):
            new_coordinate_list = []
            for elem in coordinate_list:
                if elem not in new_coordinate_list:
                    new_coordinate_list.append(elem)
            return new_coordinate_list

        def list_to_tuples(coordinate_list):
            new_coordinate_list = []
            for c in coordinate_list:
                new_coordinate_list.append(tuple(c))
            return new_coordinate_list

        return list_to_tuples(remove_duplicates(consecutive_position_list))

    def set_consecutive_positions(self, moving_robot_class):
        self.consecutive_positions = self.get_consecutive_positions(moving_robot_class)

    def remove_consecutive_positions(self):
        """Remove the positions that are consecutive to the robots and update self.temp_movement_network"""
        self.temp_movement_network = self.movement_network
        for i in range(len(self.consecutive_positions)):
            position = self.consecutive_positions[i]
            if position in list(self.temp_movement_network.nodes):
                self.temp_movement_network.remove_node(position)
            else:
                print('ERROR: A node that is not in the network is trying to be removed')
        print('The positions consecutive to any other robot have been removed from the temp_movement_network')
        return self.temp_movement_network

    def make_temp_movement_network(self, moving_robot_class):
        """Generate the network that the robots will have to traverse"""
        self.set_consecutive_positions(moving_robot_class)
        self.remove_consecutive_positions()
        return self.temp_movement_network

    def get_animal_robot_class(self):
        """:returns the class of the animal robot (where there is only one animal robot)"""
        for robot in self.robot_list:
            if robot.is_animal_robot == 'AR':
                return robot
            else:
                print('ERROR: there is no animal robot in the maze')

    def get_non_animal_robot_class(self):
        """:returns list of the non-animal class objects from self.robot_list"""
        for robot in self.robot_list:
            if robot.is_animal_robot == 'NAR':
                return robot

    def get_non_non_animal_robot_class(self):
        for robot in self.robot_list:
            if robot.is_animal_robot == 'NNAR':
                return robot

    def get_animal_robot_position_vector(self):
        for robot in self.robot_list:
            if robot.is_animal_robot == True:
                return robot.position_vector
            # else:
            #     print('ERROR: There is no animal robot in the maze')

    def pathfinder(self, non_animal_robot):
        """Get the list of movements from the pathfinding start to the pathfinding end (using dijkstra pathfining
        algorithm """
        print(non_animal_robot.name)
        def get_pathfinding_start(non_animal_robot):
            """From the position of the animal robot, find the starting position for pathfinding"""
            return non_animal_robot.position_vector

        def get_pathfinding_target(non_animal_robot):
            """From the actual target, find the position of the pathfinding target"""
            print('Target Position:', non_animal_robot.target_position)

            target_rel_position = non_animal_robot.animal_relative_position(non_animal_robot.target_position)
            print('Target relative position:', target_rel_position)

            inner_ring = [[-1, 0, +1], [-1, 1, 0], [0, 1, -1], [1, 0, -1], [1, -1, 0], [0, -1, 1]]
            movement = inner_ring[target_rel_position]

            # Element wise addition of the movement and the target position
            target = [non_animal_robot.target_position + movement for non_animal_robot.target_position, movement
                      in zip(non_animal_robot.target_position, movement)]

            return target

        def flatten(t):
            return (item for sublist in t for item in sublist)

        start = get_pathfinding_start(non_animal_robot)
        target = get_pathfinding_target(non_animal_robot)


        self.remove_consecutive_positions()
        network = list(self.temp_movement_network.nodes)

        # print('Nodes in network', network)

        print('\nsource:', tuple(start), '\ntarget:', tuple(target))

        return nx.shortest_path(self.temp_movement_network, source=tuple(start), target=tuple(target))

    def pathfinder_loop_1(self, moving_robot_class):
        # step 1 - will be different for NAR and NNAR
        first_move = []
        if moving_robot_class.is_animal_robot == 'NNAR':
            first_move.append(moving_robot_class.step_back_from_NAR())
        if moving_robot_class.is_animal_robot == 'NAR':
            first_move.append(moving_robot_class.move_to_animal_outer_ring())

        # generate pathfinding network for a given robot to path find around
        self.make_temp_movement_network(moving_robot_class)
        # path find around this network to final outer ring positions
        path = self.pathfinder(moving_robot_class)

        return moving_robot_class.make_command_list(path)

    def pathfinder_loop_2(self, moving_robot_class):
        """Move both non-animal robots (NAR & NNAR) to the inner ring at the same time"""
        direction = moving_robot_class.animal_relative_position(moving_robot_class.position_vector)
        moving_robot_class.move_to_outer_ring(direction)


def main():
    pass


if __name__ == '__main__':
    main()
