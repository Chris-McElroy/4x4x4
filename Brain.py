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
		self.decided = False
		self.assured = False

		self.undecided = [-1, -1, -1]
		self.ply = 4

	def move(self,board,n):
		"""
		The main function for this class.  Returns the point the AI wants to move in.
		"""

		self.updateAll(board,n)
		# other = Brain(self.b,self.o)

		bestPoint = self.moves[0]
		return bestPoint

		# check for four in a row on both sides
		move0 = self.assuredMove()
		if self.decided:
			return move0

		other.forceToFinish()
		if other.decided:
			self.moves = self.guardForces()

		move1 = self.lookAhead()
		if self.decided: # checks for a strong lookahead
			return move1

		other.lookAhead(other.ply)
		if other.decided: # checks for their strong lookahead
			self.moves = self.guardLookAhead()

		move2 = self.lookAhead() # casual lookahead
		return move2

	def assuredMove(self):
		other = Brain(self.b,self.o)
		self.decided = False
		other.decided = False

		# check for four in a row on both sides
		move1 = self.fourInARow()
		if self.decided:
			return move1

		move2 = other.fourInARow()
		if other.decided:
			return move2

		move3 = self.forceToFinish()
		if self.decided:
			return move3

		return self.undecided


	def lookAhead(self, p):
		"""
		Tries moving for player n at point p then rechecks board
		Returns the point used successfully if player n wins,
		and p = [-1,-1,-1] if the other player wins or nothing happens
		"""

	def forceToFinish(self):
		"""
		Forces the other player until there are no forces left, or someone wins
		Returns the point used successfully if player n wins,
		and p = [-1,-1,-1] if the other player wins or nothing happens
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

	def updateAll(self, board, n):
		"""
		Updates all pairs, moves and lines for the current board
		"""
		self.b = board # Board object, not array
		self.n = n
		self.o = self.b.otherNumber(self.n)
		self.moves = self.b.openPoints()
		self.pairs = self.b.findForces(self.n)
		self.lines = self.b.findLines(self.n,0)
		self.decided = False
		self.assured = False


	def updateWinsForPoint(self, p):
		"""
		Checks whether a just-filled point caused any wins
		"""

	def checkWins(self, p):
		"""
		Returns True if p causes a win, False if the game is still being played
		"""



