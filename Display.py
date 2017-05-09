import sys
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
		self.rects = [[[0 for i in range(4)] for j in range(4)] for k in range(4)]
		self.mostRecentClick = False
		self.approvedMove = False
		self.click_n = 0
		self.win_n = 0
		self.titleText = ""
		self.winningMove = False

	def mainMenu(self,AIList):
		""" displays and checks for the main menu """

		pygame.init()
		display = (800,600)
		self.gameDisplay = pygame.display.set_mode(display)
		self.title("Welcome to Tic Tac Toe! Please select 2 players below!")

		buttons = self.createButtons(AIList)

		inMenu = True
		players = [None, None, None]
		while inMenu:
			start = self.checkMenu(players, AIList, buttons)
			if start:
				return players

			self.gameDisplay.fill((0,0,0))


			text = "Welcome to 4x4x4 Tic Tac Toe!"
			self.displayText(text,35,(400,100))

			self.displayButtons(AIList, players, buttons)
			
			pygame.display.update()
			pygame.time.wait(15)

	def createButtons(self,AIList):
		""" returns the rectangles holding the buttons """
		buttons = [[None],[None]]
		for LR in range(2):
			yPos = 150
			for AI in AIList[1:]:
				xPos = 100 if LR == 0 else 500
				yPos += 100
				dims = (200,50)
				buttons[LR] += [pygame.Rect((xPos,yPos),dims)]
		return buttons


	def checkMenu(self, players, AIList, buttons):
		""" checks for button presses in the menu """
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()

				# check if the AIs are selected
				for LR in range(2):
					for i in range(len(AIList)-1):
						if buttons[LR][i+1].collidepoint(pos):
							players[LR] = AIList[i+1]
							self.title("Welcome to 4x4x4 Tic Tac Toe!  " + players[LR].__name__ + " player selected.")

				# check if the Go button is clicked
				if pygame.Rect((350,400),(100,100)).collidepoint(pos) and len(players) == 3:
					return True
		return False


	def displayButtons(self, AIList, players, buttons):
		""" displays the buttons for the board """
		for LR in range(2):
			yPos = 150
			for AI in AIList[1:]:
				xPos = 100 if LR == 0 else 500
				yPos += 100
				dims = (200,50)
				pygame.draw.rect(self.gameDisplay, (0,0,255),((xPos,yPos),dims))
				if AI == players[LR]:
					pygame.draw.rect(self.gameDisplay, (255,255,255),((xPos,yPos),dims), 5)
				self.displayText(AI.__name__, 20, (xPos+100, yPos+25))

		if players[0] and players[1]:
			pygame.draw.rect(self.gameDisplay, (0,255,0),((350,400),(100,100)))
			self.displayText("Go!", 30, (400, 450))


	def displayText(self,text,size,center):
		largeText = pygame.font.Font('freesansbold.ttf',size)
		text = largeText.render(text, True, (255, 255, 255))
		textR = text.get_rect()
		textR.center = (center)
		self.gameDisplay.blit(text, textR)

	def initializeBoard(self):
		""" prepares to display board """

		pygame.init()
		display = (800, 600)
		self.gameDisplay = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
		self.title("")

		self.createRects()

		gluPerspective(3.5, (float(display[0])/float(display[1])), 0.1, 240)
		glTranslatef(0.0,0, -200)
		glRotatef(20,0.3,0.5,0.04)

	def getMove(self):
		self.checkInputs()
		if self.approvedMove:
			move = self.mostRecentClick
			self.approvedMove = False
			self.mostRecentClick = False
			return move
		else:
			return False

	def checkInputs(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				self.click_n = 0

				# get a list of all sprites that are under the mouse cursor
				clicked = False
				for i in range(4):
					for j in range(4):
						for k in range(4):
							if self.rects[i][j][k].collidepoint(pos):
								clicked = True
								if self.mostRecentClick == [i,j,k]:
									self.approvedMove = True
								else:
									self.mostRecentClick = [i,j,k]
				if not clicked:
					self.mostRecentClick = clicked

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					self.pauseDisplay()

	def pauseDisplay(self):
		""" manages the paused game """
		paused = True
		oldTitle = self.titleText
		self.title("PAUSED")

		glClearColor(.4,.4,.4,.4)
		self.displayBoard()

		while paused:
			pygame.time.wait(10)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_1:
						self.dir = 1
					if event.key == pygame.K_2:
						self.dir = 2
					if event.key == pygame.K_3:
						self.dir = 3
					if event.key == pygame.K_4:
						self.dir = 4
					if event.key == pygame.K_5:
						self.dir = 5
					if event.key == pygame.K_6:
						self.dir = 6

					if event.key == pygame.K_LEFT:
						glRotated(10,0,1,0)
					if event.key == pygame.K_RIGHT:
						glRotated(-10,0,1,0)
					if event.key == pygame.K_UP:
						glRotated(10,1,0,0)
					if event.key == pygame.K_DOWN:
						glRotated(-10,1,0,0)
					
					if event.key == pygame.K_SPACE:
						paused = False

					glClearColor(.4,.4,.4,.4)
					self.displayBoard()

		self.title(oldTitle)
		self.dir = 1

		display = (800,600)
		glLoadIdentity();
		gluPerspective(3.5, (float(display[0])/float(display[1])), 0.1, 240)
		glTranslatef(0.0,0, -200)
		glRotatef(20,0.3,0.5,0.04)

		self.displayBoard()

	def displayBoard(self):
		""" clears screen and redisplays board """

		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		self.checkInputs()

		self.displayPieces()

		pygame.display.flip()

		glClearColor(0,0,0,0)

	def title(self,string):
		""" sets the title of the display to be string """
		pygame.display.set_caption(string)
		self.titleText = string

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

			if p == self.mostRecentClick:
				self.click_n += 1
				if self.click_n < 4:
					v = 4
				elif self.click_n > 6:
					self.click_n = 0

			if p == self.winningMove:
				self.win_n += 1
				if self.win_n < 4:
					v = 4
				elif self.win_n > 6:
					self.win_n = 0

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
			points = [[3-k,3-i,3-j] for i in range(4) for j in range(4) for k in range(4)]

		elif self.dir == 3:
			points = [[3-i,k,3-j] for i in range(4) for j in range(4) for k in range(4)]

		elif self.dir == 4:
			points = [[k,i,3-j] for i in range(4) for j in range(4) for k in range(4)]

		elif self.dir == 5:
			points = [[i,j,3-k] for i in range(4) for j in range(4) for k in range(4)]

		elif self.dir == 6:
			points = [[3-i,j,k] for i in range(4) for j in range(4) for k in range(4)]

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

	def cube(self, p, v):
		d = .4
		verticies = [(p[0]+i,p[1]+j,p[2]+k) for i in [-d,d] for j in [-d,d] for k in [-d,d]]
		edges = ((0,1),(0,2),(0,4),(1,3),(1,5),(2,3),(2,6),(3,7),(4,5),(4,6),(5,7),(6,7))
		surfaces = ((0,1,2,3),(0,1,5,4),(0,2,6,4),(7,6,5,4),(7,6,2,3),(7,5,1,3))

		color = self.cubeColor(v)

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

	def cubeColor(self,v):
		color = (1,1,1)
		if v == 1:
			color = (0,1,0)
		elif v == 2:
			color = (0,1,1)
		elif v == 0:
			color = (.2,.2,.2)
		elif v == 3:
			color = (1,0,0)
		elif v == 4:
			color = (1,1,0)

		return color

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

	def setWinningMove(self,p):
		""" sets the winning move """
		self.winningMove = p

