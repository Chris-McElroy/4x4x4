import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from Board import *

class Display:
	""" Displays the board """

	#constructor	
	def __init__(self, board):
		""" gets variables set up """

		self.dir = 1 # direction to view board, can be 1-6
		self.b = board

	def initializeBoard(self):
		""" prepares to display board """

		pygame.init()
		display = (800, 600)
		pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
		gluPerspective(3.5, (float(display[0])/float(display[1])), 0.1, 240)
		glTranslatef(0.0,0, -200)
		glRotatef(20,.3,.5,0)

	def displayShittyBoard(self):
		""" displays the board reallllyy shitty """
		for i in range(4):
			lineString = ""
			for j in range(4):
				l = j + 4*i
				values = self.b.lineToValues(l)
				for v in values:
					lineString += self.valueToMark(v) + " "
				lineString += "  "
			print lineString

	def checkInputs(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

	def displayBoard(self):
		""" clears screen and redisplays board """

		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		self.checkInputs()

		self.displayPieces()

		# self.displayStructure()

		pygame.display.flip()

	def displayPieces(self):
		""" displays all the pieces on the board """

		points = self.getPoints()

		# janky old positions
		# positions = [[1.2*(-1.5+i)+.2*j,1.2*3*(-1.5+j),1.2*(-1.5+k)-2.7*j**(.5)] for i in range(4) for j in range(4) for k in range(4)]

		positions = [[2.7*(-1.5+i),2*1.5*(-1.5+j),2.7*(-1.5+k)] for i in range(4) for j in range(4) for k in range(4)]
		for i in range(64):
			p = points[i]
			pos = positions[i]
			v = self.b.b[p[0]][p[1]][p[2]]
			self.cube(pos, v)

	def getPoints(self):
		""" gets the correct points based on the value of self.d """

		points = []

		if self.dir == 1:
			points = [[i,3-k,3-j] for i in range(4) for j in range(4) for k in range(4)]

		elif self.dir == 2:
			points = [[i,j,k] for i in range(4) for j in range(4) for k in range(4)]

		elif self.dir == 3:
			points = [[i,j,k] for i in range(4) for j in range(4) for k in range(4)]

		elif self.dir == 4:
			points = [[i,j,k] for i in range(4) for j in range(4) for k in range(4)]

		elif self.dir == 5:
			points = [[i,j,k] for i in range(4) for j in range(4) for k in range(4)]

		elif self.dir == 6:
			points = [[i,j,k] for i in range(4) for j in range(4) for k in range(4)]

		return points

	def valueToMark(self,v):
		""" converts value to a mark """
		mark = ""

		if (v == 0):
			mark = "-"

		elif (v == 1):
			mark = "X"

		elif (v == 2):
			mark = "O"

		return mark

	def updateBoard(self,board):
		""" updates board """

		self.b = board

	def cube(self, p, n):
		d = .4
		verticies = [(p[0]+i,p[1]+j,p[2]+k) for i in [-d,d] for j in [-d,d] for k in [-d,d]]
		edges = ((0,1),(0,2),(0,4),(1,3),(1,5),(2,3),(2,6),(3,7),(4,5),(4,6),(5,7),(6,7))
		surfaces = ((0,1,2,3),(0,1,5,4),(0,2,6,4),(7,6,5,4),(7,6,2,3),(7,5,1,3))

		color = (1,1,1)
		if n == 1:
			color = (0,1,0)
		elif n == 2:
			color = (0,1,1)
		elif n == 0:
			color = (.2,.2,.2)

		glBegin(GL_QUADS)
		glColor3fv(color)
		for surface in surfaces:
			x = 0
			for vertex in surface:
				x+=1
				glVertex3fv(verticies[vertex])
		glEnd()

		glBegin(GL_LINES)
		glColor3fv((0,0,0))
		for edge in edges:
			for vertex in edge:
				glVertex3fv(verticies[vertex])
		glEnd()






