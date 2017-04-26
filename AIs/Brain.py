from Board import *
import random

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
		self.decided = False
		self.assured = False

		self.undecided = [-1, -1, -1]
		self.ply = 4

	def move(self,board,n):
		"""
		The main function for this class.  Returns the point the AI wants to move in.
		"""

		self.updateAll(board,n)

		#bestPoint = self.moves[0]
		#return bestPoint

		other = Brain(self.b,self.o)

		# check for four in a row on both sides
		move = self.assuredMove()
		if self.decided:
			return move

		other.lookAhead()
		if other.assured: # checks for their strong lookahead
			self.moves = self.guardLookAhead()

		move = self.lookAhead() # casual lookahead
		return move

	def chooseMove(self,moves):
		"""
		chooses a move from the available one in the determined tiebreaking way
		Currently: Random
		"""

		if (len(moves) > 0):
			return random.choice(moves)
		return self.undecided

	def assuredMove(self):
		other = Brain(self.b,self.o)
		self.decided, self.assured, other.decided, other.assured = (False,)*4

		# check for four in a row on both sides
		move0 = self.fourInARow()
		if self.assured:
			print "I have the win\n"
			return move0

		move1 = other.fourInARow()
		if other.assured:
			return move1

		move2 = self.checkCheckmates()
		if self.assured:
			print "I have mate\n"
			return move2

		move3 = self.forceToFinish()
		if self.assured:
			print "I have the force\n"
			return move3

		move4 = self.lookAhead()
		if self.assured: # checks for a strong lookahead
			print "I have the win."
			return move4

		return self.undecided

	def fourInARow(self):
		""" check if there's anywhere self could go to get four in a row """

		winningMoves = []
		lines = self.b.findLines(self.n,3)

		if (len(lines) > 0):
			self.assured = True
			self.decided = True
			for l in lines:
				values = self.b.lineToValues(l)
				for i in range(4): # double counts double 4-in-a-rows bc hell yeah
					if values[i] == 0:
						move = self.b.lineToPoints(l)[i]
						winningMoves += [move]

		return self.chooseMove(winningMoves)

	def checkCheckmates(self):
		""" checks for any checkmate moves """

		pairs = self.b.findForces(self.n)
		moves = []
		winningMoves = []
		for points in pairs:
			for p in points:
				if p in moves:
					if p not in winningMoves:
						winningMoves += [p]
						self.assured = True
						self.decided = True
				else:
					moves += [p]
		return self.chooseMove(winningMoves)

	def forceToFinish(self):
		"""
		Forces the other player until there are no forces left, or someone wins
		Returns the point used successfully if player n wins,
		and self.undecided if the other player wins or nothing happens
		"""

		pairs = self.b.findForces(self.n)
		winningMoves = self.recursiveForceToFinish(pairs)

		return self.chooseMove(winningMoves) 

	def recursiveForceToFinish(self, pairs):
		""" solves force to finish recursively """

		lenPairs = len(pairs)
		moves = []

		if lenPairs == 0:
			return moves

		for pairN in range(lenPairs):
			for i in [0,1]:
				newBoard = Board()
				newAI = Brain(newBoard,self.n)
				newAI.b.copyBoard(self.b)
				newAI.updateForForce(pairs[pairN],i)
				if newAI.assured:
					self.assured = True
					self.decided = True
					moves += [pairs[pairN][i]]
				else:
					newPairs = newAI.b.findForces(self.n)
					futureMoves = newAI.recursiveForceToFinish(newPairs)
					if len(futureMoves) > 0:
						self.assured = True
						self.decided = True
						moves += [pairs[pairN][i]]

		return moves

	def lookAhead(self):
		"""
		Tries moving for player n at point p then rechecks board
		Returns the point used successfully if player n wins,
		and p = [-1,-1,-1] if the other player wins or nothing happens
		"""

		numMoves = self.b.numMoves(self.n)[0]
		moves = [[0,0,0],[0,0,3],[3,0,0],[2,0,1],[3,3,3],[3,3,3]]
		return moves[numMoves]

		currentPly = self.ply
		currentMoves = self.moves

		while (currentPly > 0):
			return [0,1,3]

		if self.assured:
			return [0,1,3]

	def updateForPoint(self, p):
		"""
		Updates pairs, moves, and lines after point p has been filled
		More efficient than updating fully each time
		"""

	def updateForForce(self, pair, myNum):
		"""
		Fills given pair and checks for win along given lines
		myNum is position chosen by player n (either 0 or 1)
		"""

		otherNum = 0 if myNum == 1 else 1

		self.b.move(self.n,pair[myNum])
		self.b.move(self.o,pair[otherNum])

		self.updateWinsForPoint(pair[myNum])

	def updateAll(self, board, n):
		"""
		Updates all pairs, moves and lines for the current board
		"""
		self.b = board # Board object, not array
		self.n = n
		self.o = self.b.otherNumber(self.n)
		self.moves = self.b.openPoints()
		self.decided = False
		self.assured = False

	def updateWinsForPoint(self, p):
		"""
		Checks whether a just-filled point caused any wins
		"""
		wins = self.b.openLinesForPoint(self.n,p,4)
		if len(wins) > 0:
			self.assured = True
			self.decided = True

		wins = self.b.openLinesForPoint(self.o,p,4)
		if self.checkCheckmates() != self.undecided and len(wins) == 0:
			self.assured = True
			self.decided = True

	def checkWins(self, p):
		"""
		Returns True if p causes a win, False if the game is still being played
		"""



