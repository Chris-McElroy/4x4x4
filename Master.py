from Board import *
from Display import *
from AIs.Brain import *
from AIs.Human import *
import time
import sys

class Master:
	""" controls everything going on """

	#constructor	
	def __init__(self):
		""" Creates display and initial menu """
		# nothing much to do here yet until display is better
		self.b = Board()
		self.d = Display(self.b)
		self.n = 0
		self.forced = False

	def playGame(self, players, p1):
		"""
		starts game between players 1 and 2
		players holds both players, whether AI or real
		player 1 is X's, player 2 is O's
		p1 holds which player will play first
		"""

		self.b.clearBoard()
		self.d.initializeBoard()
		continueGame = True
		self.forced = False
		self.n = p1

		while (continueGame):
			titleText = "Player " + str(self.n) + "'s Turn"
			if self.forced:
				titleText += " (forced)"
			self.d.title(titleText)

			self.d.updateBoard(self.b)
			i = 0
			while i < 20:
				self.d.displayBoard()
				pygame.time.wait(10)
				i += 1 # WHOOOPS FORGOT THIS

			nextMove = players[self.n-1].move(self.b, self.n)
			noProblem = self.b.move(self.n,nextMove)

			if not noProblem:
				print "HEY"
				break

			continueGame = self.checkBoard(nextMove)

			#n = self.b.otherNumber(n)
			self.n = 1 if (self.n == 2) else 2

		print "Game Over \n"


	def checkBoard(self,move):
		""" check board for wins and checks after a move """

		continueGame = True # can be assumed given that we got here

		wins = len(self.b.openLinesForPoint(self.n,move,4))
		checkMate = self.checkCheckmates(move)
		checks = self.b.findLines(self.n,3)

		if wins > 0:
			continueGame = False
			self.d.title("Player " + str(self.n) + " Wins!\nThey got 4 in a row!")

			self.d.updateBoard(self.b)
			self.d.displayShittyBoard()

		if checkMate:
			continueGame = False
			self.d.title("Player " + str(self.n) + " Wins!\nThey got checkmate!")

			self.d.updateBoard(self.b)
			self.d.displayShittyBoard()

		if (len(checks) > 0 and continueGame):
			checkPoints = self.b.lineToPoints(checks[0])
			checkString = ""
			for point in checkPoints:
				if self.b.pointToValue(point) == 0:
					self.d.checkPoint(point)
					checkString = self.pointToString(point)
					print "Move at: " + checkString
					self.forced = True
			# self.d.title("Check! Player " + str(self.b.otherNumber(self.n)) + " must respond at " + checkString + "!				")

		else:
			self.d.uncheckPoint()
			self.forced = False

		return continueGame

	def pointToString(self, p):
		""" turns a point into a string of numbers that should be inputed """
		string = ""
		for n in p:
			string += str(1+n)
		return string

	def checkCheckmates(self,move):
		""" check board for checkmates after a move """

		checkMate = False
		points = self.b.myPoints(self.n)

		for p in points:
			checks = self.b.openLinesForPoint(self.n,p,3)
			if len(checks) > 1:
				checkMates = True

		return checkMate

tryTo = Master()
player1 = Brain(tryTo.b,1)
player2 = Human(tryTo.b,2)
tryTo.playGame([player1,player2],1)









