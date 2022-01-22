'''Animal class which take inputs from DLC and makes decisions about which platform it moves to'''

from robot import *

class Animal():
    def __init__(self, platform):
        self.position_vector = None
        # references to other robots
        self.platform_1 = None
        self.platform_2 = None
        self.platform_3 = None

    def set_platform_1(self, platform_1_class):
        self.platform_1 = platform_1_class.position_vector

    def set_platform_2(self, platform_2_class):
        self.platform_2 = platform_2_class.position_vector

    def set_platform_3(self, platform_3_class):
        self.platform_3 = platform_3_class.position_vector

    def select_animal_move(self, platform):
        self.position = platform.position_vector

    def get_animal_platform(self):
        '''Get the platform which is has the animal on it'''
        pass

    def choose_random_platform(self):
        '''FOR TESTING: choose platform the animal moves to'''
        pass
