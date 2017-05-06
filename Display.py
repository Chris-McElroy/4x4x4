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

		self.check_current = False
		self.check_n = 0
		self.check_p = [0,0,0]
		self.gameDisplay = None
		self.test4 = None
		self.rects = [[[0 for i in range(4)] for j in range(4)] for k in range(4)]
		self.mostRecentClick = [-1,-1,-1]
		self.num = 0

	def initializeBoard(self):
		""" prepares to display board """

		pygame.init()
		display = (800, 600)
		self.gameDisplay = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
		self.title("")

		self.createRects()

		gluPerspective(3.5, (float(display[0])/float(display[1])), 0.1, 240)
		glTranslatef(0.0,0, -200)
		glRotatef(20,.3,.5,0.04)

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

	def getMove(self):
		self.mostRecentClick = [-1,-1,-1]
		self.checkInputs()
		if self.mostRecentClick != [-1,-1,-1]:
			return self.mostRecentClick
		else:
			return False

	def checkInputs(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				self.mostRecentClick = [-1,-1,-1]

				# get a list of all sprites that are under the mouse cursor
				for i in range(4):
					for j in range(4):
						for k in range(4):
							if self.rects[i][j][k].collidepoint(pos):
								self.mostRecentClick = [i,j,k]
				self.title(str(self.mostRecentClick))

	def displayTestBox(self):
		n = 0

		while n < 100:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()

			n += 1

			pygame.draw.rect(self.gameDisplay,(255,255,0),[200,300,20,20])
			pygame.display.flip()

	def displayBoard(self):
		""" clears screen and redisplays board """

		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		self.checkInputs()

		self.displayPieces()

		#self.gameDisplay.fill((0,0,0))

		#pygame.draw.rect(self.gameDisplay,(255,255,0),[200,300,20,20])

		# self.displayStructure()

		pygame.display.flip()

	def title(self,string):
		""" sets the title of the display to be string """
		pygame.display.set_caption(string)

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

			if p == self.check_p and self.check_current:
				self.check_n += 1
				if self.check_n < 4:
					v = 3
				elif self.check_n > 6:
					self.check_n = 0

			self.cube(pos, v)

	def checkPoint(self,p):
		""" makes sure to show p later on flashing red """
		self.check_current = True
		self.check_n = 0
		self.check_p = p

	def uncheckPoint(self):
		""" unshows check once it's forced """
		self.check_current = False
		self.check_n = 0
		self.check_p = [0,0,0]

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
		elif n == 3:
			color = (1,0,0)

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


	def createRects(self):
		""" creates all the rectangles for clicking """
		width = 30
		height = 35
		n = 0

		for i in range(4):
			for j in range(4):
				for k in range(4):
					rectPos = self.getRectPos(i,j,k)
					self.rects[i][j][k] = pygame.Rect(rectPos,(width,height))
					n += 1

	def getRectPos(self,i,j,k):
		x = 250
		y = 106

		x += i*387/3
		y += i*(-8)

		x += j*(-117)/3
		y += j*(-22)

		x += 0
		y += k*441/3

		return (x,y)



newB = Board()
newD = Display(newB)
newD.initializeBoard()

