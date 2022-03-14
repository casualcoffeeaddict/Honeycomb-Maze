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

    def set_animal_position(self):
        """Get the position of the robot class with the animal in it"""
        self.position_vector = self.maze.get_animal_robot_class().position_vector

    def set_maze(self, maze):
        """Tell the animal and the maze that they both exist"""
        self.maze = maze
        self.maze.add_animal(self)

    def make_random_movement_choice(self):
        """Makes random choice of platform to move to"""
        movement_choices = self.maze.get_non_animal_robot_class()
        return choice(movement_choices)

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

