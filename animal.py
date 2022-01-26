'''Animal class which take inputs from DLC and makes decisions about which platform it moves to'''
import random as rand
import time

class Animal():
    def __init__(self, platform_class, name):
        self.name = name
        self.position_vector = platform_class.position_vector
        # references to other robots
        self.animal_robot = platform_class
        self.non_animal_robot_1 = None
        self.non_animal_robot_2 = None
        # animal goal
        self.animal_goal = None
        # the choice of platforms the animal can choose to go to
        self.animal_choice_1 = None
        self.animal_choice_2 = None
        # get inner ring data
        self.inner_ring_dim = ['x', 'y', 'z', 'x', 'y', 'z']
        self.inner_ring_steps = [-1, -1, -1, 1, 1, 1]

    def change_position(self, dimension, step):
        '''Move position vector around the board'''
        x, y, z = self.position_vector
        if dimension == 'x':
            y += step
            z -= step
        elif dimension == 'y':
            x += step
            z -= step
        elif dimension == 'z':
            x += step
            y -= step
        else:
            print(f'ERROR: Select correct dimension for {self} either x, y, z')
        self.position_vector = [x, y, z]
        return self.position_vector

    def see_mouse_status(self):
        print(
            'Animal Robot', self.animal_robot,
            '\n Non-Animal Robot 2', self.non_animal_robot_1,
            '\n Non-Animal RObot 2', self.non_animal_robot_2,
            '\n Animal Goal', self.animal_goal,
            '\n Animal Choice 1',  self.animal_choice_1,
            '\n Animal Choice 2', self.animal_choice_2,
        )

    def set_animal_goal(self, animal_goal_class):
        self.animal_goal = animal_goal_class

    def set_animal_robot(self, animal_robot):
        self.animal_robot = animal_robot

    def set_non_animal_robot_1(self, non_animal_robot_1):
        self.non_animal_robot_1 = non_animal_robot_1

    def set_non_animal_robot_2(self, non_animal_robot_2):
        self.non_animal_robot_2 = non_animal_robot_2

    def reassign_animal_robot_class(self, animal_robot, non_animal_robot_class_1, non_animal_robot_class_2):
        self.animal_robot = animal_robot
        self.non_animal_robot_1 = non_animal_robot_class_1
        self.non_animal_robot_2 = non_animal_robot_class_2

    def select_animal_move(self, platform):
        self.position = platform.position_vector

    def get_animal_platform(self):
        '''Get the platform which is has the animal on it'''
        pass

    def check_if_animal_at_goal(self):
        '''Checks if the animal platform is at the goal platform'''
        if self.animal_goal.position_vector == self.position_vector:
            return True
        elif self.animal_goal.position_vector != self.position_vector:
            return False

    def get_inner_ring(self):
        '''get the positions of the consecutive 6 spaces around the mouse platform'''
        inner_ring_list = []
        self.change_position('y', 1)
        for i in range(len(self.inner_ring_dim)):
            inner_ring_list.append(self.change_position(self.inner_ring_dim[i], self.inner_ring_steps[i]))
        return inner_ring_list

    def get_new_animal_positions(self):
        '''FOR TESTING: Gets two random positions from the inner ring of the AnimalRobot that the NonAnimalRobots
        are not occupying'''
        inner_ring_list = self.get_inner_ring()
        inner_ring_positions = []
        for i in range(len(inner_ring_list)):
            inner_ring_positions.append(inner_ring_list[i])


        # # remove the positions of obstacles on the maze from selection
        # if self.non_animal_robot_1.position_vector is not inner_ring_positions:
        #     inner_ring_positions.remove(self.non_animal_robot_1.position_vector)
        # if self.non_animal_robot_2.position_vector is not inner_ring_positions:
        #     inner_ring_positions.remove(self.non_animal_robot_2.position_vector)
        # if self.animal_goal.position_vector is not inner_ring_positions:
        #     inner_ring_positions.remove(self.animal_goal.position_vector)

        # select choice from remaining list
        return rand.choices(inner_ring_positions, k=2)

    def set_new_animal_choices(self):
        '''Get choices for the animal to decide to move to'''
        choice_1, choice_2 = self.get_new_animal_positions()
        if choice_1 == choice_2:
            self.get_new_animal_positions()
            self.set_new_animal_choices()
        else:
            self.animal_choice_1 = choice_1
            self.animal_choice_2 = choice_2
        return self.animal_choice_1, self.animal_choice_2

    def makes_random_choice(self):
        '''FOR TESTING: Animal makes choice; randomly'''
        self.set_new_animal_choices()
        choice_list = [self.animal_choice_1, self.animal_choice_2]
        return rand.choice(choice_list)

    def change_animal_platform(self, choice_method):
        '''Based on what choice the animal makes, the the robot which is the animal robot changes'''
        animal_robot_position = choice_method
        print('animal robot position:', animal_robot_position)
        temp_animal_robot_class = self.animal_robot
        temp_non_animal_robot_class_1 = self.non_animal_robot_1
        temp_non_animal_robot_class_2 = self.non_animal_robot_2
        print('start:',
              temp_animal_robot_class.name,
              temp_non_animal_robot_class_1.name,
              temp_non_animal_robot_class_2.name)
        print('temp position vectors:',
              temp_non_animal_robot_class_1.position_vector,
              temp_non_animal_robot_class_2.position_vector)
        if temp_non_animal_robot_class_1.position_vector == animal_robot_position:
            self.animal_robot = temp_non_animal_robot_class_1
            self.non_animal_robot_1 = temp_animal_robot_class
            # self.non_animal_robot_2 remains unchanged as the mouse did not move there
        elif temp_non_animal_robot_class_2.position_vector == animal_robot_position:
            self.animal_robot = temp_non_animal_robot_class_2
            self.non_animal_robot_2 = temp_animal_robot_class
            # self.non_animal_robot_1 remains unchanged as the mouse did not move there
        else: print('ERROR: No change in animal class was made')
        return self.animal_robot.name, self.non_animal_robot_1.name, self.non_animal_robot_2.name

    def animal_makes_choice_DLC(self):
        '''Function for where the animal chooses via integration with deeplabcut'''
        pass
