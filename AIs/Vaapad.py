from Board import *
from Brute import *
import random

class Vaapad:
	"""
	The AI class for tic tac toe.  Decides where the AI will go when fed with a board.
	"""

	# general class functions
	def __init__(self):
		""" Stores board and player info for easy access """
		self.b = Board() # Board object, not array
		self.n = 0
		self.o = 0
		self.moves = self.b.openPoints()
		self.decided = False
		self.assured = False
		self.d = None

		self.undecided = False
		self.forcingCombo = []
		self.comboLen = False
		self.ply = 4

	def chooseMove(self,moves):
		"""
		chooses a move from the available one in the determined tiebreaking way
		Currently: Random
		"""

		if (len(moves) > 0):
			return random.choice(moves)
		return self.undecided

	def colors(self):
		""" returns the colors of vaapad """
		return [(150,0,230),(80, 0, 130)]

	# high level move functions
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

		other.otherBadLookAhead()
		if other.assured: # checks for their strong lookahead
			self.moves = other.guardLookAhead()
			move = self.badLookAhead()

		if not move:
			lilHelper = Brute()
			return lilHelper.move(self.b,self.n,self.d)

		return move

	def assuredMove(self):
		self.decided, self.assured = (False,)*2

		if self.forcingCombo:
			if self.forcingCombo[0][0] not in self.b.myPoints(self.n):
				self.forcingCombo = []
				self.comboLen = 0
			elif self.forcingCombo[0][1] in self.b.myPoints(self.o):
				# if they're moving in line with the combo, keep it up
				self.assured = True
				self.decided = True
				self.forcingCombo = self.forcingCombo[1:]
				percent = 100.0*(self.comboLen-len(self.forcingCombo)+1)/self.comboLen
				self.d.displayProgress("Forced Shatterpoint: ", percent)
				pygame.time.wait(400)
				return self.forcingCombo[0][0]

		# check for four in a row on both sides
		move0 = self.fourInARow(self.n)
		if self.assured:
			return move0

		move1 = self.fourInARow(self.o)
		if move1:
			self.decided = True
			return move1

		move3 = self.findShatterpoint()
		if self.assured:
			self.comboLen = len(self.forcingCombo)
			self.d.displayProgress("Forced Shatterpoint: ", 100.0/self.comboLen)
			pygame.time.wait(400)
			return move3

		move4 = self.badLookAhead()
		
		return move4

	# specialized checking functions
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

	def findShatterpoint(self):
		"""
		Forces the other player until there are no forces left, or someone wins
		Returns the point used successfully if player n wins,
		and self.undecided if the other player wins or nothing happens
		"""

		ply = 0
		oldBoard = Board()
		oldBoard.copyAll(self.b)
		combos, openCombos = self.fastForce()
		self.displayForce(100,ply,True)

		while openCombos:
			total = len(openCombos)
			oldPercent = 0
			ply += 1

			nextOC = []

			for i in range(total):

				percent = 100.0*i/total
				if percent >= oldPercent + 3:
					self.displayForce(percent,ply,True)
					oldPercent = percent

				for pair in openCombos[i]:
					self.b.move(self.n,pair[0])
					self.b.move(self.o,pair[1])

				newC, newOC = self.fastForce()

				for c in range(len(newOC)):
					nextOC += [openCombos[i] + newOC[c]]
				for c in range(len(newC)):
					combos += [openCombos[i] + newC[c]]

				self.b = Board()
				self.b.copyAll(oldBoard)

			if combos:
				combo = self.chooseMove(combos)
				self.forcingCombo = combo
				return combo[0][0]

			openCombos = nextOC

		return False

	def fastForce(self):
		""" forces to finish REL quick """

		pairs = self.b.findForces(self.n)
		lenPairs = len(pairs)
		allowedP = self.forceCheck(pairs,lenPairs)

		combos = []
		openCombos = []

		for pairN in allowedP[0]:
			for i in allowedP[1]:

				self.b.move(self.n,pairs[pairN][i])
				self.b.move(self.o,pairs[pairN][1-i])

				itWorks = self.updateWinsForPoint(pairs[pairN],i)
				if itWorks:
					combos += [[[pairs[pairN][i],pairs[pairN][1-i]]]]
				else:
					openCombos += [[[pairs[pairN][i],pairs[pairN][1-i]]]]

				self.b.clearPoint(pairs[pairN][i])
				self.b.clearPoint(pairs[pairN][1-i])

		return combos, openCombos

	def forceCheck(self,pairs,lenPairs):
		""" sees if it can pull anti-force combo """

		otherChecks = self.b.findLines(self.o,3)

		allowedPairs = []
		allowedIndex = []

		if len(otherChecks) and lenPairs:
			checkLine = self.b.lineToPoints(next(iter(otherChecks)))
			for p in checkLine:
				if self.b.pointToValue(p) == 0:
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
					pairN += 1
				i = 1-i
				if pairN == lenPairs:
					allAllowed = False # fucking give the fuck up
		else:
			allowedPairs = range(lenPairs)
			allowedIndex = range(2)

		return [allowedPairs,allowedIndex]

	def displayForce(self,percent,ply,offense):
		""" displays progress text for forcing """

		text = "Offensive "+str(ply)+"-ply Search: "
		if not offense:
			text = "Defensive "+str(ply)+"-ply Search: "
		if self.assured:
			text =  "Successful "+str(ply)+"-ply Search: "
		self.d.displayProgress(text, percent)

	# brute force checking functions
	def lookAhead(self):
		"""
		Brunt of AI, looks ahead, keeps track of if win is strong/weak
		"""

		strong = True
		strongMoves = []
		movesSet = set()

		for move in self.moves:
			goodGuy = Vaapad()
			goodGuy.updateAll(self.b,self.n,self.d)
			goodGuy.b.move(move)

			if goodGuy.fourInARow(goodGuy.n):
				moves += [move]
			elif goodGuy.checkCheckmates():
				moves += [move]
			else:
				badGuy = Vaapad()
				badGuy.updateAll(goodGuy.b,goodGuy.o,goodGuy.d)

				badGuy.assuredMove()

	def magicNumber(self):
		"""
		where the magic numbers come in
		"""

		score = 0
		linesSet = [[self.b.findLines(self.o,i) for i in range(1,5)]]
		linesSet += [[self.b.findLines(self.n,i) for i in range(1,5)]]
		for i in range(2):
			for num in range(4):
				score += (num+1)*len(linesSet[i][num])*(2*i-0.7)

		return score

	def badLookAhead(self):
		"""
		Tries moving for player n at point p then rechecks board
		Returns the point used successfully if player n wins,
		and p = [-1,-1,-1] if the other player wins or nothing happens
		"""

		bestScore = self.magicNumber()
		bestMove = []
		mNum = 0

		for move in self.moves:
			mNum += 1
			percent = 100.0*mNum/len(self.moves)
			self.d.displayProgress("Bad Look-Ahead: ", percent)
			goodGuy = Vaapad()
			goodGuy.updateAll(self.b,self.n,self.d)
			goodGuy.b.move(goodGuy.n,move)

			score = goodGuy.magicNumber()
			if score > bestScore:
				bestMove = [move]
				bestScore = score
			elif score == bestScore:
				bestMove += [move]

		return self.chooseMove(bestMove)

	def otherBadLookAhead(self):
		""" just tries to make sure other cant force to finish """

		ply = 0
		oldBoard = Board()
		oldBoard.copyAll(self.b)
		combos, openCombos = self.fastForce()
		self.displayForce(100,ply,True)

		while openCombos:
			total = len(openCombos)
			oldPercent = 0
			ply += 1

			nextOC = []

			for i in range(total):

				percent = 100.0*i/total
				if percent >= oldPercent + 3:
					self.displayForce(percent,ply,False)
					oldPercent = percent

				for pair in openCombos[i]:
					self.b.move(self.n,pair[0])
					self.b.move(self.o,pair[1])

				newC, newOC = self.fastForce()

				for c in range(len(newOC)):
					nextOC += [openCombos[i] + newOC[c]]
				for c in range(len(newC)):
					combos += [openCombos[i] + newC[c]]

				self.b = Board()
				self.b.copyAll(oldBoard)

			if combos:
				self.forcingCombo = combos
				break

			openCombos = nextOC

		return False

	def guardLookAhead(self):
		""" works to defend strong opponent moves by limiting to blocks """
		pairs = []
		powerMoves = []

		for combo in self.forcingCombo:
			for pair in combo:
				if pair not in pairs:
					pairs += [pair]
				else:
					for i in range(2):
						if pair[i] not in powerMoves:
							powerMoves += [pair[i]]

		if powerMoves:
			return powerMoves
		else:
			return self.moves

	# updating functions
	def updateForPoint(self, p):
		"""
		Updates pairs, moves, and lines after point p has been filled
		More efficient than updating fully each time
		"""

	def updateAll(self, board, n, display):
		"""
		Updates all pairs, moves and lines for the current board
		"""
		self.b.copyAll(board) # Board object, not array
		self.n = n
		self.d = display
		self.o = self.b.otherNumber(self.n)
		self.moves = self.b.openPoints()
		self.decided = False
		self.assured = False

	def updateWinsForPoint(self, pair, myNum):
		"""
		Checks whether a just-filled point caused any wins
		"""
		otherNum = 0 if myNum == 1 else 1

		wins = self.b.openLinesForPoint(self.n,pair[myNum],4)
		if wins:
			self.assured = True
			self.decided = True
			return True

		checks = self.b.openLinesForPoint(self.n,pair[myNum],3)
		other = self.b.openLinesForPoint(self.o,pair[otherNum],4)
		if  checks and not other:
			self.assured = True
			self.decided = True
			return True

		return False

	def checkWins(self, p):
		"""
		Returns True if p causes a win, False if the game is still being played
		"""



