from Board import *
from Brute import *
import random

class Vaapad:
	"""
	The AI class for tic tac toe.  Decides where the AI will go when fed with a board.
	"""

	def __init__(self):
		""" Stores board and player info for easy access """
		self.b = Board() # Board object, not array
		self.n = 0
		self.o = 0
		#self.moves = self.b.openPoints()
		self.decided = False
		self.assured = False
		self.d = None

		self.undecided = False
		self.ply = 4

	def move(self,board,n, display):
		"""
		The main function for this class.  Returns the point the AI wants to move in.
		"""

		self.updateAll(board,n,display)

		# check for four in a row on both sides
		move = self.assuredMove()
		if self.decided:
			return move

		other = Vaapad()
		other.updateAll(self.b,self.o,self.d)

		other.lookAhead()
		#if other.assured: # checks for their strong lookahead
			#self.moves = self.guardLookAhead()

		move = self.lookAhead() # casual lookahead
		return move

	def chooseMove(self,moves):
		"""
		chooses a move from the available one in the determined tiebreaking way
		Currently: Random
		"""

		nn = 64
		if (len(moves) > nn):
			return moves[nn]
		elif (len(moves) > 0):
			return random.choice(moves)
		return self.undecided

	def assuredMove(self):

		self.decided, self.assured = (False,)*2

		# check for four in a row on both sides
		move0 = self.fourInARow(self.n)
		if self.assured:
			print "I have the win\n"
			return move0

		move1 = self.fourInARow(self.o)
		if move1:
			self.decided = True
			return move1

		move3 = self.forceToFinish()
		if self.assured:
			print "I have the force.\n"
			return move3

		move4 = self.lookAhead()
		if self.assured: # checks for a strong lookahead
			print "I have the win."
		
		return move4

	def fourInARow(self,n):
		""" check if there's anywhere self could go to get four in a row """

		winningMoves = []
		lines = self.b.findLines(n,3)

		if (len(lines) > 0):
			self.assured = True
			self.decided = True
			for l in lines:
				points = self.b.lineToPoints(l)
				for i in range(4): 
					if self.b.pointToValue(points[i]) == 0:
						move = points[i]
						winningMoves += [move] # double counts double 4-in-a-rows bc hell yeah

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
		for ply in range(32):
			winningMoves = self.recursiveForceToFinish(pairs, ply)
			if winningMoves != []:
				break

		return self.chooseMove(winningMoves) 

	def recursiveForceToFinish(self, pairs, ply):
		""" solves force to finish recursively """

		lenPairs = len(pairs)
		moves = []
		otherChecks = self.b.findLines(self.o,3)

		allowedPairs = range(lenPairs)
		allowedIndex = range(2)

		if len(otherChecks) > 0:
			checkLine = self.b.lineToPoints(otherChecks[0])
			for p in checkLine:
				if newAI.b.pointToValue(p) == 0:
					checkP = p
			allAllowed = True
			pairN = 0
			i = 0
			while allAllowed:
				if pairs[pairN][i] == checkP:
					allowedPairs = [pairN]
					allowedIndex = [i]
					allAllowed = False
				if i == 1:
					i = 0
					pairN += 1
				if i == 0:
					i = 1
				if pairN == lenPairs:
					return moves # fucking give the fuck up

		for pairN in allowedPairs:
			for i in allowedIndex:
				newAI = Vaapad()
				mewAI.updateAll(self.b,self.n,self.d)
				newAI.updateForForce(pairs[pairN],i)
				if newAI.assured:
					moves += [pairs[pairN][i]]
				elif ply > 0:
					otherChecks = newAI.b.findLines(newAI.o,3)
					newPairs = newAI.b.findForces(newAI.n)
					if otherChecks == []:
						futureMoves = newAI.recursiveForceToFinish(newPairs, ply-1)
						if futureMoves != []:
							moves += [pairs[pairN][i]]
					else:
						checkLine = newAI.b.lineToPoints(otherChecks[0])
						for p in checkLine:
							if newAI.b.pointToValue(p) == 0:
								checkP = p
						for pair in newPairs:
							for i in [0,1]:
								if pair[i] == checkP:
									newAI.updateForForce(pair,i)

				# elif ply == 0:
				# 	print "got to 0"

		if moves != []:
			self.assured = True
			self.decided = True
		return moves

	def lookAhead(self):
		"""
		Tries moving for player n at point p then rechecks board
		Returns the point used successfully if player n wins,
		and p = [-1,-1,-1] if the other player wins or nothing happens
		"""

		numMoves = self.b.numMoves(self.n)[0]
		# simple four in a row
		#moves = [[0,0,0],[1,0,0],[2,0,0],[3,3,3]]

		# simple checkmate
		#moves = [[0,0,0],[1,0,0],[0,0,3],[2,0,1]]

		# 1 force checkmate
		#moves = [[0,0,0],[1,0,0],[1,0,1],[2,0,1],[3,3,3]]

		# 3 move force
		# moves = [[0,0,0],[0,0,3],[3,0,0],[2,0,0],[0,0,1],[3,3,3]]

		# god opening
		moves = [(1,1,1),(0,3,0),(1,2,2),(2,2,2),(3,2,3)]
		openPoints = self.b.openPoints()
		if self.n == 2:
			print numMoves
			print openPoints
		if numMoves < len(moves):
			if moves[numMoves] in openPoints:
				return moves[numMoves]

		lilHelper = Brute()
		return lilHelper.move(self.b,self.n,self.d)


		currentPly = self.ply
		#currentMoves = self.moves

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

		self.updateWinsForPoint(pair,myNum)

	def updateAll(self, board, n, display):
		"""
		Updates all pairs, moves and lines for the current board
		"""
		self.b.copyBoard(board) # Board object, not array
		self.n = n
		self.d = display
		self.o = self.b.otherNumber(self.n)
		#self.moves = self.b.openPoints()
		self.decided = False
		self.assured = False

	def updateWinsForPoint(self, pair, myNum):
		"""
		Checks whether a just-filled point caused any wins
		"""
		otherNum = 0 if myNum == 1 else 1

		wins = self.b.openLinesForPoint(self.n,pair[myNum],4)
		if len(wins) > 0:
			self.assured = True
			self.decided = True

		checks = self.b.openLinesForPoint(self.n,pair[myNum],3)
		other = self.b.openLinesForPoint(self.o,pair[otherNum],4)
		if  len(checks) > 0 and len(other) == 0:

			# print "i think ill have checkmate"
			# print checks
			# print moveChain
			# print pair[myNum]
			# print "here's the board:"
			# for i in [3,2,1,0]:
			# 	lineString = ""
			# 	for j in range(4):
			# 		l = j + 4*i
			# 		values = self.b.lineToValues(l)
			# 		for v in values:
			# 			lineString += self.valueToMark(v) + " "
			# 		lineString += "  "
			# 	print lineString
			self.assured = True
			self.decided = True

	def checkWins(self, p):
		"""
		Returns True if p causes a win, False if the game is still being played
		"""

	def valueToMark(self,v):
		""" converts value to a mark """
		mark = ""

		if (v == 0):
			mark = "-"

		elif (v == 1):
			mark = "X"

		elif (v == 2):
			mark = "O"

		return mark

	def colors(self):
		""" returns the colors of vaapad """
		return [(150,0,230),(80, 0, 130)]



