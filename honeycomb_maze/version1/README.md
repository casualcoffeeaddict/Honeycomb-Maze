# Honeycomb Maze Project
Alif Aziz
### Work flow for honeycomb maze:
1. Connect to robots
2. Set initial robot positions
   1. UI interface
3. Make Platform Map
   1. including making a list of positions that cant be final positions, ie remove the spaces the robot cannot go to

#### Main loop
4. Get initial positions of robots
   1. UI interface required for this?
5. pick new platform positions
   1. positions will be pick from the list of possible moves from the inner ring
      1. 
6. construct path from initial to final positions
   1. Method:
      1. NNAR go from inner ring to outer ring (i.e. step back from NAR)
      2. pathfind
         1. get pathfinding start (the current position of the NNAR)
         2. get pathfinding target (the outer ring position of the actual target position)
         3. fun pathfinding command
      3. go back to inner ring (step in to AR)
7. check compatibility of all possible pairs of paths
   1. Think about how the paths will be encoded in the program
      1. how will the path to ssh work?
      2. the paths will only intersect if the tiles intersect at the same 'time', (if the paths are encoded by a list the list entries can be the same but can not be the same _at the same time_)
8. calculate final paths using compatabilty (using compatibility matrix and path lengths)
9. make figure of current and future platforms
check if robots need to be staggered
   1. do the robots have to move in at the same time?
10. determine timing of various paths
send ssh commands to actual robots
11. update the robots positions on the board
#### Integrate DLC into the program
12. Check were the animal is (via DLC) - where is the animal and the robots location?
13. Check if the animal is at the goal, if so end the loop
