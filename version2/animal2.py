"""Animal Class"""

from random import choice


class Animal:
    def __init__(self, maze, *name):
        # Functions to set up the animal
        self.set_maze(maze)
        self.set_animal_position()
        # Identifying the animal
        self.name = name
        self.position_vector = None
        # maze the animal is in
        self.maze = None

    def set_animal_position(self):
        """Get the position of the robot class with the animal in it"""
        self.position_vector = self.maze.get_animal_robot_position_vector()

    def set_maze(self, maze):
        """Tell the animal and the maze that they both exist"""
        self.maze = maze
        self.maze.add_animal(self)

    def make_random_movement_choice(self):
        """Makes random choice of platform to move to"""
        movement_choices = self.maze.get_non_animal_class()
        return choice(movement_choices)

    def change_animal_class(self, choice_method=make_random_movement_choice):
        """Based on choice (random by default) , change the class of the animal robot and non animal robot"""
        new_animal_robot = choice_method

        for robot in self.maze.robot_list:
            robot.is_animal_robot = False

        new_animal_robot.is_animal_robot = True
        self.set_animal_position()
