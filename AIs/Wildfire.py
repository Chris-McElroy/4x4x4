import time
import random



class Wildfire:
	""" functions as the player for a real life person """

	def __init__(self):
		""" Stores player info for easy access """
		self.MAX_FORCES = 9
		self.forceCache = {}

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
		winningForce = self.forceCheck(board, n, self.MAX_FORCES)
		if winningForce:
			return winningForce

		# if we will have a losing sequence of forces, we need to take action against it.
		otherForce = self.forceCheck(board, board.otherNumber(n), self.MAX_FORCES)
		# currently just do shittiest possible block
		if otherForce:
			return otherForce


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


		# placeholder acting like a human until I fill in more.
		move = False
		while not move:
			time.sleep(.1)
			move = d.getMove()
		return move

	def winningMove(self, board, n):
		forces = board.findLines(n, 3).copy()
		if len(forces) > 0:
			for point in board.lineToPoints(next(iter(forces))):
				if board.pointToValue(point) == 0:
					return point
	
	def forceCheck(self, board, n, movesLeft):
		self.forceCache = {}
		return self.forceCheckRec(board, n, movesLeft)

	def forceCheckRec(self, board, n, movesLeft):

		if self.forceCache.has_key(board.hash()):
			return self.forceCache[board.hash()]

		if self.winningMove(board, n):
			self.forceCache[board.hash()] = self.winningMove(board, n)
			return self.winningMove(board, n)

		if self.winningMove(board, board.otherNumber(n)) or movesLeft == 0:
			self.forceCache[board.hash()] = 0
			return 0

		possibleForces =  board.findLines(n, 2)

		for force in possibleForces:
			openSpots = filter(lambda p: board.pointToValue(p) == 0, board.lineToPoints(force))

			board.move(n, openSpots[0])
			board.move(board.otherNumber(n), openSpots[1])

			success = self.forceCheckRec(board, n, movesLeft-1)
			board.clearPoint(openSpots[0])
			board.clearPoint(openSpots[1])

			# we don't have getters or setters because this is sus
			# kids, don't do this at home

			if success:
				self.forceCache[board.hash()] = openSpots[1]
				return openSpots[0]
			
			board.move(n, openSpots[1])
			board.move(board.otherNumber(n), openSpots[0])

			success = self.forceCheckRec(board, n, movesLeft-1)
			board.clearPoint(openSpots[0])
			board.clearPoint(openSpots[1])

			if success:
				self.forceCache[board.hash()] = openSpots[1]
				return openSpots[1]

		return 0

	def evaluatePosition(self, board, n):
		score = 0
		score += len(board.findLines(n,1))
		score += len(board.findLines(n,2))
		score -= len(board.findLines(board.otherNumber(n),1))
		score -= len(board.findLines(board.otherNumber(n),2))


		if self.forceCheck(board, board.otherNumber(n), self.MAX_FORCES-3) != 0:
			return 0

		return score

	def colors(self):
		""" returns the colors of grey """
		return [(136, 204, 136),(17, 102, 17)]
