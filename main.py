'''Main Maze program that will move the robots around'''




# Check whether the intersection between the rings (list) are part of the target platform

# def intersection(platform_robot1, platform_robot2):
#     '''check the paths of the platform robots do not intersect'''
#     if path_between_points is in :
#         # robot paths do not intersect
#         return True
#     else:
#         # robot paths do intersect
#         return False

def reassign_robots():
    '''Changes the names of the robots to work with the program'''
    # animal_robot =
    # platform_robot1 =
    # platform_robot2 =
    pass

outer_ring_movement_vectors = [Hex(2,0,-2), Hex(2,-2,0), Hex(0,-2,2), Hex(-2,0,2), Hex(-2,2,0), Hex(0,2,-2)]







# def main():
#     '''Main loop of code'''
#     # STARTING POSITIONS
#     animal_robot = Hex(0,0,0)
#     platform_robot1 = Hex(-1,0,1)
#     platform_robot2 = Hex(0,-1,1)
#     while animal_robot != goal_platform:
#         # get the new locations (from the inner ring from the location of the animal's choice)
#         newplatform1, newplatform2 = select_target_location(animal_robot, platform_robot1, platform_robot2).split()
#         # send the robot from the inner ring to the outer ring
#         movement_direction_robot1 = hex_subtract(animal_robot, platform_robot1)
#         outer_ring_position_robot1 = hex_add(platform_robot1, movement_direction_robot1)
#
#         movement_direction_robot2 = hex_subtract(animal_robot, platform_robot2)
#         outer_ring_position_robot2 = hex_add(platform_robot2, movement_direction_robot2)
#         # get the path from location in the outer ring to the required location in the outer ring
#         # travel around middle rings to the desired location
#         # Check whether the intersection between the rings of both the paths that exist intersect
#         if intersection(platform_robot1, platform_robot2) == False:
#             # send the code to ssh
#         # get input from the DLC reassignment
#     pass7#

def object_main():
    pr = PlatformRobot(0 , 0 , 0, rotation='x', rel_position=0)
    print(
          pr.move_to_outer_ring())

if __name__ == '__main__':
    object_main()