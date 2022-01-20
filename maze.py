'''Maze class for the robot to move around in'''

class HexagonGrid():
    '''Base maze class which defines the area of the maze'''
    def __init__(self, column_number, row_number):
        self.columns = column_number
        self.rows = row_number

class HexagonMaze(HexagonGrid):
    '''Maze area for hexagonal platform'''
    def __init__(self, column_number, row_number):
        super().__init__(self, column_number, row_number)
        self.animal_robot = None
        self.animal_goal = None
        self.non_animal_robot_1 = None
        self.non_animal_robot_2 = None

    def set_animal_robot(self, animal_robot_class):
        self.animal_robot = animal_robot_class

    def set_animal_goal(self, animal_goal_class):
        self.animal_goal = animal_goal_class

    def set_non_animal_robot_1(self, non_animal_robot_class_1):
        self.non_animal_robot_1 = non_animal_robot_class_1

    def set_non_animal_robot_2(self, non_animal_robot_class_2):
        self.non_animal_robot_1 = non_animal_robot_class_2

    def useable_area(self):
        '''Maze are that can be used for hexagon style movement'''
        pass

def main():
    hm = HexagonMaze(10, 10)

if __name__ == '__main__':
    main()