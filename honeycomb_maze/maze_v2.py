"""Maze class"""
import logging
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
        self.set_network()

    def see_status(self):
        """Return the status of the maze (the position of the animal, robots, maze and goal for debugging"""
        print('\n \n========STATUS OF THE MAZE========')
        print(f'Maze goal is: {self.goal}')
        print('Position of Robots:')
        for robot in self.robot_list:
            print(f'{robot.name} is in position {robot.position_vector} and its the {robot.is_animal_robot}')

        print('Position of Animals:')
        for animal in self.animal_list:
            print(f'{animal.name} is in position {animal.position_vector}')

        print('=======END OF STATUS UPDATE======= \n \n ')

    def set_goal(self, goal):
        self.goal = goal

    def add_robot(self, robot):
        self.robot_list.append(robot)

    def add_animal(self, animal):
        self.animal_list.append(animal)

    def generate_network(self):
        """Makes the correctly labeled grid.
        :returns hexagonal grid on which the platforms move around

        parameters:
        First is X dimension, second is Y dimension, where the X is the 'spikey' top surface and Y is the smooth side
        """

        def node_generation(row, col):

            def pairwise(iterable):  # function
                "s -> (s0, s1), (s2, s3), (s4, s5), ..."
                a = iter(iterable)
                return zip(a, a)

            start = 0
            node_list = []
            # for every 2 rows in the network until you fun out of rows to iterate through:
            for x1, x2 in pairwise(list(range(row))):  # for every 2 elements in the list
                for y in list(range(start, col + start, 1)):  # for every y coordinate
                    node_list.append((x1, y, -(x1 + y)))
                    node_list.append((x2, y, -(x2 + y)))
                start = start - 1
                # y goes up however it starts back 1 every time it reaches the top

                # step back in the coordinate system 2
            return node_list

        def add_nodes(node_list, graph):
            for node in node_list:
                graph.add_node(node)
            # nx.draw_spring(graph, with_labels=True)
            return graph

        def consecutive_positions(node):
            # generate consecutive positions
            inner_ring_vectors = [(1, 0, -1), (1, -1, 0), (0, -1, 1), (-1, 0, 1), (-1, 1, 0),
                                  (0, 1, -1)]  # consecutive vectors
            inner_ring_nodes = []
            for inner_ring_vector in inner_ring_vectors:
                # add each vector to the node
                # print(node, inner_ring_vector)
                consecutive_node = [
                    a_i + b_i for a_i, b_i in zip(node, inner_ring_vector)]
                # print(consecutive_node)
                # add it to the list

                inner_ring_nodes.append(tuple(consecutive_node))

            return inner_ring_nodes

        def find_consecutive_nodes(node, graph):
            """if consecutive_nodes are in the node list, then add them to list of edges that need to be joined together"""
            edge_list = []  # list of edges that need to be joined

            inner_ring_nodes = consecutive_positions(node)  # list of positions consecutive to the nodes
            # print(inner_ring_nodes)
            # if consecutive nodes are in the list of nodes in the graph
            for inner_ring_node in inner_ring_nodes:
                if inner_ring_node in graph.nodes:
                    edge_list.append(inner_ring_node)  #
                # else:
                #     print(f'the node, {inner_ring_node} was not added as it is not in the {graph}')

            return edge_list

        def add_edges(edge_list, graph, node):
            """Add edges from edge list to the graph"""
            for edge in edge_list:
                graph.add_edge(node, edge)
            # nx.draw_spring(graph, with_labels=True)
            return graph

        I = nx.Graph()  # make graph

        def make_network(row, col, graph):
            """Join all the functions together"""

            # create coordinates
            node_list = node_generation(row, col, )

            # add nodes to list
            add_nodes(node_list, graph)

            for node in graph.nodes:
                # for each node
                edge_list = find_consecutive_nodes(node,
                                                   graph)  # find the set of nodes that are consecutive and in the graph
                add_edges(edge_list, graph, node)

            return graph

        return make_network(self.rows, self.columns, I)

    def set_network(self):
        self.movement_network = self.generate_network()

    def get_inner_ring_coordinates(self, position_vector):
        inner_ring = [[1, 0, -1], [1, -1, 0], [0, -1, 1], [-1, 0, 1], [-1, 1, 0], [0, 1, -1]]
        consecutive_coordinate_list = []
        print(f' position vector', position_vector)
        logging.info(f' position vector', position_vector)
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
        logging.info('The positions consecutive to any other robot have been removed from the temp_movement_network')
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
                logging.error('ERROR: there is no animal robot in the maze')


    def get_non_animal_robot_class(self):
        """:returns list of the non-animal class objects from self.robot_list"""
        for robot in self.robot_list:
            if robot.is_animal_robot == 'NAR':
                return robot

    def get_non_non_animal_robot_class(self):
        for robot in self.robot_list:
            if robot.is_animal_robot == 'NNAR':
                return robot

    def check_animal_at_goal(self):
        """Check if the animal position is at the position of the goal robot"""
        if self.get_animal_robot_class() == self.goal:
            return True
        elif self.get_animal_robot_class() != self.goal:
            return False

    def pathfinder(self, non_animal_robot):
        """
        Get the list of movements from the pathfinding start to the pathfinding end (using dijkstra pathfining
        algorithm

        Parameters
        ----------
        non_animal_robot = the robot that is just about to move
        """
        print(non_animal_robot.name)
        logging.debug(non_animal_robot.name)
        def flatten(t):
            return (item for sublist in t for item in sublist)

        start = non_animal_robot.position_vector
        target = non_animal_robot.pathfinding_target_position

        self.remove_consecutive_positions()
        network = list(self.temp_movement_network.nodes)

        # print('Nodes in network', network)
        logging.debug('\nPathfinding Source:', tuple(start), '\nPathfinding Target:', tuple(target))
        print('\nPathfinding Source:', tuple(start), '\nPathfinding Target:', tuple(target))

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
