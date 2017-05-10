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
		self.moves = self.b.openPoints()
		self.decided = False
		self.assured = False
		self.d = None

		self.undecided = False
		self.forcingCombo = []
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

		other.otherBadLookAhead()
		if other.assured: # checks for their strong lookahead
			self.moves = other.guardLookAhead()
			move = self.badLookAhead()

		if not move:
			lilHelper = Brute()
			return lilHelper.move(self.b,self.n,self.d)

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
		self.decided, self.assured = (False,)*2

		if self.forcingCombo != []:
			if self.forcingCombo[0][1] in self.b.myPoints(self.o):
				# if they're moving in line with the combo, keep it up
				self.assured = True
				self.decided = True
				self.forcingCombo = self.forcingCombo[1:]
				return self.forcingCombo[0][0]

		# check for four in a row on both sides
		move0 = self.fourInARow(self.n)
		if self.assured:
			return move0

		move1 = self.fourInARow(self.o)
		if move1:
			self.decided = True
			return move1

		move3 = self.forceToFinish()
		if self.assured:
			self.d.displayProgress("Forced Shatterpoint: ",int(100.0/len(self.forcingCombo)))
			return move3

		move4 = self.badLookAhead()
		
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
			winningMoves, combos, keepSearching = self.forceToFinishR(pairs, ply, 1)
			if winningMoves:
				self.assured = True
				self.decided = True

				combo = self.chooseMove(combos)
				self.forcingCombo = combo
				for i in range(len(combos)):
					if combo == combos[i]:
						return combo[0][0]
			if not keepSearching:
				break

		return False

	def forceToFinishR(self, pairs, ply, original):
		""" solves force to finish recursively """

		lenPairs = len(pairs)
		moves = []
		combos = []
		otherChecks = self.b.findLines(self.o,3)
		keepSearching = False

		allowedPairs = range(lenPairs)
		allowedIndex = range(2)

		if len(otherChecks) > 0:
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
					i = 0
					pairN += 1
				if i == 0:
					i = 1
				if pairN == lenPairs:
					return moves # fucking give the fuck up

		for pairN in allowedPairs:
			if original:
				text = "Offensive "+str(ply)+"-ply Search: "
				percent = int(100.0*pairN/len(allowedPairs))
				if original == 2:
					text = "Defensive "+str(ply)+"-ply Search: "
				if moves:
					text =  "Successful "+str(ply)+"-ply Search: "
				self.d.displayProgress(text, percent)
			for i in allowedIndex:
				newAI = Vaapad()
				newAI.updateAll(self.b,self.n,self.d)
				newAI.updateForForce(pairs[pairN],i)
				if newAI.assured:
					moves += [pairs[pairN][i]]
					combos += [[[pairs[pairN][i],pairs[pairN][1-i]]]]
				elif ply > 0:
					otherChecks = newAI.b.findLines(newAI.o,3)
					newPairs = newAI.b.findForces(newAI.n)
					if len(otherChecks) == 0:
						futureM, futureC, futureKS = newAI.forceToFinishR(newPairs, ply-1, 0)
						if futureKS:
							keepSearching = True
						if futureM != []:
							for m in range(len(futureM)):
								combos += [[[pairs[pairN][i],pairs[pairN][1-i]]] + futureC[m]]
								moves += [pairs[pairN][i]]
					else:
						checkLine = newAI.b.lineToPoints(next(iter(otherChecks)))
						for p in checkLine:
							if newAI.b.pointToValue(p) == 0:
								checkP = p
						for pair in newPairs:
							for i in [0,1]:
								if pair[i] == checkP:
									newAI.updateForForce(pair,i)

				elif ply == 0:
					keepSearching = True

		return moves, combos, keepSearching

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

	def focusOnTheNow(self):
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

		bestScore = self.focusOnTheNow()
		bestMove = []
		mNum = 0

		for move in self.moves:
			mNum += 1
			percent = int(100.0*mNum/len(self.moves))
			self.d.displayProgress("Bad Look-Ahead: ", percent)
			goodGuy = Vaapad()
			goodGuy.updateAll(self.b,self.n,self.d)
			goodGuy.b.move(goodGuy.n,move)

			score = goodGuy.focusOnTheNow()
			if score > bestScore:
				bestMove = [move]
				bestScore = score
			elif score == bestScore:
				bestMove += [move]

		return self.chooseMove(bestMove)

	def otherBadLookAhead(self):
		""" just tries to make sure other cant force to finish """

		pairs = self.b.findForces(self.n)
		for ply in range(32):
			winningMoves, combos, keepSearching = self.forceToFinishR(pairs, ply, 2)
			self.forcingCombo = combos
			if winningMoves:
				self.assured = True
				self.decided = True
				break
			if not keepSearching:
				break

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



