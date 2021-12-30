from hexagon_grid_functions import *
from hexagon_map import inner_ring

def valid_turn(turning_robot, robot1, robot2):
    '''check if the turn is possible without collision'''
    if turning_robot in inner_ring(robot1) or turning_robot in inner_ring(robot2):
        return False
    else:
        return True


def rel_turn(robot, clock, number):
    '''robot is the robotbeing turned, clock is either clockwise or anticlockwise, number is 1 - 6'''
    # check if turn is valid
    if valid_turn(turning_robot, robot1, robot2):
        # Perform turn
    else:
        print('turn is not valid: robots consecutive to turning robot')


def test():
    turning_robot = Hex(0, 0, 0)
    robot1 = Hex(2, -2, 0)
    robot2 = Hex(-2, 2, 0)
    print(valid_turn(turning_robot, robot1, robot2))

if __name__ == '__main__':
    test()