'''This will define the boundary of the hexagon maze for the given layout of the maze'''
from hexagon_grid_functions import *
import random as rand

inner_ring_directions_list = [Hex(1, 0, -1), Hex(1, -1, 0), Hex(0, -1, 1), Hex(-1, 0, 1), Hex(-1, 1, 0), Hex(0, 1, -1)]
outer_ring_directions_list = [Hex(-2, 2, 0), Hex(2, -1, -1), Hex(2, -2, 0), Hex(1, 1, -2), Hex(0, 2, -2), Hex(-1, 2, -1), Hex(-2, 2, 0),Hex(-2, 1, 1), Hex(-2, 0, 2), Hex(-1, -1, 2), Hex(0, -2, 2), Hex(1, -2, 1)]



def inner_ring(robot):
    '''will get the ring of moves around a given coordiate, coordiate of radius 1'''
    output = []
    for i in range(len(inner_ring_directions_list)):
        output.append(hex_add(robot, inner_ring_directions_list[i]))
    return output

def outer_ring(robot):
    '''will get the ring of moves around a given coordiate, coordiate of radius 2'''
    output = []
    for i in range(len(outer_ring_directions_list)):
        output.append(hex_add(robot, outer_ring_directions_list[i]))
    return output

def select_target_location(animal_robot, platform_robot1, platform_robot2):
    '''Randomly select 2 different values from the inner ring, that the platform robots are not already located on'''
    # Check if the platform_robots are correctly inputted
    move_list = inner_ring(animal_robot)
    if platform_robot1 or platform_robot2 not in move_list:
        print('Error: The platform robots are not located in the inner ring')
    # Remove platform robots from the moves available
    move_list.remove(platform_robot1)
    move_list.remove(platform_robot2)
    # Select two moves from the remaining list
    return rand.sample(move_list, 2)

def straight_move(start, end):
    '''start coordinates and end coordinates '''
    # gets the list of coordinates between two points in 3D space
    pass

def hex_to_ssh():
    '''Will make moves into the correct output to the ssh'''
    pass

def hexagon_map(nCol, nRow):
    '''This will generate a list of all 'legal' move locations for the maze'''
    # find out the largest value of two values
    max_diameter = [nCol, nRow].max()
    # generate a hexagon list of the max_diameter
    # maze_list =
    
    # 'overlay' a rectangle of size nCol, nRow and remove these values from the maze_list
    # return maze_list
pass

def excluded_platforms():
    '''This will define the areas of the map where the robots can not go as due to the pathfinding of the robot'''
    pass

def test():
    a = Hex(0, +1, -1)
    inner_ring(a)
    print(select_target_location(a))

if __name__ == '__main__':
    test()