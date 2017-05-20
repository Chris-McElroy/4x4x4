import time
import random



class Wildfire:
	""" functions as the player for a real life person """

	def __init__(self):
		""" Stores player info for easy access """
		self.MAX_FORCES = 9
		self.forceCache = set()

	def move(self,board,n, d):
		"""
		The main function for this class.  Returns the point the person wants to move in.
		"""

		# obvious - if you can win, do it. If you can't and they can, block it.
		if self.winningMove(board, n):
			return self.winningMove(board, n)
		if self.winningMove(board, board.otherNumber(n)):
			return self.winningMove(board, board.otherNumber(n))

		# if we have a winning sequence of forces, take it
		winningForces = self.forceCheck(board, n, self.MAX_FORCES)
		if winningForces:
			return winningForces[0][0]

		# if we will have a losing sequence of forces, we need to take action against it.
		otherForces = self.forceCheck(board, board.otherNumber(n), self.MAX_FORCES)
		# currently just do shittiest possible block
		if otherForces:
			return otherForces[0][0]


		bestScore = -999
		bestMoves = []
		i = 0
		for point in board.openPoints():
			i += 1
			d.displayProgress("Main Loop: ", (100*i)/len(board.openPoints()))

			board.move(n, point)
			score = self.evaluatePosition(board, n)
			board.clearPoint(point)

			if score > bestScore:
				bestScore = score
				bestMoves = [point]
			elif score == bestScore:
				bestMoves.append(point)

		return random.choice(bestMoves)


	def winningMove(self, board, n):
		""" Checks if there is a winning move for player n and if there is, returns it"""
		forces = board.findLines(n, 3).copy()
		if len(forces) > 0:
			for point in board.lineToPoints(next(iter(forces))):
				if board.pointToValue(point) == 0:
					return point
	
	def forceCheck(self, board, n, movesLeft):
		""" Wrapper function for forcecheckrec"""
		self.forceCache.clear()
		return self.forceCheckRec(board, n, movesLeft)

	def forceCheckRec(self, board, n, movesLeft):
		""" Recursively finds all possible forcing sequences with {movesleft} moves
			for player n up to reordering and returns them"""

		if board.hash() in self.forceCache:
			# we've already visited this, no need to do so again
			return False

		if self.winningMove(board, n):
			self.forceCache.add(board.hash())
			# this looks weird, but we're returning a list of
			# possible lists of moves
			return [[self.winningMove(board, n)]]

		if self.winningMove(board, board.otherNumber(n)) or movesLeft == 0:
			self.forceCache.add(board.hash())
			return False

		possibleForces =  board.findLines(n, 2)

		wins = []

		for force in possibleForces:
			openSpots = filter(lambda p: board.pointToValue(p) == 0, board.lineToPoints(force))

			board.move(n, openSpots[0])
			board.move(board.otherNumber(n), openSpots[1])

			wins1 = self.forceCheckRec(board, n, movesLeft-1)
			board.clearPoint(openSpots[0])
			board.clearPoint(openSpots[1])

			# we don't have getters or setters because this is sus
			# kids, don't do this at home

			if wins1:
				self.forceCache.add(board.hash())
				wins += [openSpots + moves for moves in wins1]
			
			board.move(n, openSpots[1])
			board.move(board.otherNumber(n), openSpots[0])

			wins2 = self.forceCheckRec(board, n, movesLeft-1)
			board.clearPoint(openSpots[0])
			board.clearPoint(openSpots[1])

			if wins2:
				self.forceCache.add(board.hash())
				openSpots.reverse()
				wins += [openSpots + moves for moves in wins2]

		return wins

	def evaluatePosition(self, board, n):
		score = 0
		score += len(board.findLines(n,1))
		score += len(board.findLines(n,2))
		score -= len(board.findLines(board.otherNumber(n),1))
		score -= len(board.findLines(board.otherNumber(n),2))

		return score

	def colors(self):
		""" returns the colors of grey """
		return [(136, 204, 136),(17, 102, 17)]
