from hexagon_grid_functions import *
from hexagon_map import inner_ring

def valid_turn(turning_robot, robot1, robot2):
    '''check if the turn is possible without collision'''
    if turning_robot in inner_ring(robot1) or turning_robot in inner_ring(robot2):
        return False
    else:
        return True


def rel_turn(turning_robot, rotation, robot1, robot2):
    '''robot is the robot being turned, number is 1 - 6'''
    # check if turn is valid
    if valid_turn(turning_robot, robot1, robot2):
        rotation = rotation % 6
        if rotation == 0:
            print('No rotation')
        elif 0 < rotation < 3:
            print('Turn right')
        elif rotation == 3:
            print('Turn behind')
        elif 3 < rotation < 6:
            print('Turn left')
        print(rotation)
    else:
        print('turn is not valid: robots consecutive to turning robot')

def ssh_turn():
    '''send turn command to robot program'''
    pass

def test():
    turning_robot = Hex(0, 0, 0)
    robot1 = Hex(2, -2, 0)
    robot2 = Hex(-2, 2, 0)
    print(rel_turn(turning_robot, -10, robot1, robot2))

if __name__ == '__main__':
    test()