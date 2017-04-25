from Board import *
from Display import *
from Brain import *
from Human import *
import time

class Master:
	""" controls everything going on """

	#constructor	
	def __init__(self):
		""" Creates display and initial menu """
		# nothing much to do here yet until display is better
		self.b = Board()
		self.d = Display(self.b)
		self.n = 0

	def playGame(self, players, p1):
		"""
		starts game between players 1 and 2
		players holds both players, whether AI or real
		player 1 is X's, player 2 is O's
		p1 holds which player will play first
		"""

		self.b.clearBoard()
		continueGame = True
		self.n = p1

		while (continueGame):

			print "Player " + str(self.n) + "'s Turn:"

			self.d.updateBoard(self.b)
			self.d.displayShittyBoard()

			time.sleep(1)

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
		checks = len(self.b.findLines(n,3))

		if wins > 0:
			continueGame = False
			print "Player " + str(self.n) + " Wins!"
			print "They got 4 in a row!"

			self.d.updateBoard(self.b)
			self.d.displayShittyBoard()

		if checkMate:
			continueGame = False
			print "Player " + str(self.n) + " Wins!"
			print "They got checkmate!"

			self.d.updateBoard(self.b)
			self.d.displayShittyBoard()

		if (checks > 0 and continueGame):
			print "\nCheck! Player " + str(self.b.otherNumber(self.n)) + " must respond!"

		return continueGame

	def checkCheckmates(self,move):
		""" check board for checkmates after a move """

		checkMate = False
		points = self.b.myPoints(self.n)

		for p in points:
			checks = self.b.openLinesForPoint(self.n,p,3)
			if len(checks) > 1:
				checkMates = True

		return checkMate













