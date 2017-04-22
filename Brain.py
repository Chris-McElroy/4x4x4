from Board import *

class Brain:
	"""
	The AI class for tic tac toe.  Decides where the AI will go when fed with a board.
	"""

	def __init__(self, currentBoard, playerNumber):
		""" Stores board and player info for easy access """
		self.b = currentBoard # Board object, not array
		self.n = playerNumber
		self.o = self.b.otherNumber(self.n)
		self.moves = self.b.openPoints()
		self.pairs = self.b.findForces(self.n)
		self.lines = self.b.findLines(self.n,0)

	def move(self,board,n):
		"""
		The main function for this class.  Returns the point the AI wants to move in.
		"""
		bestPoint = self.b.openPoints()[0]
		return bestPoint

	def lookAhead(self, p):
		"""
		Tries moving for player n at point p then rechecks board
		Returns hypothetical new AI with updated info
		"""

	def forceToFinish(self):
		"""
		Forces the other player until there are no forces left, or someone wins
		Returns True if player n wins, False if the other player wins or nothing happens
		"""

	def updateForPoint(self, p):
		"""
		Updates pairs, moves, and lines after point p has been filled
		More efficient than updating fully each time
		"""

	def updateForForce(self, pair, myNum):
		"""
		Updates pairs after pair has been filled, and checks for win along given lines
		myNum is position chosen by player n (either 0 or 1)
		"""

	def updateAll(self):
		"""
		Updates all pairs, moves and lines for the current board
		"""

	def checkWinsForPoint(self, p):
		"""
		Checks whether a just-filled point caused any wins
		"""

	def checkWins(self, p):
		"""
		Returns True if p causes a win, False if the game is still being played
		"""



