'''
@Author: Rene Jacques
March 17, 2019
'''

import custom_user_input
import map_builder
import node, cv2, random, copy
import numpy as np
from A_star_npq import A_star
from Dijkstra_npq import Dijkstra

# define colors
white = (255,255,255)
black = (0,0,0)
gray = (50,50,50)
blue = (255,0,0)
green = (0,255,0)
red = (0,0,255)

class App:
	'''Main Class'''
	def __init__(self,start,goal,radius,clearance,resolution,user_input=False,rand_run=False,num_runs=1,algo=0):
		self.start = start
		self.goal = goal
		self.radius = radius
		self.clearance = clearance
		self.res = int(resolution)
		if self.res == 0:
			self.res = 1

		# get user input 
		if user_input:
			q = custom_user_input.Custom_User_Input()
			q.query('Enter Start Point in the form x,y: ','start',cSepNum=True)
			q.query('Enter Goal Point in the form x,y: ','goal',cSepNum=True)
			q.query('Enter Robot Radius: ','rad',isNumber=True)
			q.query('Enter Clearance: ','clear',isNumber=True)
			q.query('Enter Grid Resolution: ','res',isNumber=True)
			q.query('Enter Desired Algorithm (0 for A* or 1 for Dijkstra): ','algo',isNumber=True)
			q_in = q.get_input()

			self.start = q_in['start']
			self.start = (int(self.start[0]),int(self.start[1]))
			self.goal = q_in['goal']
			self.goal = (int(self.goal[0]),int(self.goal[1]))
			self.radius = int(q_in['rad'])
			self.clearance = int(q_in['clear'])
			self.res = int(q_in['res'])
			if self.res == 0:
				self.res = 1
			algo = int(q_in['algo'])
			# print(repr(algo),0,algo!=0,algo!=1)
			if algo != 0 and algo != 1:
				print('Input Algorithm is Invalid. Will Use Default a_star.')
				algo = 0

			print('\n')

		# check if start coordinates are within the map
		if self.start[0]*self.res >= 250 or self.start[0]*self.res < 0 or self.start[1]*self.res >= 150 or self.start[1]*self.res < 0:
			print('Invalid Start Coordinates: Coordinates are outside of the configuration space') 
			return

		# check if goal coordinates are within the map
		if self.goal[0]*self.res >= 250 or self.goal[0]*self.res < 0 or self.goal[1]*self.res >= 150 or self.goal[1]*self.res < 0:
			print('Invalid Start Coordinates: Coordinates are outside of the configuration space')
			return

		print('Starting Point: '+str(self.start[0])+','+str(self.start[1]))
		print('Goal Point: '+str(self.goal[0])+','+str(self.goal[1]))
		print('Robot Radius: '+str(self.radius))
		print('Clearance: '+str(self.clearance))
		print('Grid Resolution: '+str(self.res))

		print('=====')

		print('Running '+str(num_runs)+' times')

		print('-----')

		print('Building Map...')
		m = map_builder.Map_Builder()
		self.grid = m.create_map(self.res,clearance=self.clearance,radius=self.radius,draw=False)
		print('Finished Building Map.')

		# run algorithm as many times as num_runs
		count = 0
		while count < num_runs:
			print('=====')
			print('Run ',count+1)

			print('-----')

			# create the output image
			img,grid_lines,s = self.draw_output()

			# create random start and goal coordinates that are within the map and are not in obstacles
			if rand_run:
				print('Randomizing Start and Goal')
				self.start = (random.randint(0,(img.shape[1]-s*20)//s//self.res-1),random.randint(0,(img.shape[0]-s*20)//s//self.res-1))
				while self.grid[self.start[0],self.start[1]] == 1:
					self.start = (random.randint(0,(img.shape[1]-s*20)//s//self.res-1),random.randint(0,(img.shape[0]-s*20)//s//self.res-1))
				
				self.goal = (random.randint(0,(img.shape[1]-s*20)//s//self.res-1),random.randint(0,(img.shape[0]-s*20)//s//self.res-1))
				while self.grid[self.goal[0],self.goal[1]] == 1:
					self.goal = (random.randint(0,(img.shape[1]-s*20)//s//self.res-1),random.randint(0,(img.shape[0]-s*20)//s//self.res-1))

				print('Random Start: '+str(self.start))
				print('Random Goal: '+str(self.goal))
				print('-----')

			print('Begin '+'A*' if algo == 0 else 'Dijkstra'+' Search...')
		
			# run A* of Dijkstra based on user input
			if algo == 0:
				a_star = A_star(self.grid,grid_lines,img,self.res,s)
				a_star.search(self.start,self.goal)

			elif algo == 1:
				dijkstra = Dijkstra(self.grid,grid_lines,img,self.res,s)
				dijkstra.search(self.start,self.goal)

			count += 1
		
			print('Finished Path Search.')

		print('=====')
		print('Finished All Runs')

	def draw_output(self):
		s = 9 # scaling factor
		img = np.zeros((int(s*150),int(s*250)),np.uint8)
		img[np.where(img==0)] = 255

		img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

		# draw walls
		for key in self.grid:
			if self.grid[key] == 0:
				pass
			elif self.grid[key] == 1:
				x,y = int(s*key[0]*self.res),int(s*key[1]*self.res)
				a,b = int(s*(key[0]*self.res+self.res)),int(s*(key[1]*self.res+self.res))
				cv2.rectangle(img,(x,y),(a,b),black,-1)

		# pad image
		border = cv2.copyMakeBorder(img,s*10,s*10,s*10,s*10,cv2.BORDER_CONSTANT,value=(100,100,100))

		grid_lines = copy.copy(border)
		# draw grid
		for i in range(250//self.res+1):
			cv2.line(grid_lines,(int(s*i*self.res)+s*10,s*10),(int(s*(i*self.res))+s*10,grid_lines.shape[0]-s*10),gray,5 if i==0 else (2 if i%5==0 else 1))

		for j in range(150//self.res+1):
			cv2.line(grid_lines,(s*10,int(s*j*self.res)+s*10),(grid_lines.shape[1]-s*10,int(s*(j*self.res))+s*10),gray,5 if i==0 else (2 if j%5==0 else 1))

		return border,grid_lines,s

if __name__ == '__main__':
	'''Main function'''
	res = 1
	rad = 5
	clr = 0
	start = (10,140)
	goal = (240,10)
	a = App(start,goal,clr,rad,res,user_input=True,rand_run=False,num_runs=1,algo=0)