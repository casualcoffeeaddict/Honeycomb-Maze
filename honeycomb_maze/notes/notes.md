# Pathfinding Method

## Send robots to outer ring
_Must be done for both of the robots_

1. Use hardcoded methods to send the robots to the outer ring (ie positions of pathfinding start)

## Main pathfinding
_This needs to be done for both of the robots in sequence_

1. Make the complete triangular network
2. Remove the positions of the invalid moves
   1. get the positions of the robots (that are not moving for that round of moving?)
   2. get the positions around those robots that are unable to be accessed by the robots 
   3. remove those positions from the network (making them unavailable)
3. Get a list of the pathfinding through the maze
   1. from the actual position of the robot positions, get the start position for the network (corresponding outer ring positions)
   2. from the actual target, get the pathfinding target (will be corresponding outer ring position)
   3. perform the pathfinding
4. send the list of coordinates to the robot that will move
5. robot gets the list of commands to use


## Send robots to inner ring
_Once both the robots are in position_

1. Use the hardcoded methods to send the robots to the inner ring (ie from the pathfinding target to the inner ring)