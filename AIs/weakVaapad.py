from Board import *
from Display import *
import pygame
import random

class weakVaapad:
	"""
	The AI class for tic tac toe.  Decides where the AI will go when fed with a board.
	"""

	# general class functions
	def __init__(self):
		""" Stores board and player info for easy access """
		self.b = Board() # Board object, not array
		self.n = 0
		self.o = 0
		self.moves = list(self.b.openPoints())
		self.nMoves = len(self.b.myPoints(self.n))
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

		move = self.weakLookAhead()

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
		if move0:
			self.assured = True
			self.decided = True
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

		self.otherLookAhead()

		if self.decided:
			print "Not sure what happened here, please let Chris know"
			print "If you could record the moves from the replay that'd be really great"
			print "here they are: ", self.b.moveList

		# return self.strongLookAhead()
	
		return False

	# specialized checking functions
	def fourInARow(self,n):
		""" check if there's anywhere self could go to get four in a row """

		winningMoves = []
		lines = self.b.findLines(n,3)

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

	def findShatterpoint(self, limit = 32, display = 1, depth = 0):
		"""
		Forces the other player until there are no forces left, or someone wins
		Returns the point used successfully if player n wins,
		and self.undecided if the other player wins or nothing happens
		"""

		oldBoard = Board()
		oldBoard.copyAll(self.b)
		combos, openCombos = self.fastForce()

		ply = 1

		while (not combos) and openCombos and ply <= limit:
			total = len(openCombos)
			oldPercent = -1

			nextOC = []
			ocSet = set()

			if type(display) == list and ply > 3:
				self.displayForce(0,ply,display, depth)

			for i in range(total):

				percent = 100.0*i/total
				if type(display) == int:
					if percent >= oldPercent + 3 and self.nMoves > 2:
						self.displayForce(percent,ply,display, depth)
						oldPercent = percent

				tryForce, ocSet = self.shouldForce(openCombos,i,ocSet)
				if tryForce:

					for pair in openCombos[i]:
						self.b.move(self.n,pair[0])
						self.b.move(self.o,pair[1])

					newC, newOC = self.fastForce()

					for c in range(len(newOC)):
						nextOC += [openCombos[i] + newOC[c]]
					for c in range(len(newC)):
						combos += [openCombos[i] + newC[c]]
						if display != 1:
							self.b = Board()
							self.b.copyAll(oldBoard)
							self.forcingCombo = openCombos[i]+newC[c]
							return ply

					self.b = Board()
					self.b.copyAll(oldBoard)

			openCombos = nextOC
			ply += 1

		if display != 1 and combos:
			self.forcingCombo = combos[0]
			return ply

		if combos:
			combo = self.chooseMove(combos)
			self.forcingCombo = combo
			return combo[0][0]

		if display != 1 and openCombos and ply > limit:
			return False
		if display != 1 and not openCombos:
			return ply
		return False

	def shouldForce(self,openCombos,i, ocSet):
		""" tests whether you should try the given forcing combination """

		newSet = set()
		for pair in openCombos[i]:
			newSet.add(self.pairHash(pair))

		if newSet in ocSet:
			return False, ocSet

		else:
			ocSet.add(frozenset(newSet))
			return True, ocSet

	def pairHash(self,pair):
		""" returns a hash of each pair """
		v = [0,0]
		for i in [0,1]:
			p = pair[i]
			v[i] = p[0]+p[1]*4+p[2]*16
		return v[0]+v[1]*64

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

	def displayForce(self,percent,ply,display, depth):
		""" displays progress text for forcing """
		text = ""
		if depth:
			text += "(" + str(depth) + "-deep) "

		if type(display) == list:
			text += display[0] + str(ply) + "-ply): "
			percent = 100.0*display[1]/display[2]
			self.d.displayProgress(text, percent)

		elif display:
			if self.assured:
				text +=  "Successful "+str(ply)+"-ply Search: "
			elif display == 1:
				text += "Offensive "+str(ply)+"-ply Search: "
			elif display == 2:
				text += "Defensive "+str(ply)+"-ply Search: "
			
			self.d.displayProgress(text, percent)

	# brute force checking functions
	def strongLookAhead(self):
		"""
		Looks ahead for undefeatable moves
		"""

		moves = []
		totalM = len(self.moves)

		for i in range(totalM):
			text = "Strong Look-Ahead: "
			if moves:
				text = "Successful Look-Ahead"
			self.d.displayProgress(text, 100.0*i/totalM)

			badGuy = weakVaapad()
			badGuy.updateAll(self.b,self.o,self.d)
			badGuy.b.move(badGuy.o,self.moves[i])
			# if they don't have any way to block the force, you're great
			if not badGuy.otherLookAhead(False, 1):
				moves += [self.moves[i]]

		if moves:
			self.assured = True
			self.decided = True

		return self.chooseMove(moves)

	def weakLookAhead(self):
		""" looks ahead, tries to set up a decent force """

		forceMoves = []
		pairs = self.b.findForces(self.n)
		for pair in pairs:
			for m in pair:
				forceMoves += [pair]

		futureForce = False
		bestScore = self.magicNumber()
		orig = bestScore
		bestMoves = []

		nMoves = len(self.moves)

		for i in range(nMoves):
			self.d.displayProgress("Finding Optimal Move: ",100.0*i/nMoves)

			goodGuy = weakVaapad()
			goodGuy.updateAll(self.b,self.n,self.d)
			goodGuy.b.move(self.n,self.moves[i])

			score = goodGuy.magicNumber()

			if self.moves[i] not in forceMoves:
				finished = goodGuy.findShatterpoint(6, ["Finding Optimal Move (",i,nMoves])

				if (goodGuy.assured or not finished) and not futureForce:
					futureForce = True
					bestScore = score
					bestMoves = []

			if bestScore < score:
				bestScore = score
				bestMoves = [self.moves[i]]
			elif bestScore == score:
				bestMoves += [self.moves[i]]

		return self.chooseMove(bestMoves)

	def magicNumber(self):
		"""
		where the magic numbers come in
		"""

		score = 0
		linesSet = [[self.b.findLines(self.o,i) for i in range(1,5)]]
		linesSet += [[self.b.findLines(self.n,i) for i in range(1,5)]]
		for i in range(2):
			for num in range(4):
				score += (num/.9+1)*len(linesSet[i][num])*(2*i-0.7)

		return score

	def otherLookAhead(self,fullSearch = True,depth=0):
		""" looks ahead defensively to try to block opponent's forces """

		if depth == 3:
			return False

		badGuy = weakVaapad()
		badGuy.updateAll(self.b,self.o,self.d)
		possMoves = []
		workingMoves = []

		test = badGuy.findShatterpoint(32, 2, depth)

		if badGuy.assured:
			for pair in badGuy.forcingCombo:
				for move in pair:
					if move not in possMoves:
						possMoves += [move]

				badGuy.b.move(badGuy.n,pair[0])
				badGuy.b.move(badGuy.o,pair[1])

			newPairs = badGuy.b.findForces(badGuy.o)

			for pair in newPairs:
				for move in pair:
					if move not in possMoves:
						possMoves += [move]

			badGuy.b = Board()
			badGuy.b.copyAll(self.b)

			lenPM = len(possMoves)

			for i in range(lenPM):
				badGuy.assured = False
				badGuy.b.move(badGuy.o,possMoves[i])
				check = badGuy.fourInARow(badGuy.o)
				text = ""
				if depth:
					text += "(" + str(depth) + "-deep) "
				text += "Checking Blocks: "
				self.d.displayProgress(text,100.0*i/lenPM)

				if check:
					badGuy.b.move(badGuy.n,check)

					goodGuy = weakVaapad()
					goodGuy.updateAll(badGuy.b,badGuy.o,badGuy.d)

					if goodGuy.otherLookAhead(False, depth+1):
						workingMoves += [possMoves[i]]

					badGuy.b.clearPoint(check)
					badGuy.b.clearPoint(possMoves[i])

				else:
					finished = badGuy.findShatterpoint(6, ["Checking Blocks (",i,lenPM], depth)

					badGuy.b.clearPoint(possMoves[i])

					if (not badGuy.assured) and finished:
						if not fullSearch:
							return True
						workingMoves += [possMoves[i]]

			if workingMoves:
				self.moves = workingMoves

			else:
				self.moves = possMoves
				if not fullSearch:
					return False

		elif not fullSearch:
			return True

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
		self.moves = list(self.b.openPoints())
		self.nMoves = len(self.b.myPoints(self.n))
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



