"""Animal Class"""
from random import choice


class Animal:
    def __init__(self, maze, *name):
        # Functions to set up the animal
        self.set_maze(maze)
        # self.set_animal_position()
        # Identifying the animal
        self.name = name
        self.position_vector = None
        # maze the animal is in
        self.maze = None
        # path that animal takes through maze
        self.animal_path = []  # this is a path of position vectors.

    def set_animal_position(self):
        """Get the position of the robot class with the animal in it"""
        print('animal position vector', self.maze.get_animal_robot_class().position_vector)
        self.position_vector = self.maze.get_animal_robot_class().position_vector

    def set_maze(self, maze):
        """Tell the animal and the maze that they both exist"""
        self.maze = maze
        self.maze.add_animal(self)

    def make_random_movement_choice(self):
        """Makes random choice of platform to move to
        ---
        :return class of the selected robot platform
        """
        robot_list = self.maze.robot_list.copy()  # create copy of robot list
        animal_robot_class = self.maze.get_animal_robot_class()

        robot_list.remove(animal_robot_class)  # remove the class of the robot on which the animal is on

        animal_choice = choice(robot_list)  # choose a platform for the robot to move to.

        self.animal_path.append(animal_choice.position_vector)  # append choice animal makes to list to keep track
        return animal_choice  # return position vector of the robot chosen

    def make_user_choice(self):
        """
        User can make choice of which platform the animal moves to.
        :return: User choice of platform for animal
        """
        robot_list = self.maze.robot_list.copy()  # create copy of robot list
        animal_robot_class = self.maze.get_animal_robot_class()

        robot_list.remove(animal_robot_class)  # remove the class of the robot on which the animal is on
        # list of robots' names
        robot_name_list = []
        for robot in robot_list:
            robot_name_list.append(robot.name)


        while True:
            try:
                user_input = int(input(f'Which robot would you like to choose from the following list? \n{robot_name_list}'))
                break

            except ValueError:
                print('Invalid Input. Try again.')

        return robot_list[user_input-1]


    def change_animal_class(self, new_animal_class):
        """Based on choice (random by default), change the class of the animal robot and non-animal robot"""

        # change class for robot list
        for robot in self.maze.robot_list:
            if robot.is_animal_robot == 'AR' and new_animal_class == robot:
                robot.is_animal_robot = 'AR'
            elif robot.is_animal_robot == 'AR' and new_animal_class != robot:
                robot.is_animal_robot = 'NAR'

            elif robot.is_animal_robot == 'NAR' and new_animal_class == robot:
                robot.is_animal_robot = 'AR'
            elif robot.is_animal_robot == 'NAR' and new_animal_class != robot:
                robot.is_animal_robot = 'NNAR'

            elif robot.is_animal_robot == 'NNAR' and new_animal_class == robot:
                robot.is_animal_robot = 'AR'
            elif robot.is_animal_robot == 'NNAR' and new_animal_class != robot:
                robot.is_animal_robot = 'NNAR'
