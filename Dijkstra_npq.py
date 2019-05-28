'''
@Author: Rene Jacques
March 21, 2019
'''

from node import H_Node
from priority_queue import NaivePriorityQueue
import math, cv2

# define grid space values
WALL = 1
SPACE = 0
OPEN = 2
CLOSED = 3

# define colors
yellow = (0,255,255)
cyan = (255,255,0)
white = (255,255,255)
black = (0,0,0)
gray = (50,50,50)
blue = (255,0,0)
green = (0,255,0)
red = (0,0,255)

def distance(one,two):
	'''Calculate straight line distance between two points'''
	x1,y1 = one.getCoords()
	x2,y2 = two.getCoords()
	return math.sqrt((x1-x2)**2+(y1-y2)**2)

class Dijkstra:
	'''Dijkstra Search Algorithm'''
	def __init__(self,grid,lines,img,res,scale):
		self.grid = grid
		self.lines = lines
		self.img = img
		self.res = res
		self.scale = scale

		self.open_set = NaivePriorityQueue() 
		self.closed_set = set()

	def img_test(self):
		'''Test if image is correct'''
		cv2.rectangle(self.img,(self.res*10,self.res*10),(self.res*10+50,self.res*10+50),yellow,-1)
		cv2.imshow('A*',cv2.resize(self.img,(0,0),fx=0.5,fy=0.5))

		cv2.waitKey(0)

	def search(self,start,goal):
		'''Search for goal coordinates given start coordinates'''
		x,y = start
		# color in start square
		cv2.rectangle(self.img,((self.scale*10)+self.scale*self.res*x,(self.scale*10)+self.scale*self.res*y),((self.scale*10)+self.scale*(self.res*x+self.res),(self.scale*10)+self.scale*(self.res*y+self.res)),blue,-1)

		x,y = goal
		# color in goal square
		cv2.rectangle(self.img,((self.scale*10)+self.scale*self.res*x,(self.scale*10)+self.scale*self.res*y),((self.scale*10)+self.scale*(self.res*x+self.res),(self.scale*10)+self.scale*(self.res*y+self.res)),red,-1)

		# create start node
		s = H_Node()
		s.setCoords(start[0],start[1])

		# create goal node
		g = H_Node()
		g.setCoords(goal[0],goal[1])

		# add start node to open_set
		self.open_set.add(s)

		# initialize variable to check if the size of the open_set stays 1 for 5 loops
		open_count = 0

		# search until the open_set is empty or a break is encountered
		while not self.open_set.isEmpty() and open_count != 5:
			if(len(self.open_set.getQueue()) == 1):
				open_count += 1
			else:
				open_count = 0

			# get the next node out of the open set
			next_node = self.open_set.pop()

			# get the next nodes neighbors
			neighbors = self.get_neighbors(next_node)

			for neighbor in neighbors:
				# check if the neighbor is at the goal
				if neighbor.getCoords()[0]==goal[0] and neighbor.getCoords()[1]==goal[1]:
					print('Goal Found At:'+str(neighbor.getCoords()))

					# show the path from goal to start
					self.build_path(neighbor)

					# draw the gridlines on the final output image
					grid_img = cv2.bitwise_and(self.img,self.lines)
					cv2.imshow('Dijkstra',cv2.resize(grid_img,(0,0),fx=0.5,fy=0.5))

					cv2.waitKey(0)
					return
				else:
					# calculate the g and h costs for the neighbor
					g_cost = next_node.getCost()[0]+distance(next_node,neighbor) # neighbor g cost = parent node's g cost + distance between neighbor and parent
					h_cost = 0 # neighbor h cost = 0
					neighbor.setCost(g_cost,h_cost)

					# initialize a flag to indicate duplicates in the open and closed sets
					duplicate_flag = False

					# check if the neighbor is in the open set or the closed set
					for item in self.open_set.getQueue():
						# check if the neighbor is in the closed set
						if str(neighbor.getCoords()) in self.closed_set:
							duplicate_flag = True
							break

						if not duplicate_flag:
							# check if the neighbor is in the open set
							if item.getCoords() == neighbor.getCoords():
								# if the neighbor's g cost is less than a node's g cost 
								if neighbor.getCost()[0] < item.getCost()[0]:
									self.open_set.remove(item) # remove the node from the open set
									self.open_set.add(neighbor) # add the neighbor to the open set
								duplicate_flag = True
								break

					# if the neighbor is not in the open set and not in the closed set
					if not duplicate_flag:
						# add neighbor to the open set
						self.open_set.add(neighbor)
						x,y = neighbor.getCoords()

						# if the neighbor is not the start node and not the goal node 
						if (x != start[0] or y != start[1]) and (x != goal[0] or y != goal[1]):
							# color in the neighbor's grid square as yellow
							cv2.rectangle(self.img,((self.scale*10)+self.scale*self.res*x,(self.scale*10)+self.scale*self.res*y),((self.scale*10)+self.scale*(self.res*x+self.res),(self.scale*10)+self.scale*(self.res*y+self.res)),yellow,-1)

			# add the current node to the closed set
			closed = str(next_node.getCoords())
			self.closed_set.add(closed)
			x,y = next_node.getCoords()

			# if the current node is not the start node and not the goal node
			if (x != start[0] or y != start[1]) and (x != goal[0] or y != goal[1]):
				# color in the current node's grid square as cyan
				cv2.rectangle(self.img,((self.scale*10)+self.scale*self.res*x,(self.scale*10)+self.scale*self.res*y),((self.scale*10)+self.scale*(self.res*x+self.res),(self.scale*10)+self.scale*(self.res*y+self.res)),cyan,-1)

			# draw the grid lines and display the animation
			grid_img = cv2.bitwise_and(self.img,self.lines)
			cv2.imshow('Dijkstra',cv2.resize(grid_img,(0,0),fx=0.5,fy=0.5))

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		# if the open set is empty then there is no path possible
		if self.open_set.isEmpty() or open_count ==5:
			print('No Path Possible')
		cv2.waitKey(0)

	def get_neighbors(self,n):
		'''Get all of the neighbors for the input node'''
		neighbors = []
		directions = [-1,0,1]

		x,y = n.getCoords()

		# get each neigbor to the top left, top middle, top right, right middle, bottom right, bottom middle, bottom left, left middle
		for i in directions:
			for j in directions:

				# if the coordinates are not changed then ignore them
				if i == 0 and j == 0:
					pass

				# make sure that the coordinates are not outside of the map
				elif x+i < 0 or y+j < 0 or x+i > (self.img.shape[1]-self.scale*20)//self.scale//self.res-1 or y+j > (self.img.shape[0]-self.scale*20)//self.scale//self.res-1:
					pass

				# if the coordinates are not in a wall then create a new node and add to the neighbor list 
				elif self.grid[x+i,y+j] != WALL:
					neighbor = H_Node()
					neighbor.setCoords(x+i,y+j)
					neighbor.setPathParent(n)
					neighbors.append(neighbor)

		return neighbors

	def build_path(self,n):
		'''Recursive function to build the path by searching through the parents of each node from start to goal'''
		x,y = n.getCoords()

		# color in the path squares
		cv2.rectangle(self.img,((self.scale*10)+self.scale*self.res*x,(self.scale*10)+self.scale*self.res*y),((self.scale*10)+self.scale*(self.res*x+self.res),(self.scale*10)+self.scale*(self.res*y+self.res)),red,-1)
		
		# check if the next parent exists (if it does not then the end of the path has been reached)
		if n.getPathParent() != None:
			self.build_path(n.getPathParent())