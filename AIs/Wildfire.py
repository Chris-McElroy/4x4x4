import time
import random
from Board import *

class Wildfire:
	""" functions as the player for a real life person """

	def __init__(self):
		""" Stores player info for easy access """
		self.MAX_FORCES = 9
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

		self.step  = "Finding offensive Forces: "
		# if we have a winning sequence of forces, take it
		winningForces = self.forceCheck(board, n, self.MAX_FORCES, d)
		if winningForces:
			print "Found", len(winningForces), "winning forces"
			return winningForces[0][0]


		self.step  = "Finding defensive Moves: "
		# if we will have a losing sequence of forces, we need to take action against it.
		otherForces = self.forceCheck(board, board.otherNumber(n), self.MAX_FORCES, d)
		# currently just do shittiest possible block

		possibleMoves = board.openPoints()

		if otherForces:
			print "Defending against", len(otherForces), "forces"

			# # testBoard = Board()
			# totalDefensiveMoves = []
			# for force in otherForces:
			# 	defensiveMoves = []
			# 	# testBoard.copyAll(board)
			# 	for i in range(len(force)):
			# 		if i%2 == 0:
			# 			# testBoard.move(board.otherNumber(n), force[i])
			# 			defensiveMoves.append(force[i])
			# 		# else:
			# 		# 	testBoard.move(n, force[i])
			# 	totalDefensiveMoves.append(defensiveMoves)

			defensiveMoves = [p for p in possibleMoves if self.isDefensive(p, otherForces)]

			if defensiveMoves:
				possibleMoves = bestDefensiveMoves
			else:
				print "Failed to find possible defensive move. #rip"


		self.step = "Main Loop: "
		bestScore = -999
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


	def winningMove(self, board, n):
		""" Checks if there is a winning move for player n and if there is, returns it"""
		forces = board.findLines(n, 3).copy()
		if len(forces) > 0:
			for point in board.lineToPoints(next(iter(forces))):
				if board.pointToValue(point) == 0:
					return point
	
	def forceCheck(self, board, n, movesLeft, d):
		""" Wrapper function for forcecheckrec"""
		self.forceCache.clear()
		return self.forceCheckRec(board, n, movesLeft, d)

	def forceCheckRec(self, board, n, movesLeft, d):
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

		i = 0
		for force in possibleForces:

			if movesLeft == self.MAX_FORCES:
				d.displayProgress(self.step, (100*i)/(len(possibleForces)))
				i+= 1

			openSpots = filter(lambda p: board.pointToValue(p) == 0, board.lineToPoints(force))

			board.move(n, openSpots[0])
			board.move(board.otherNumber(n), openSpots[1])

			wins1 = self.forceCheckRec(board, n, movesLeft-1, d)
			board.clearPoint(openSpots[0])
			board.clearPoint(openSpots[1])

			# we don't have getters or setters because this is sus
			# kids, don't do this at home

			if wins1:
				self.forceCache.add(board.hash())
				wins += [openSpots + moves for moves in wins1]
			
			board.move(n, openSpots[1])
			board.move(board.otherNumber(n), openSpots[0])

			wins2 = self.forceCheckRec(board, n, movesLeft-1, d)
			board.clearPoint(openSpots[0])
			board.clearPoint(openSpots[1])

			if wins2:
				self.forceCache.add(board.hash())
				openSpots.reverse()
				wins += [openSpots + moves for moves in wins2]

		return wins

	def evaluatePosition(self, board, n):
		""" Evaluates a certain board position based on a series of heuristics"""
		score = 0
		score += len(board.findLines(n,1))
		score += len(board.findLines(n,2))
		score -= len(board.findLines(board.otherNumber(n),1))
		score -= len(board.findLines(board.otherNumber(n),2))

		return score

	def isDefensive(self, p, totalDefensiveMoves):
		""" returns whether p is a defensive move for all possible opponent's forces"""
		for defensiveMoves in totalDefensiveMoves:
			if p not in defensiveMoves:
				return False
		return True

	def colors(self):
		""" returns the colors of green """
		return [(136, 204, 136),(17, 102, 17)]
