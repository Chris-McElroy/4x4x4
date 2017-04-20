class Board:
	"""
	Provides the 4x4x4 board for the game, holds all moves, can be used for lookahead
	"""

	#constructor	
	def __init__(self):
		""" Creates original Board """
		self.b = [[[0 for i in range(4)] for j in range(4)] for k in range(4)]

	# make, check and clear moves
	def clearBoard(self):
		"""
		Clears the board for a new game
		returns the number of moves deleted
		"""
		currentMoves = self.numMoves(1)
		self.b = [[[0 for i in range(4)] for j in range(4)] for k in range(4)]
		return sum(currentMoves)

	def openPoints(self):
		"""
		Return a list of all open points on the board
		"""
		points = []
		for i in range(4):
			for j in range(4):
				for k in range(4):
					current = self.b[i][j][k]
					if (current == 0):
						points += [[i,j,k]]
		return points

	def myPoints(self, n):
		"""
		Return a list of all points player n has on the board
		"""
		return []

	def otherNumber(self, n):
		"""
		Returns the other player's number
		"""

	def numMoves(self, n):
		""" Finds how many moves have been made by each player """
		p1 = 0
		p2 = 0
		for i in range(4):
			for j in range(4):
				for k in range(4):
					current = self.b[i][j][k]
					if (current == n):
						p1 += 1
					elif (current != 0):
						p2 += 1
		return [p1,p2]

	def move(self,n,x,y,z):
		""" moves player n at x,y,z, returns false if blocked """

		current = self.b[x][y][z]
		if (current == 0):
			self.b[x][y][z] = n
			return True
		else:
			return False

	# Find lines
	def findLines(self,n,num):
		""" 
		Checks all lines on the board, returns the line number
		of all lines for which player n has at least num points,
		but player !n has none.
		"""

		lines = []

		for l in range(76):
			values = self.lineToValues(l)
			p1 = 0
			p2 = 0
			for v in values:
				if (v == n):
					p1 += 1
				elif (v != 0):
					p2 += 1
			if (p1 >= num and p2 == 0):
				lines += [l]

		return lines

	def findRows(self, n, num):
		"""
		Checks all the row lines on the board for having
		at least num points for player n and none for player !n
		"""
		lines = []
		for i in range(4):
			for j in range(4):
				p1 = 0
				p2 = 0
				for k in range(4):
					current = self.b[k][i][j]
					if (current == n):
						p1 += 1
					elif (current != 0):
						p2 += 1
				if (p1 >= num and p2 == 0):
					lines += [4*i + j]
		return lines

	def findCols(self, n, num):
		"""
		Checks all the column lines on the board for having
		at least num points for player n and none for player !n
		"""
		lines = []
		for i in range(4):
			for j in range(4):
				p1 = 0
				p2 = 0
				for k in range(4):
					current = self.b[j][k][i]
					if (current == n):
						p1 += 1
					elif (current != 0):
						p2 += 1
				if (p1 >= num and p2 == 0):
					lines += [16 + 4*i + j]
		return lines

	def findVrts(self, n, num):
		"""
		Checks all the vertical lines on the board for having
		at least num points for player n and none for player !n
		"""
		lines = []
		for i in range(4):
			for j in range(4):
				p1 = 0
				p2 = 0
				for k in range(4):
					current = self.b[i][j][k]
					if (current == n):
						p1 += 1
					elif (current != 0):
						p2 += 1
				if (p1 >= num and p2 == 0):
					lines += [32 + 4*i + j]
		return lines		

	def findDias(self, n, num):
		"""
		Checks all the diagonal lines on the board for having
		at least num points for player n and none for player !n
		"""

		lines = []

		# x stays constant
		for i in range(4):
			p1 = 0
			p2 = 0
			for j in range(4):
				current = self.b[i][j][j]
				if (current == n):
					p1 += 1
				elif (current != 0):
					p2 += 1
			if (p1 >= num and p2 == 0):
				lines += [48 + i]

		for i in range(4):
			p1 = 0
			p2 = 0
			for j in range(4):
				current = self.b[i][j][3-j]
				if (current == n):
					p1 += 1
				elif (current != 0):
					p2 += 1
			if (p1 >= num and p2 == 0):
				lines += [52 + i]


		# y stays constant
		for i in range(4):
			p1 = 0
			p2 = 0
			for j in range(4):
				current = self.b[j][i][j]
				if (current == n):
					p1 += 1
				elif (current != 0):
					p2 += 1
			if (p1 >= num and p2 == 0):
				lines += [56 + i]

		for i in range(4):
			p1 = 0
			p2 = 0
			for j in range(4):
				current = self.b[j][i][3-j]
				if (current == n):
					p1 += 1
				elif (current != 0):
					p2 += 1
			if (p1 >= num and p2 == 0):
				lines += [60 + i]

		# z stays constant
		for i in range(4):
			p1 = 0
			p2 = 0
			for j in range(4):
				current = self.b[j][j][i]
				if (current == n):
					p1 += 1
				elif (current != 0):
					p2 += 1
			if (p1 >= num and p2 == 0):
				lines += [64 + i]

		for i in range(4):
			p1 = 0
			p2 = 0
			for j in range(4):
				current = self.b[j][3-j][i]
				if (current == n):
					p1 += 1
				elif (current != 0):
					p2 += 1
			if (p1 >= num and p2 == 0):
				lines += [68 + i]

		# major diagonals

	# Point/Line conversions
	def lineToPoints(self, line):
		"""
		Given a line number, this will return the set of four
		points that make up that line, listed by x, y, and z
		"""
		if (0 <= line and line < 16):
			return self.rowsToPoints(line)
		elif (16 <= line and line < 32):
			return self.colsToPoints(line)
		elif (32 <= line and line < 48):
			return self.vrtsToPoints(line)
		elif (48 <= line and line < 76):
			return self.diasToPoints(line)
		else:
			return []

	def rowsToPoints(self, line):
		"""
		Given a line number between 0 and 15, this will return the
		set of four points that make up that line, listed by x, y, and z
		"""
		l = line
		z = l % 4
		y = (l-z)/4
		return [[i,y,z] for i in range(4)]

	def colsToPoints(self, line):
		"""
		Given a line number between 16 and 31, this will return the
		set of four points that make up that line, listed by x, y, and z
		"""
		l = line - 16
		x = l % 4
		z = (l-x)/4
		return [[x,i,z] for i in range(4)]

	def vrtsToPoints(self, line):
		"""
		Given a line number between 32 and 47, this will return the
		set of four points that make up that line, listed by x, y, and z
		"""
		l = line - 32
		y = l % 4
		x = (l-y)/4
		return [[x,y,i] for i in range(4)]

	def diasToPoints(self, line):
		"""
		Given a line number between 48 and 75, this will return the
		set of four points that make up that line, listed by x, y, and z
		"""
		if (48 <= line and line < 52):
			l = line - 48
			x = l % 4
			return [[x,i,i] for i in range(4)]
		if (52 <= line and line < 56):
			l = line - 52
			x = l % 4
			return [[x,i,3-i] for i in range(4)]
		if (56 <= line and line < 60):
			l = line - 56
			y = l % 4
			return [[i,y,i] for i in range(4)]
		if (60 <= line and line < 64):
			l = line - 60
			y = l % 4
			return [[i,y,3-i] for i in range(4)]
		if (64 <= line and line < 68):
			l = line - 64
			z = l % 4
			return [[i,i,z] for i in range(4)]
		if (68 <= line and line < 72):
			l = line - 68
			z = l % 4
			return [[i,3-i,z] for i in range(4)]
		if (line == 72):
			return [[i,i,i] for i in range(4)]
		if (line == 73):
			return [[i,i,3-i] for i in range(4)]
		if (line == 74):
			return [[i,3-i,i] for i in range(4)]
		if (line == 75):
			return [[3-i,i,i] for i in range(4)]

	def pointsToLine(self,p1,p2):
		"""
		Given two points, this will return their line number
		if they're in a line, and -1 if they are not
		"""

		line = -1

		# make sure points are valid
		for p in p1,p2:
			for v in p:
				if (v < 0 or v > 3):
					return line

		# see if they have the same x
		if (p1[0] == p2[0]):
			# see if they have the same y
			if (p1[1] == p2[1]):
				# must be vertical
				if (p1[2] != p2[2]):
					line = 32 + 4*p1[0] + p1[1]
			# see if they have the same z
			elif (p1[2] == p2[2]):
				# must be in y dir
				line = 16 + 4*p1[2] + p1[0]
			# if both y and z change it must be diagonal
			# see if it's coming from 0,0 or 0,3
			elif (p1[1] == p1[2]):
				# should be coming from 0,0; check
				if (p2[1] == p2[2]):
					line = 48 + p1[0]
			elif (p1[1] == 3 - p1[2]):
				# should be coming from 0,0; check
				if (p2[1] == 3-p2[2]):
					line = 52 + p1[0]
		# see if they have the same y
		elif (p1[1] == p2[1]):
			# see if they have the same z
			if (p1[2] == p2[2]):
				# must be in x dir
				line = 4*p1[1] + p1[2]
			# if both x and z change it must be diagonal
			# see if it's coming from 0,0 or 0,3
			elif (p1[0] == p1[2]):
				# should be coming from 0,0; check
				if (p2[0] == p2[2]):
					line = 56 + p1[1]
			elif (p1[0] == 3 - p1[2]):
				# should be coming from 0,0; check
				if (p2[0] == 3-p2[2]):
					line = 60 + p1[1]
		# see if they have the same z
		elif (p1[2] == p2[2]):
			# if both x and y change it must be diagonal
			# see if it's coming from 0,0 or 0,3
			if (p1[0] == p1[1]):
				# should be coming from 0,0; check
				if (p2[0] == p2[1]):
					line = 64 + p1[2]
			elif (p1[0] == 3 - p1[1]):
				# should be coming from 0,0; check
				if (p2[0] == 3-p2[1]):
					line = 68 + p1[2]
		# if all change, must be on a main diagonal
		# diagnoal 1
		elif (p1[0] == p1[1] and p1[0] == p1[2]):
			# check p2
			if (p2[0] == p2[1] and p2[0] == p2[2]):
				line = 72
		# diagonal 2
		elif (p1[0] == p1[1] and p1[0] == 3 - p1[2]):
			# check p2
			if (p2[0] == p2[1] and p2[0] == 3 - p2[2]):
				line = 73
		# diagonal 3
		elif (p1[0] == 3 - p1[1] and p1[0] == p1[2]):
			# check p2
			if (p2[0] == 3 - p2[1] and p2[0] == p2[2]):
				line = 74
		# diagonal 4
		elif (p1[0] == 3 - p1[1] and p1[0] == 3 - p1[2]):
			# check p2
			if (p2[0] == 3 - p2[1] and p2[0] == 3 - p2[2]):
				line = 75

		return line

	# Searching specific lines
	def lineToValues(self, line):
		"""
		Given a line number, this will return the value of all
		four points in a list
		"""
		values = []
		points = self.lineToPoints(line)
		for p in points:
			current = self.b[p[0]][p[1]][p[2]]
			values += [current]
		return values

	# finding force moves
	def findForces(self, n):
		"""
		Returns pairs of forcing moves
		"""
		pairs = []
		blocked = False

		for l in range(76):
			points = self.lineToPoints(l)
			openPoints = []
			for i in range(4):
				v = self.b[points[i][0]][points[i][1]][points[i][2]]
				if (v == 0):
					openPoints += [i]
				elif (v != n):
					blocked = True
					break
			if (not blocked and len(openPoints) == 2):
				pairs += [[points[openPoints[0]], points[openPoints[1]]]]
		return pairs

	def linesForPoint(self, p):
		"""
		Returns a list of all the line numbers passing through point p
		"""
		return []

	def openLinesForPoint(self, n, p, num):
		"""
		Returns a list of all the line numbers of lines passing through
		point p, with no non n moves and num moves by player n
		"""

		otherN = self.otherNumber(n)
		lines = self.linesForPoint(p)
		openLines = []
		for l in lines:
			blocked = False
			values = self.lineToValues(l)
			p1 = 0
			for v in values:
				if (v == otherN):
					blocked = True
					break
				if (v == n):
					p1 += 1
			if (p1 >= num and not blocked):
				openLines += [l]
		return openLines










