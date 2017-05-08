import time
import random



class Wildfire:
	""" functions as the player for a real life person """

	def __init__(self, currentBoard, playerNumber):
		""" Stores player info for easy access """
		self.n = playerNumber
		self.MAX_FORCES = 6

	def move(self,board,n, d):
		"""
		The main function for this class.  Returns the point the person wants to move in.
		"""

		# obvious - if you can win, do it. If you can't and they can, block it.
		if self.winningMove(board, n):
			return self.winningMove(board, n)
		if self.winningMove(board, board.otherNumber(n)):
			return self.winningMove(board, board.otherNumber(n))

		winningForce = self.forceCheckRec(board, n, self.MAX_FORCES)
		if winningForce:
			return winningForce

		bestScore = 0
		bestMoves = []
		for point in board.openPoints():
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
		forces = board.findLines(n, 3)
		if len(forces) > 0:
			for point in board.lineToPoints(forces[0]):
				if board.pointToValue(point) == 0:
					return point
	
	def forceCheckRec(self, board, n, movesLeft):

		if self.winningMove(board, n):
			return self.winningMove(board, n)

		if self.winningMove(board, board.otherNumber(n)) or movesLeft == 0:
			return 0

		possibleForces =  board.findLines(n, 2)

		for force in possibleForces:
			openSpots = filter(lambda p: board.pointToValue(p) == 0, board.lineToPoints(force))

			board.move(n, openSpots[0])
			board.move(board.otherNumber(n), openSpots[1])

			success = self.forceCheckRec(board, n, movesLeft-1)
			board.clearPoint(openSpots[0])
			board.clearPoint(openSpots[1])

			if success:
				return openSpots[0]
			
			board.move(n, openSpots[1])
			board.move(board.otherNumber(n), openSpots[0])

			success = self.forceCheckRec(board, n, movesLeft-1)
			board.clearPoint(openSpots[0])
			board.clearPoint(openSpots[1])
			if success:
				return openSpots[1]

		return 0

	def evaluatePosition(self, board, n):
		score = 0
		score += len(board.findLines(n,1))
		score += 2 * len(board.findLines(n,2))
		score += 20 * (self.forceCheckRec(board, n, self.MAX_FORCES-2) != 0)

		if self.forceCheckRec(board, board.otherNumber(n), self.MAX_FORCES-2) != 0:
			return 0

		return score
