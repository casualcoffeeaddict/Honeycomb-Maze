'''Maze class for the robot to move around in'''

class HexagonGrid():
    '''Base maze class which defines the area of the maze'''
    def __init__(self, column_number, row_number):
        self.columns = column_number
        self.rows = row_number

class HexagonMaze(HexagonGrid):
    '''Maze area for hexagonal platform'''
    def __init__(self, column_number, row_number):
        super().__init__(column_number, row_number)
        self.animal_robot = None
        self.animal_goal = None
        self.non_animal_robot_1 = None
        self.non_animal_robot_2 = None
        # move list of class
        self.valid_moves = self.set_move_list(self.hexagonal_useable_area())

    def set_animal_robot(self, animal_robot_class):
        self.animal_robot = animal_robot_class

    def set_animal_goal(self, animal_goal_class):
        self.animal_goal = animal_goal_class

    def set_non_animal_robot_1(self, non_animal_robot_class_1):
        self.non_animal_robot_1 = non_animal_robot_class_1

    def set_non_animal_robot_2(self, non_animal_robot_class_2):
        self.non_animal_robot_1 = non_animal_robot_class_2

    def set_move_list(self, map_type):
        self.move_list = map_type

    def hexagonal_useable_area(self):
        '''Maze are that can be used for hexagon style movement'''

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

        def cube_to_axial_conversion(list):
            hexagonal_coordinates = []
            for i in range(len(list)):
                x1 = list[i][0]
                y1 = list[i][1]
                x = int(y1)
                y = int(x1 - (y1 - (y1 & 1)) / 2)
                hexagonal_coordinates.append([x, y, -x - y])
            return hexagonal_coordinates

        cubic_coordinate_list = generate_coordinates(self.rows, self.columns)
        return cube_to_axial_conversion(cubic_coordinate_list)

    def circular_useable_area(self):
        '''Maze area that can be used for circular stype of movement'''
        circular_move_list = []
        return circular_move_list


def main():
    hm = HexagonMaze(3, 3)
    print(hm.hexagonal_useable_area())

if __name__ == '__main__':
    main()