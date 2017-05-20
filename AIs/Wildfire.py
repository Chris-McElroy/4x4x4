import random
from Board import *

class Wildfire:
	""" functions as the player for a real life person """

	def __init__(self):
		""" Stores player info for easy access """
		self.MAX_FORCES = 7
		self.forceCache = set()
		self.step = ""

	def move(self,board,n, d):
		"""
		The main function for this class.  Returns the point the person wants to move in.
		"""

		# obvious - if you can win, do it. If you can't and they can, block it.

		if self.winningMove(board, n):
			return self.winningMove(board, n)
		if self.winningMove(board, board.otherNumber(n)):
			return self.winningMove(board, board.otherNumber(n))

		self.step  = "Finding Offensive Forces: "
		winningForces = self.findForces(board, n, self.MAX_FORCES, d)
		if winningForces:
			print "Found", len(winningForces), "winning forces"
			return winningForces[0][0]


		self.step  = "Finding Opponent's Forces: "
		otherForces = self.findForces(board, board.otherNumber(n), self.MAX_FORCES, d)
		
		possibleMoves = [p for p in board.openPoints() if p not in self.findCasualChecks(board, n)]
		if otherForces:
			self.step = "Analyzing Defensive Moves: "
			possibleMoves = self.findDefensiveMoves(board, n, otherForces, d)
		
		if not possibleMoves:
			self.setp = "Deciding Casual Checks"
			###### TODO: Better casual check analysis than 'pick one'
			possibleMoves = self.findCasualChecks(board, n)

		self.step = "Choosing From Acceptable Moves: "
		return self.pickMove(board, n, possibleMoves, d)

	def winningMove(self, board, n):
		""" Checks if there is a winning move for player n and if there is, returns it"""
		forces = board.findLines(n, 3).copy()
		if len(forces) > 0:
			for point in board.lineToPoints(next(iter(forces))):
				if board.pointToValue(point) == 0:
					return point

	def findCasualChecks(self, board, n):
		checks = []

		possibleForces =  board.findLines(n, 2)
		for force in possibleForces:
			openSpots = filter(lambda p: board.pointToValue(p) == 0, board.lineToPoints(force))
			checks += openSpots

		return checks
	
	def findForces(self, board, n, movesLeft, d):
		""" Wrapper function for findForcesrec"""
		self.forceCache.clear()
		return self.findForcesRec(board, n, movesLeft, d)

	def findForcesRec(self, board, n, movesLeft, d):
		""" Recursively finds all possible forcing sequences with {movesleft} moves
			for player n up to reordering and returns them"""

		if board.hash() in self.forceCache:
			# we've already visited this, no need to do so again
			return False

		if self.winningMove(board, n):
			self.forceCache.add(board.hash())
			# this looks weird, but we're returning a list of possible lists of moves
			return [[self.winningMove(board, n)]]

		if self.winningMove(board, board.otherNumber(n)) or movesLeft == 0:
			self.forceCache.add(board.hash())
			return False

		possibleForces =  board.findLines(n, 2)
		wins = []
		i = 0

		for force in possibleForces:

			openSpots = filter(lambda p: board.pointToValue(p) == 0, board.lineToPoints(force))
			openSpotsRev = [openSpots[1], openSpots[0]]

			for moves in [openSpots, openSpotsRev]:

				if movesLeft == self.MAX_FORCES:
					d.displayProgress(self.step, (100*i)/(2*len(possibleForces)))
					i+= 1

				board.move(n, moves[0])
				board.move(board.otherNumber(n), moves[1])

				winsRec = self.findForcesRec(board, n, movesLeft-1, d)
				board.clearPoint(moves[0])
				board.clearPoint(moves[1])

				if winsRec:
					self.forceCache.add(board.hash())
					wins += [moves + recMoves for recMoves in winsRec]
			
		return wins

	def pickMove(self, board, n, possibleMoves, d):
		""" uses the heuristic in evaluateMove to choose the best move
		from possibleMoves. if there are multiple, it chooses randomly"""
		bestScore = -float('inf')
		bestMoves = []
		i = 0
		for point in possibleMoves:
			i += 1
			d.displayProgress(self.step, (100*i)/len(possibleMoves))

			board.move(n, point)
			score = self.evaluatePosition(board, n)
			board.clearPoint(point)

			if score > bestScore:
				bestScore = score
				bestMoves = [point]
			elif score == bestScore:
				bestMoves.append(point)

		return random.choice(bestMoves)

	def evaluatePosition(self, board, n):
		""" Evaluates a certain board position based on a series of heuristics"""
		score = 0
		score += len(board.findLines(n,1))
		score += len(board.findLines(n,2))
		score -= len(board.findLines(board.otherNumber(n),1))
		score -= len(board.findLines(board.otherNumber(n),2))

		return score

	def findDefensiveMoves(self, board, n, otherForces, d):
		""" Finds moves that block all forces in otherForces"""

		startingChecks = self.findCasualChecks(board, n)
		testBoard = Board()
		for i in range(len(otherForces)):
			d.displayProgress(self.step, (100*i)/len(otherForces))

			force = otherForces[i]
			testBoard.copyAll(board)
			for j in range(len(force)):
				if j%2 == 0:
					testBoard.move(board.otherNumber(n), force[j])
				else:
					testBoard.move(n, force[j])

			defensiveChecks = self.findCasualChecks(testBoard, n)
			otherForces[i] += [check for check in defensiveChecks if check not in startingChecks]


		defensiveMoves = [p for p in board.openPoints() if self.isDefensive(p, otherForces)]

		return defensiveMoves

	def isDefensive(self, p, totalDefensiveMoves):
		""" returns whether p is a defensive move for all possible opponent's forces"""
		for defensiveMoves in totalDefensiveMoves:
			if p not in defensiveMoves:
				return False
		return True

	def colors(self):
		""" returns the colors of green """
		return [(136, 204, 136),(17, 102, 17)]
