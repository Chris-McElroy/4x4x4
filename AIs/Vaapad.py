from Board import *
from Display import *
import pygame
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
		self.moves = list(self.b.openPoints())
		self.nMoves = len(self.b.myPoints(self.n))
		self.decided = False
		self.assured = False
		self.scared = False
		self.d = None

		self.undecided = False
		self.forcingCombo = []
		self.comboLen = False
		self.ply = 4

		self.lastPrintTime = -1000

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

	def updateText(self,percent, depth, ply, textN, numMoves):
		""" updates the display text based on the inputs """

		currentTime = pygame.time.get_ticks()
		if currentTime - self.lastPrintTime > 100:
			possText = ["Shatterpoint", "Possible Move", "Unbeatable Move", "Optimal Move"]

			text = "(" + str(depth) + "-deep, " + str(ply) + "-ply) "
			text += "Finding " if numMoves == 0 else "Found " + str(numMoves) + " "
			text += possText[textN]
			text += ": " if numMoves <= 1 else "s: "

			self.d.displayProgress(text, percent)
			self.lastPrintTime = currentTime

	# high level move functions
	def move(self,board,n, newDisplay):
		"""
		The main function for this class.  Returns the point the AI wants to move in.
		"""

		self.updateAll(board,n,newDisplay,-1000)

		# check for four in a row on both sides
		move = self.assuredMove()
		if self.decided:
			if move == False:
				print "Chris has been trying to recreate this bug for a while,"
				print "Please get all this info to him if possible."
				print "Moves: ", self.b.moveList
				print "Players: ", self.n, self.o
				print "Move, assured, decided, scared: ", move, self.assured, self.decided, self.scared
				print "Board:"
				newD = Display(self.b,[None],[None])
				newD.displayShittyBoard()
				print "Possible moves: ", self.moves

			return move

		move = self.weakLookAhead()

		return move

	def assuredMove(self):
		""" attempts to make all the right moves in all the right places """

		# see if its in the middle of a force
		move = self.keepForcing()
		if self.assured:
			return move

		# check for four in a row on both sides
		move = self.fourInARow(self.n)
		if move:
			self.assured = True
			self.decided = True
			return move

		move = self.fourInARow(self.o)
		if move:
			self.decided = True
			return move

		# search for a new force
		move = self.findShatterpoint([0,0,0,0])
		if self.assured:
			self.comboLen = len(self.forcingCombo)
			self.d.displayProgress("Forced Shatterpoint: ", 100.0/self.comboLen)
			pygame.time.wait(400)
			return move

		# check what to defend
		self.otherLookAhead([0,0,1,0])

		# search for a strong move
		if not self.scared:
			strongMove = self.strongLookAhead()
			if self.assured:
				return strongMove

		return False

	# specialized checking functions
	def keepForcing(self):
		""" keeps a force going if it was happening """
		if self.forcingCombo:
			if self.forcingCombo[0][0] not in self.b.myPoints(self.n):
				self.forcingCombo = []
				self.comboLen = 0
				return False
			elif self.forcingCombo[0][1] in self.b.myPoints(self.o):
				# if they're moving in line with the combo, keep it up
				self.assured = True
				self.decided = True
				self.forcingCombo = self.forcingCombo[1:]
				percent = 100.0*(self.comboLen-len(self.forcingCombo)+1)/self.comboLen
				self.d.displayProgress("Forced Shatterpoint: ", percent)
				pygame.time.wait(400)
				return self.forcingCombo[0][0]
		return False

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

	def findShatterpoint(self, display, limit = 32):
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
			oldPercent = -100

			nextOC = []
			ocSet = set()

			for i in range(total):
				if not display[2]:
					display[0] = 100*i/total
					display[3] = len(combos)
				self.updateText(display[0],display[1],ply,display[2],display[3])

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
						if display[2]:
							self.b = Board()
							self.b.copyAll(oldBoard)
							self.forcingCombo = openCombos[i]+newC[c]
							return ply

					self.b = Board()
					self.b.copyAll(oldBoard)

			openCombos = nextOC
			ply += 1

		if display[2] and combos:
			return ply

		if combos:
			combo = self.chooseMove(combos)
			self.forcingCombo = combo
			return combo[0][0]

		if display[2] and openCombos and ply > limit:
			return False
		if display[2] and not openCombos:
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
		allowedP, allowedI = self.forceCheck(pairs,lenPairs)

		combos = []
		openCombos = []
		moveList = []

		for pairN in allowedP:
			for i in allowedI:

				move = pairs[pairN][i]
				otherMove = pairs[pairN][1-i]

				if move in moveList:
					self.assured = True
					self.decided = True
					combos += [[[move,otherMove]]]

				else:
					openCombos += [[[move, otherMove]]]

				moveList += [move]

		return combos, openCombos

	def forceCheck(self,pairs,lenPairs):
		""" sees if it can pull anti-force combo """

		otherChecks = self.b.findLines(self.o,3)

		allowedPairs = []
		allowedIndex = []

		if otherChecks and lenPairs:
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

		return allowedPairs, allowedIndex

	def findCombos(self, display, limit = 32):
		"""
		finds shatterpoint but returns all the forces in the top used ply,
		if there is one
		"""

		oldBoard = Board()
		oldBoard.copyAll(self.b)
		combos, openCombos, forceList = self.fastCombos()

		ply = 1

		while (not combos) and openCombos and ply <= limit:
			total = len(openCombos)
			nextOC = []
			ocSet = set()

			for i in range(total):
				self.updateText(display[0],display[1],ply,display[2],display[3])

				tryForce, ocSet = self.shouldForce(openCombos,i,ocSet)
				if tryForce:

					for pair in openCombos[i]:
						self.b.move(self.n,pair[0])
						self.b.move(self.o,pair[1])

					newC, newOC, newFL = self.fastCombos()

					for c in range(len(newOC)):
						nextOC += [openCombos[i] + newOC[c]]
					for c in range(len(newC)):
						combos += [openCombos[i] + newC[c]]
					for forces in newFL:
						forceList += [forces]

					self.b = Board()
					self.b.copyAll(oldBoard)

			openCombos = nextOC
			ply += 1

		return combos, forceList

	def fastCombos(self):
		""" fastForce but finds force sets """

		pairs = self.b.findForces(self.n)
		lenPairs = len(pairs)
		allowedP, allowedI = self.forceCheck(pairs,lenPairs)

		combos = []
		openCombos = []
		forceList = []
		moveList = []

		for pairN in allowedP:
			for i in allowedI:
				move = pairs[pairN][i]
				otherMove = pairs[pairN][1-i]

				if move in moveList:
					otherMove2 = False
					for pairN2 in range(pairN):
						for i in allowedI:
							if move == pairs[pairN2][i]:
								otherMove2 = pairs[pairN2][1-i]
					self.assured = True
					self.decided = True
					combos += [[[move,otherMove,otherMove2]]]
					forceList += [self.b.findForces(self.o)]

				else:
					openCombos += [[[move, otherMove]]]

				moveList += [move]

		return combos, openCombos, forceList

	# brute force checking functions
	def strongLookAhead(self):
		"""
		Looks ahead for undefeatable moves
		"""
		moves = []
		numMoves = 0
		possMoves = []

		forceMoves = []
		pairs = self.b.findForces(self.n)
		for pair in pairs:
			for m in pair:
				forceMoves += [m]

		badGuy = Vaapad()
		badGuy.updateAll(self.b,self.o,self.d,self.lastPrintTime)

		for move in self.moves:
			shouldMove = self.shouldStrong(move,forceMoves)

			if shouldMove:
				possMoves += [move]

		i = 0
		totalM = len(possMoves)

		for move in possMoves:
			percent = 100.0*i/totalM
			self.updateText(percent,0,0,2,numMoves)

			badGuy.b.move(badGuy.o,move)
			# if they don't have any way to block the force, you're great
			if not badGuy.otherLookAhead([percent,1,2,numMoves,i,totalM]):
				moves += [move]
				numMoves += 1

			badGuy.b.clearPoint(move)

			# if (move in moves):
			# 	if not shouldMove:
			# 		print "FUCKED UP LOOKIE HERE ", move
			# 	else:
			# 		print "awesome!!!"
			# else:
			# 	if shouldMove:
			# 		print "acceptable"
			# 	else:
			# 		print "good call"

			i += 1

		if moves:
			self.assured = True
			self.decided = True

		return self.chooseMove(moves)

	def shouldStrong(self,move,forceMoves):
		""" decides whether a point's worth it to try forcing """
		if move in forceMoves:
			return False
		openLines = []
		for i in range(2):
			openLines += self.b.openLinesForPoint(self.n,move,i)
		if len(openLines) < 3:
			return False
		goodLines = self.b.openLinesForPoint(self.n,move,1)
		if len(goodLines) < 2:
			return False

		return True

	def otherLookAhead(self, display):
		""" looks ahead defensively to try to block opponent's forces """

		badGuy = Vaapad()
		badGuy.updateAll(self.b,self.o,self.d,self.lastPrintTime)
		possMoves = []
		workingMoves = []

		combos, forceList = badGuy.findCombos(display)

		if badGuy.assured:
			if display[1] == 3:
				return False

			display = [display[i] if i != 1 else display[i]+1 for i in range(len(display))]

			possMoves = self.getPossMoves(combos, forceList, possMoves)

			i = 0
			while possMoves:
				move = possMoves[0]

				if display[1] == 1:
					display[0] = 100.0*i/(len(possMoves)+i)
					display[3] = len(workingMoves)
				if display[2] == 2 and display[1] == 2:
					display[0] = (100.0/display[5])*(display[4]+1.0*i/(len(possMoves)+i))

				self.updateText(display[0],display[1],0,display[2], display[3])

				badGuy.assured = False
				badGuy.b.move(badGuy.o,move)

				check = badGuy.fourInARow(badGuy.o)

                # this means it will never try a casual check out of shatterpoint
				if check:
					newPossMoves = possMoves[1:]
				# 	badGuy.b.move(badGuy.n,check)
                #
				# 	goodGuy = Vaapad()
				# 	goodGuy.updateAll(badGuy.b,badGuy.o,badGuy.d,badGuy.lastPrintTime)
                #
				# 	lookFurther = goodGuy.otherLookAhead(display)
                #
				# 	badGuy.b.clearPoint(check)
				# 	badGuy.b.clearPoint(move)
                #
				# 	if lookFurther:
				# 		if display[1] != 1:
				# 			return True
				# 		workingMoves += [move]
                #

				else:
					combos, forceList = badGuy.findCombos(display)

					badGuy.b.clearPoint(move)

					if not badGuy.assured:
						if display[1] != 1:
							return True
						workingMoves += [move]
						newPossMoves = possMoves[1:]

					else:
						newPossMoves = self.getPossMoves(combos,forceList,possMoves)

				i += 1
				possMoves = newPossMoves

			if workingMoves:
				self.moves = workingMoves

			else: # admit defeat
				self.scared = True
				if display[1] != 1:
					return False

		else:
			if display[1] != 0:
				return True

	def getPossMoves(self, combos, forceList,possMoves):
		""" gets the possible, shared moves among each combo """
		for i in range(len(combos)):
			comboMoves = []
			for pair in combos[i]:
				for move in pair:
					if move not in comboMoves:
						comboMoves += [move]
			for pair in forceList[i]:
				for move in pair:
					if move not in comboMoves:
						comboMoves += [move]

			if i == 0 and not possMoves:
				possMoves = comboMoves
			else:
				newPM = []
				for move in possMoves:
					if move in comboMoves:
						newPM += [move]
				possMoves = newPM
		return possMoves

	def weakLookAhead(self):
		""" looks ahead, tries to set up a decent force """
		forceMoves = []
		pairs = self.b.findForces(self.n)
		for pair in pairs:
			for m in pair:
				forceMoves += [m]

		bestScore = 0
		bestMoves = set()
		orig = self.webMagicNumber(0,None)

		i = 0
		nMoves = len(self.moves)

		for move in self.moves:
			goodGuy = Vaapad()
			goodGuy.updateAll(self.b,self.n,self.d,self.lastPrintTime)
			goodGuy.b.move(self.n,move)

			score = goodGuy.webMagicNumber(orig, move)

			if move not in forceMoves:
				finished = goodGuy.findShatterpoint([100.0*i/nMoves,1,3,len(bestMoves)], 6)
				if goodGuy.assured or not finished:
					score = score*1.25

			if score > bestScore:
				bestScore = score
				bestMoves = set()
			if score == bestScore:
				bestMoves.add(move)

			i += 1

		return self.chooseMove(list(bestMoves))

	# updating/boardy functions
	def goodMagicNumber(self, originalScore, move):
		"""
		finds all the good shit
		"""
		goodLines = [0,3,5,6,9,10,12,15,16,19,21,22,25,26,28,31,32,35,37,38,41,42,44,47]
		goodLines += range(48,76)

		mainDiags = range(72,76)

		myPoints = self.b.myPoints(self.n)
		osPoints = self.b.myPoints(self.o)

		myLines = 0
		osLines = 0

		for point in myPoints:
			lines = self.myLines(point,self.n)
			for l in lines:
				if l in goodLines:
					myLines += 1
				if l in mainDiags:
					myLines += 1
		for point in osPoints:
			lines = self.myLines(point,self.o)
			for l in lines:
				if l in goodLines:
					osLines += 1
				if l in mainDiags:
					osLines += 1

		# print move, myLines, osLines

	def webMagicNumber(self, originalScore, move):
		"""
		a new magic number theory
		"""

		myPoints, osPoints = self.checkPoints()
		myPlanes, osPlanes = self.checkPlanes()

		ODQ = (1-osPlanes/2.5)/2.0

		score = myPoints*(1+ODQ) + osPoints*(-1+ODQ)

		preMultiplyer = self.checkGoodPoints()

		return (score - originalScore)*preMultiplyer

	def checkGoodPoints(self):
		""" checks good points real good """

		corners = [(0,0,0),(3,0,0),(0,3,0),(0,0,3),(0,3,3),(3,0,3),(3,3,0),(3,3,3)]
		centers = [(1,1,1),(2,1,1),(1,2,1),(1,1,2),(1,2,2),(2,1,2),(2,2,1),(2,2,2)]

		cornerN = [self.b.pointToValue(c) for c in corners]
		centerN = [self.b.pointToValue(c) for c in centers]

		cornerC = (cornerN.count(self.n), cornerN.count(self.o))
		centerC = (centerN.count(self.n), centerN.count(self.o))

		mostC = [0,0]
		mostC[0] = cornerC[0] if cornerC[0] > centerC[0] else centerC[0]
		mostC[1] = cornerC[1] if cornerC[1] > centerC[1] else centerC[1]

		return 1.0*2**mostC[0]/(2**mostC[1])

	def checkPoints(self):
		""" checks points magically """

		myPoints, osPoints = (0,)*2

		goodPoints = [(0,0,0),(3,0,0),(0,3,0),(0,0,3),(0,3,3),(3,0,3),(3,3,0),(3,3,3),
					  (1,1,1),(2,1,1),(1,2,1),(1,1,2),(1,2,2),(2,1,2),(2,2,1),(2,2,2)]

		for p in goodPoints:
			myL = len(self.myLines(p,self.n))
			osL = len(self.myLines(p,self.o))

			if myL > osL:
				myPoints += myL-osL
			elif osL > myL:
				osPoints += osL-myL

		return myPoints, osPoints

	def checkPlanes(self):
		""" checks planes magically """
		r4 = range(4)
		planes = []
		myPlanes, osPlanes = (0,)*2

		planes += [[self.b.pointToValue((i,j,k)) for i in r4 for j in r4] for k in r4]
		planes += [[self.b.pointToValue((k,i,j)) for i in r4 for j in r4] for k in r4]
		planes += [[self.b.pointToValue((j,k,i)) for i in r4 for j in r4] for k in r4]

		planes += [[self.b.pointToValue((i,i,j)) for i in r4 for j in r4]]
		planes += [[self.b.pointToValue((3-i,i,j)) for i in r4 for j in r4]]

		planes += [[self.b.pointToValue((j,i,i)) for i in r4 for j in r4]]
		planes += [[self.b.pointToValue((j,3-i,i)) for i in r4 for j in r4]]

		planes += [[self.b.pointToValue((i,j,i)) for i in r4 for j in r4]]
		planes += [[self.b.pointToValue((i,j,3-i)) for i in r4 for j in r4]]

		for plane in planes:
			myN = plane.count(self.n)
			osN = plane.count(self.o)
			if myN and not osN:
				myPlanes += myN**2
			elif osN and not myN:
				osPlanes += osN**2

		return myPlanes, osPlanes

	def good(self,p):
		""" returns true if the point is good """
		# add corners
		goodP = [(0,0,0),(3,0,0),(0,3,0),(0,0,3),(0,3,3),(3,0,3),(3,3,0),(3,3,3),
				 (1,1,1),(2,1,1),(1,2,1),(1,1,2),(1,2,2),(2,1,2),(2,2,1),(2,2,2)]
		return p in goodP

	def good2(self,p):
		""" returns true if the point is good """
		# add corners
		goodP = [(0,0,0),(3,0,0),(0,3,0),(0,0,3),(0,3,3),(3,0,3),(3,3,0),(3,3,3)]
		return p in goodP

	def myLines(self,p,n):
		""" gets all the open lines for the point for num > 0 """

		lines = []
		for num in range(1,4):
			lines += self.b.openLinesForPoint(n,p,num)*num

		return lines

	def updateForPoint(self, p):
		"""
		Updates pairs, moves, and lines after point p has been filled
		More efficient than updating fully each time
		"""

	def updateAll(self, board, n, newDisplay, printTime):
		"""
		Updates all pairs, moves and lines for the current board
		"""
		self.b.copyAll(board) # Board object, not array
		self.n = n
		self.d = newDisplay
		self.o = self.b.otherNumber(self.n)
		self.moves = list(self.b.openPoints())
		self.nMoves = len(self.b.myPoints(self.n))
		self.decided = False
		self.assured = False
		self.scared = False

		self.lastPrintTime = printTime
