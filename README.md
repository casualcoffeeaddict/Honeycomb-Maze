# Honeycomb Maze Project
Alif Aziz
###Work flow for honeycomb maze:
1. Connect to robots
2. Set initial robot positions
3. Make Platform Map
   1. including making a list of positions that cant be final positions
4. Get initial positions of robots
5. pick new platform positions
6. contruct path from inital to final positions
7. check compatibility of all possible pairs of paths
8. calculate final paths using compatabilty (using compatibility matrix and path lengths)
9. make figure of current and future platforms
check if robots need to be staggered
10. determine timing of various paths
send ssh commands to actual robots
11. update the robots positions on the board
12. Check if the animal is at the goal
