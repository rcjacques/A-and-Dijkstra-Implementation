'''
@Author: Rene Jacques
March 18, 2019
'''

import cv2, math
import numpy as np

# define colors
red = (0,0,255)
green = (0,255,0)
blue = (255,0,0)
black = (0,0,0)
white = (255,255,255)

def line_eq(p1,p2):
	'''Equation for a line derived from two points'''
	slope = 1.0*(p2[0]-p1[0])/(p2[1]-p1[1])
	intercept = p2[0]-slope*p2[1]

	return slope,intercept

def ellipse_eq(center,width,height,x,y):
	'''Checks if x,y are within an ellipse described by center, width, height'''
	if (((1.0*center[0]-x)**2)/(width**2))+(((1.0*center[1]-y)**2)/(height**2)) <= 1:
		return True
	return False

def circle_eq(center,x,y,radius):
	'''Checks if x,y are within a circle described by center, radius'''
	if (center[0]-x)**2+(center[1]-y)**2 <= radius**2:
		return True
	return False

def mink_sum(A,B):
	'''Enlarges shape A with shape B using Minkowski Sum'''
	output = []
	for a in A:
		for b in B:
			# sum Ax, Bx and sum Ay, By to get the new shape
			output.append([a[0]+b[0],a[1]+b[1]])
	return output

class Map_Builder:
	'''Builds the map of the obstacles as well as the grid space describing the obstacles'''
	def __init__(self):
		pass

	def create_map(self,res,clearance,radius,draw=False):
		'''Creates the maps'''
		res = int(res)
		if res == 0:
			res = 1

		dist = clearance+radius

		# map: create empty image the size of the map and make it white
		img = np.zeros((150,250),np.uint8)
		img[np.where(img==0)] = 255 

		img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
		
		# map grid: create empty image the size of the map and make it white
		grid_img = np.zeros((150,250),np.uint8)
		grid_img[np.where(grid_img==0)] = 255

		grid_img = cv2.cvtColor(grid_img,cv2.COLOR_GRAY2BGR)

		# minkowski: create empty image the size of the map and make it white
		mink = np.zeros((150,250),np.uint8)
		mink[np.where(mink==0)] = 255

		mink = cv2.cvtColor(mink,cv2.COLOR_GRAY2BGR)

		# minkowski grid: create empty image the size of the map and make it white
		mink_grid = np.zeros((150,250),np.uint8)
		mink_grid[np.where(mink_grid==0)] = 255

		mink_grid = cv2.cvtColor(mink_grid,cv2.COLOR_GRAY2BGR)

		# minkowski mpa: create empty image the size of the map and make it white
		mink_map = np.zeros((150,250),np.uint8)
		mink_map[np.where(mink_map==0)] = 255

		mink_map = cv2.cvtColor(mink_map,cv2.COLOR_GRAY2BGR)

		# define robot shape
		rob_x = np.linspace(-dist,dist,num=1+2*dist,dtype=np.int32)
		rob_y = np.linspace(-dist,dist,num=1+2*dist,dtype=np.int32)

		rob_circle = []

		# create list of points in robot circle
		for x in rob_x:
			for y in rob_y:
				if circle_eq((0,0),x,y,dist):
					rob_circle.append([x,y])

		rob_circle = np.array([rob_circle])
		rob_circle = rob_circle[0]

		#obstacle 1: rectangle
		rx,ry = 50,60 #x,y
		rw,rh = 50,45

		#obstacle 2: polygon
		p1 = (150-56,125) #y,x
		p2 = (150-52,163)
		p3 = (150-90,170)
		p4 = (150-52,193)
		p5 = (150-15,173)
		p6 = (150-15,150)

		m1,b1 = line_eq(p1,p2)
		m2,b2 = line_eq(p2,p3)
		m3,b3 = line_eq(p3,p4)
		m4,b4 = line_eq(p4,p5)
		m5,b5 = line_eq(p5,p6)
		m6,b6 = line_eq(p6,p1)

		#obstacle 3: elipse
		ex,ey = 140,30 #center coordinates
		ew,eh = 15,6 #width, height

		#obstacle 4: circle
		cx,cy = 190,20 #center coordinates
		cr = 15 #radius

		# initialize grid space
		grid = {}
		for i in range(img.shape[1]):
			for j in range(img.shape[0]):
				grid[i,j] = 0

		# initialize shape containers
		square = []
		poly = []
		ellipse = []
		circle = []
		
		#color in obstacles for map display and put obstacle points in their containers
		for row in range(img.shape[0]):
			for col in range(img.shape[1]):
				if col >= rx and col <= rx+rw and row >= ry-(rh/2) and row <= ry+(rh/2):
					img[row,col] = 0
					cv2.rectangle(grid_img,(res*int(1.0*col/res),res*int(1.0*row/res)),(res*int(1.0*col/res)+res,res*int(1.0*row/res)+res),black,-1)
					cv2.circle(mink,(col,row),res,red,-1)
					square.append([col,row])

				if (row >= m1*col+b1 or row >= m2*col+b2) and row >= m3*col+b3 and row <= m4*col+b4 and row <= m5*col+b5 and row <= m6*col+b6:
					img[row,col] = 0
					cv2.rectangle(grid_img,(res*int(1.0*col/res),res*int(1.0*row/res)),(res*int(1.0*col/res)+res,res*int(1.0*row/res)+res),black,-1)
					cv2.circle(mink,(col,row),res,red,-1)
					poly.append([col,row])

				if ellipse_eq((ex,ey),ew,eh,col,row):
					img[row,col] = 0
					cv2.rectangle(grid_img,(res*int(1.0*col/res),res*int(1.0*row/res)),(res*int(1.0*col/res)+res,res*int(1.0*row/res)+res),black,-1)
					cv2.circle(mink,(col,row),res,red,-1)
					ellipse.append([col,row])

				if circle_eq((cx,cy),col,row,cr):
					img[row,col] = 0
					cv2.rectangle(grid_img,(res*int(1.0*col/res),res*int(1.0*row/res)),(res*int(1.0*col/res)+res,res*int(1.0*row/res)+res),black,-1)
					cv2.circle(mink,(col,row),res,red,-1)
					circle.append([col,row])

		# calculate minkowski shapes
		mink_square = mink_sum(square,rob_circle)
		mink_poly = mink_sum(poly,rob_circle)
		mink_ellipse = mink_sum(ellipse,rob_circle)
		mink_circle = mink_sum(circle,rob_circle)

		# color in minkowski shapes and fill grid with walls in the correct locations
		for point in mink_square:
			if point[1] >= 0 and point[0] >= 0:
				mink_grid[point[1],point[0]] = black
				grid[int(1.0*point[0]/res),int(1.0*point[1]/res)] = 1
				cv2.rectangle(mink_map,(res*int(1.0*point[0]/res),res*int(1.0*point[1]/res)),(res*int(1.0*point[0]/res)+res,res*int(1.0*point[1]/res)+res),black,-1)

		for point in mink_poly:
			if point[1] >= 0 and point[0] >= 0:
				mink_grid[point[1],point[0]] = black
				grid[int(1.0*point[0]/res),int(1.0*point[1]/res)] = 1
				cv2.rectangle(mink_map,(res*int(1.0*point[0]/res),res*int(1.0*point[1]/res)),(res*int(1.0*point[0]/res)+res,res*int(1.0*point[1]/res)+res),black,-1)

		for point in mink_ellipse:
			if point[1] >= 0 and point[0] >= 0:
				mink_grid[point[1],point[0]] = black
				grid[int(1.0*point[0]/res),int(1.0*point[1]/res)] = 1
				cv2.rectangle(mink_map,(res*int(1.0*point[0]/res),res*int(1.0*point[1]/res)),(res*int(1.0*point[0]/res)+res,res*int(1.0*point[1]/res)+res),black,-1)

		for point in mink_circle:
			if point[1] >= 0 and point[0] >= 0:
				mink_grid[point[1],point[0]] = black
				grid[int(1.0*point[0]/res),int(1.0*point[1]/res)] = 1
				cv2.rectangle(mink_map,(res*int(1.0*point[0]/res),res*int(1.0*point[1]/res)),(res*int(1.0*point[0]/res)+res,res*int(1.0*point[1]/res)+res),black,-1)

		#Expand Bounding Walls
		cv2.rectangle(mink_grid,(0,0),(mink_grid.shape[1],dist),black,-1)
		cv2.rectangle(mink_grid,(mink_grid.shape[1]-dist,0),(mink_grid.shape[1],mink_grid.shape[0]),black,-1)
		cv2.rectangle(mink_grid,(0,mink_grid.shape[0]-dist),(mink_grid.shape[1],mink_grid.shape[0]),black,-1)
		cv2.rectangle(mink_grid,(0,0),(dist,mink_grid.shape[0]),black,-1)

		for i in range(mink_grid.shape[1]//res):
			if dist == 0:
				pass
			elif dist <= res:
				grid[i,0] = 1
				grid[i,mink_grid.shape[0]//res-1] = 1
				cv2.rectangle(mink_map,(i*res,0),(i*res+res,res),black,-1)
				cv2.rectangle(mink_map,(i*res,mink_grid.shape[0]-res),(i*res+res,mink_grid.shape[0]),black,-1)
			elif dist > res:
				for k in range(math.ceil(dist/res)):
					grid[i,k] = 1
					grid[i,mink_grid.shape[0]//res-1-k] = 1
					cv2.rectangle(mink_map,(i*res,k*res),(i*res+res,k*res+res),black,-1)
					cv2.rectangle(mink_map,(i*res,mink_grid.shape[0]-((k+1)*res)+res),(i*res+res,mink_grid.shape[0]-(k+1)*res),black,-1)

		for j in range(mink_grid.shape[0]//res):
			if dist == 0:
				pass
			elif dist <= res:
				grid[0,j] = 1
				grid[mink_grid.shape[1]//res-1,j] = 1
				cv2.rectangle(mink_map,(0,j*res),(res,j*res+res),black,-1)
				cv2.rectangle(mink_map,(mink_grid.shape[1]-res,j*res),(mink_grid.shape[1],j*res+res),black,-1)
			elif dist > res:
				for k in range(math.ceil(dist/res)):
					grid[k,j] = 1
					grid[mink_grid.shape[1]//res-1-k,j] = 1
					cv2.rectangle(mink_map,(k*res,j*res),(k*res+res,j*res+res),black,-1)
					cv2.rectangle(mink_map,(mink_grid.shape[1]-(k*res)-res,j*res),(mink_grid.shape[1]-k*res,j*res+res),black,-1)

		# save maps as pngs
		cv2.imwrite('obst_map.png',img)
		cv2.imwrite('mink_map.png',mink_grid)

		# draw maps 
		if draw:
			cv2.imshow('Map',cv2.resize(img,(0,0),fx=3,fy=3))
			cv2.imshow('Grid Map',cv2.resize(grid_img,(0,0),fx=3,fy=3))
			cv2.imshow('Minkowski Map',cv2.resize(mink_map,(0,0),fx=3,fy=3))
			cv2.imshow('Minkowski Grid',cv2.resize(mink_grid,(0,0),fx=3,fy=3))

			cv2.waitKey(0)
			cv2.destroyAllWindows()

		return grid

def test():
	print('start')
	m = Map_Builder()
	grid = m.create_map(5,6,0,draw=True)
	print('finished')

if __name__ == '__main__':
	test()