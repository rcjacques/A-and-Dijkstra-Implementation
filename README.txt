Author: Rene Jacques
Class: ENPM661 Planning for Autonomous Robotics
Projecg 2
April 2, 2019

Necessary Libraries:
	cv2, random, copy, numpy

Main File:
	project_2_final.py

Secondary Files:
	node.py, A_star_npq.py, Dijkstra_npq.py, map_builder.py, custom_user_input.py

Run Instructions:

Run project_2_final.py in command line in order to be able to input start state, goal state, grid resolution, robot radius, wall clearance, and which algorithm to use. 
	If you do not want to run with user input then change the user_input flag to be False in App() at the bottom of project_2_final.py

Run Instructions For Specific Cases:

	-To perform a Dijkstra Point robot search:
		-Run project_2_final.py in command line
		-Set desired start state
		-Set desired goal state
		-Set desired grid resolution
		-Set robot radius to 0
		-Set wall clearance to 0
		-Set algorithm to 'dijkstra'

	-To perform a Dijkstra Rigid robot search:
		-Run project_2_final.py in command line
		-Set desired start state
		-Set desired goal state
		-Set desired grid resolution
		-Set desired robot radius
		-Set desired wall clearance
		-Set algorithm to 'dijkstra'

	-To perform an A* Point robot search:
		-Run project_2_final.py in command line
		-Set desired start state
		-Set desired goal state
		-Set desired grid resolution
		-Set robot radius to 0
		-Set wall clearance to 0
		-Set algorithm to 'a_star'

	-To perform an A* Rigid robot search:
		-Run project_2_final.py in command line
		-Set desired start state
		-Set desired goal state
		-Set desired grid resolution
		-Set desired robot radius
		-Set desired wall clearance
		-Set algorithm to 'a_star'

Main File Description:
	project_2_final.py
		-This is the main file for this project
		-This file:
			-recieves user input
			-converts input into usable variables
			-uses the input to generate a map of the obstacle space
			-runs the user specified algorithm to find a path between the start and goal in that obstacle space
		-Inputs:
			-Start Point: 
				-in the form '0,0' where the first number is the x coordinate of the starting point in the obstacle grid space and the second number is the y coordinate of the starting point in the obstacle grid space
			-Goal Point: 
				-in the form '0,0' where the first number is the x coordinate of the goal point in the obstacle grid space and the second number is the y coordinate of the goal point in the obstacle grid space
			-Robot Radius:
				-in the form '0' with the input unit being in millimeters representing the radius of a rigid robot (set this number and Wall Clearance to 0 for a point robot)
			-Wall Clearance:
				-in the form '0' with the input unit being in millimeters representing the minimum distance that the robot is allowed to approach the wall (set this number and Robot Radius to 0 for a point robot)
			-Grid Resolution:
				-in the form '0' with the input unit being in millimeters representing the width and height of each square in the grid space
			-Desired Algorithm:
				-the default algorithm to be used is A*. If the user input is not recognized then A* will be used. However if 'dijkstra' is input then the program will use the Dijkstra algorithm instead
		-Notes:
			-this program has the capability to run for as many times as the user desires, and to use random starting locations and ending locations if the user desires. These parameters can be changed within App() at the bottom of project_2_final.py, but cannot be changed through command line user input as they are not expected to be used generally.

Secondary File Descriptions:
	map_builder.py
		-This file builds the map with obstacles using semi-algebraic models and half-planes. It also enlarges the obstacles using the Minkowski sum if the at least one of robot radius and clearance are greater than 0. It normally takes around 10 seconds to build the map. While the map is being built the obstacle space is also built using the same semi-algebraic models and half-planes. For each pixel that is an obstacle the upper left grid coordinate is determined (the size of the grid is based on the input resolution) and that grid square's value is set to 1, indicating that it is an obstacle. If the grid value is 0, then the space is open. This file can be run on its own and it will display 4 images: the normal map (unenlarged), the grid space derived from the normal map, the enlarged map, the grid space derived from the enlarged map. 

	node.py
		-This file contains several classes. The Node class is the same class that was used for project 1. The node class that is used for this project is called H_Node. H_Node is an extension of Node. H_Node is able to store (x,y) coordinate pairs and g, h, and f costs for heuristic storage.

	custom_user_input.py
		-This file contains the Custom_User_Input class. This class is used to simplify current and future user input requirements by automatically checking if inputs are strings or numbers and then returning the proper data type jf it exists. If user input is incorrect then this class returns False.

	A_star_npq.py
		-This file contains the A_star class. This class calculates and visualizes both the nodes that have been visited and the path required to reach the goal using the A* algorithm. This class takes as input the grid squares, grid lines, image, resolution, and scaling factor. When performing a search the search method takes as input the starting coordinates in the grid space and the goal coordinates in the grid space. 

	Dijkstra_npq.py
		-This file contains the Dijkstra class. This class calculates and visualizes both the nodes that have been visited and the path required to reach the goal using Dijkstra's algorithm. This class takes as input the grid squares, grid lines, image, resolution, and scaling factor. When performing a search the search method takes as input the starting coordinates in the grid space and the goal coordinates in the grid space.