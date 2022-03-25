"""Animal Class"""
from random import choice
from logging import *

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
        self.animal_path = []   # this is a path of position vectors.

    def set_animal_position(self):
        """Get the position of the robot class with the animal in it"""
        self.position_vector = self.maze.get_animal_robot_class().position_vector

    def set_maze(self, maze):
        """Tell the animal and the maze that they both exist"""
        self.maze = maze
        self.maze.add_animal(self)

    def make_random_movement_choice(self):
        """Makes random choice of platform to move to
        ---
        :return Position vector of the selected robot platform
        """
        robot_list = self.maze.robot_list
        animal_robot_class = self.maze.get_animal_robot_class()

        robot_list.remove(animal_robot_class) # remove the class of the robot on which the animal is on

        animal_choice = choice(robot_list).position_vector

        self.animal_path.append(animal_choice) # append choice animal makes to list to keep track
        return choice # return position vector of the robot chosen

    def change_animal_class(self, new_animal_class):
        """Based on choice (random by default) , change the class of the animal robot and non animal robot"""
        new_animal_class.is_animal_robot

        for robot in self.maze.robot_list:
            if robot.is_animal_robot == 'AR' and new_animal_class == self:
                robot.is_animal_robot = 'AR'
            if robot.is_animal_robot == 'AR' and new_animal_class != self:
                robot.is_animal_robot = 'NAR'

            if robot.is_animal_robot == 'NAR' and new_animal_class == self:
                robot.is_animal_robot = 'AR'
            if robot.is_animal_robot == 'NAR' and new_animal_class != self:
                robot.is_animal_robot = 'NNAR'

            if robot.is_animal_robot == 'NNAR' and new_animal_class == self:
                robot.is_animal_robot = 'AR'
            if robot.is_animal_robot == 'NNAR' and new_animal_class != self:
                robot.is_animal_robot = 'NNAR'

