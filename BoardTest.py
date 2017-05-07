from Board import *
import unittest

class BoardTest(unittest.TestCase):

	# Global boards for testing (add more up here as needed)
	openBoard = [[[0 for i in range(4)] for j in range(4)] for k in range(4)]
	onesBoard = [[[1 for i in range(4)] for j in range(4)] for k in range(4)]
	twosBoard = [[[2 for i in range(4)] for j in range(4)] for k in range(4)]
	# single 1 at 0,0,0
	oneMoveBoard = [[[0 for i in range(4)] for j in range(4)] for k in range(4)]
	oneMoveBoard[0][0][0] = 1
	# 1 at 0,0,0, 1 at 3,2,1, 2 at 1,2,3, 2 at 0,1,2. 
	fourMoveBoard = [[[0 for i in range(4)] for j in range(4)] for k in range(4)]
	fourMoveBoard[0][0][0] = 1
	fourMoveBoard[3][2][1] = 1
	fourMoveBoard[1][2][3] = 2
	fourMoveBoard[0][2][1] = 2
	# line boards
	oneLineXBoard = [[[1 if (i%4 == 0 and j%4 == 0) else 0 for i in range(4)] for j in range(4)] for k in range(4)]
	oneLineYBoard = [[[1 if (i%4 == 0 and k%4 == 0) else 0 for i in range(4)] for j in range(4)] for k in range(4)]
	oneLineZBoard = [[[1 if (k%4 == 0 and j%4 == 0) else 0 for i in range(4)] for j in range(4)] for k in range(4)]
	# plane is z = 0
	onePlaneBoard = [[[1 if (i%4 == 0) else 0 for i in range(4)] for j in range(4)] for k in range(4)]
	# forcing boards
	twoMoveBoard = [[[1 if (k%4 == 0 and j%4 == 0 and i % 2 != 0) else 0 for i in range(4)] for j in range(4)] for k in range(4)]
	forcingBoard = [[[1 if (i%2 != 0) else 0 for i in range(4)] for j in range(4)] for k in range(4)]

	def test_clearBoard(self):
		test1 = Board()
		self.assertEqual(test1.b,self.openBoard)

		self.assertEqual(test1.clearBoard(), 0)
		self.assertEqual(test1.b,self.openBoard)

		test1.b = self.fourMoveBoard
		self.assertEqual(test1.clearBoard(), 4)
		self.assertEqual(test1.b,self.openBoard)

	def test_openPoints(self):
		test1 = Board()
		test2 = [[i,j,k] for i in range(4) for j in range(4) for k in range(4)]
		self.assertEqual(test1.openPoints(),test2)

		test1.move(1,[0,0,0])
		test1.move(2,[0,0,1])
		test1.move(2,[1,0,2])

		test2 = test2[2:18] + test2[19:]
		self.assertEqual(test1.openPoints(),test2)

	def test_myPoints(self):
		n = 1
		test1 = Board()
		test2 = []
		self.assertEqual(test1.myPoints(n),test2)

		test1.move(1,[0,0,0])
		test2 += [[0,0,0]]
		self.assertEqual(test1.myPoints(n),test2)

		test1.move(2,[0,0,1])
		self.assertEqual(test1.myPoints(n),test2)

		test1.move(1,[1,2,3])
		test2 += [[1,2,3]]
		self.assertEqual(test1.myPoints(n),test2)

		test1.move(1,[0,0,1])
		self.assertEqual(test1.myPoints(n),test2)

	def test_otherNumber(self):
		test1 = Board()
		self.assertEqual(test1.otherNumber(1),2)
		self.assertEqual(test1.otherNumber(2),1)
		self.assertEqual(test1.otherNumber(0),0)
		self.assertEqual(test1.otherNumber(4),0)

	def test_numMoves(self):
		n = 1
		test1 = Board()
		self.assertEqual(test1.numMoves(n),[0,0])

		test1.move(1,[0,0,0])
		self.assertEqual(test1.numMoves(n),[1,0])

		test1.move(2,[0,0,1])
		self.assertEqual(test1.numMoves(n),[1,1])

		test1.move(2,[1,1,2])
		self.assertEqual(test1.numMoves(n),[1,2])

		test1.move(1,[0,0,1])
		self.assertEqual(test1.numMoves(n),[1,2])

	def test_move(self):
		test1 = Board()
		test2 = self.openBoard
		self.assertEqual(test1.b,test2)

		self.assertEqual(test1.move(1,[0,0,0]),True)
		self.assertEqual(test1.move(2,[0,2,1]),True)
		self.assertEqual(test1.move(2,[1,2,3]),True)
		self.assertEqual(test1.move(1,[3,2,1]),True)
		self.assertEqual(test1.move(2,[0,0,0]),False)
		self.assertEqual(test1.move(2,[1,2,3]),False)

		test2 = self.fourMoveBoard
		self.assertEqual(test1.b,test2)

	def test_findLines(self):
		test1 = Board()
		lines = []
		self.assertEqual(test1.findLines(1,1),lines)

		test1.b = self.twosBoard
		self.assertEqual(test1.findLines(1,1),lines)

		test1.b = self.onesBoard
		self.assertEqual(test1.findLines(1,1),lines)
		self.assertEqual(test1.findLines(1,2),lines)
		self.assertEqual(test1.findLines(1,3),lines)

		lines = range(76)
		self.assertEqual(test1.findLines(1,4),lines)

		test1.b = self.oneLineXBoard
		lines = [0]
		self.assertEqual(test1.findLines(1,4),lines)

		test1.b = self.oneLineYBoard
		lines = [16]
		self.assertEqual(test1.findLines(1,4),lines)

		test1.b = self.oneLineZBoard
		lines = [32]
		self.assertEqual(test1.findLines(1,4),lines)

		test1.b = self.oneMoveBoard
		lines = test1.linesForPoint([0,0,0])
		self.assertEqual(test1.findLines(1,1),lines) # will fail without lines for point written

		lines = range(76)
		for l in test1.linesForPoint([0,0,0]):
			lines.remove(l)
		self.assertEqual(test1.findLines(1,0),lines) # will fail without lines for point written

		test1.b = self.onePlaneBoard
		lines = [0,4,8,12]+range(16,20)+[64]+[68]
		self.assertEqual(test1.findLines(1,4),lines)

	def test_lineToPoints(self):
		test1 = Board()
		points = [[i,2,3] for i in range(4)]
		line = 11
		self.assertEqual(test1.lineToPoints(line),points)

		points = [[3,i,2] for i in range(4)]
		line = 11+16
		self.assertEqual(test1.lineToPoints(line),points)

		points = [[2,3,i] for i in range(4)]
		line = 11+32
		self.assertEqual(test1.lineToPoints(line),points)

		points = [[1,i,i] for i in range(4)]
		line = 1+48
		self.assertEqual(test1.lineToPoints(line),points)

		points = [[i,1,i] for i in range(4)]
		line = 1+56
		self.assertEqual(test1.lineToPoints(line),points)

		points = [[i,i,1] for i in range(4)]
		line = 1+64
		self.assertEqual(test1.lineToPoints(line),points)

		points = [[i,i,3-i] for i in range(4)]
		line = 73
		self.assertEqual(test1.lineToPoints(line),points)

	def test_pointsToLine(self):
		test1 = Board()
		point1 = [0,0,0]
		point2 = [0,0,0]
		line = -1
		self.assertEqual(test1.pointsToLine(point1,point2),line)

		point2 = [0,0,4]
		self.assertEqual(test1.pointsToLine(point1,point2),line)

		point2 = [1,1,2]
		self.assertEqual(test1.pointsToLine(point1,point2),line)

		point1 = [3,2,3]
		point2 = [1,2,3]
		line = 0 + 11
		self.assertEqual(test1.pointsToLine(point1,point2),line)

		point1 = [3,3,2]
		point2 = [3,1,2]
		line = 16 + 11
		self.assertEqual(test1.pointsToLine(point1,point2),line)

		point1 = [2,3,3]
		point2 = [2,3,1]
		line = 32 + 11
		self.assertEqual(test1.pointsToLine(point1,point2),line)

		point1 = [1,1,1]
		point2 = [1,3,3]
		line = 48 + 1
		self.assertEqual(test1.pointsToLine(point1,point2),line)

		point1 = [1,1,1]
		point2 = [3,1,3]
		line = 56 + 1
		self.assertEqual(test1.pointsToLine(point1,point2),line)

		point1 = [1,1,1]
		point2 = [3,3,1]
		line = 64 + 1
		self.assertEqual(test1.pointsToLine(point1,point2),line)

		point1 = [1,1,2]
		point2 = [3,3,0]
		line = 72 + 1
		self.assertEqual(test1.pointsToLine(point1,point2),line)

	def test_lineToValues(self):
		test1 = Board()
		test1.b = self.oneMoveBoard
		values = [1,0,0,0]

		self.assertEqual(test1.lineToValues(0),values)
		self.assertEqual(test1.lineToValues(16),values)
		self.assertEqual(test1.lineToValues(32),values)
		self.assertEqual(test1.lineToValues(48),values)
		self.assertEqual(test1.lineToValues(56),values)
		self.assertEqual(test1.lineToValues(64),values)
		self.assertEqual(test1.lineToValues(72),values)

		test1.b = self.fourMoveBoard
		self.assertEqual(test1.lineToValues(0),values)

		values = [2,0,0,1]
		self.assertEqual(test1.lineToValues(9),values)

		values = [0,0,0,0]
		self.assertEqual(test1.lineToValues(49),values)

		values = [0,0,2,0]
		self.assertEqual(test1.lineToValues(29),values)

	def test_findForces(self):
		test1 = Board()
		pairs = []
		self.assertEqual(test1.findForces(1),pairs)

		test1.b = self.twoMoveBoard
		pairs = [[[0,0,0],[0,0,2]]]
		self.assertEqual(test1.findForces(1),pairs)

		test1.b = self.fourMoveBoard
		pairs = []
		self.assertEqual(test1.findForces(1),pairs)
		self.assertEqual(test1.findForces(2),pairs)

		test1.b = self.forcingBoard
		pairs = [[[i,j,0],[i,j,2]] for i in range(4) for j in range(4)]
		pairs += [[[i,0,0],[i,2,2]] for i in range(4)]
		pairs += [[[i,1,2],[i,3,0]] for i in range(4)]
		pairs += [[[0,i,0],[2,i,2]] for i in range(4)]
		pairs += [[[1,i,2],[3,i,0]] for i in range(4)]
		pairs += [[[0,0,0],[2,2,2]],[[1,1,2],[3,3,0]],[[0,3,0],[2,1,2]],[[3,0,0],[1,2,2]]]
		self.assertEqual(test1.findForces(1),pairs)

	def test_linesForPoint(self):
		test1 = Board()
		point = [0,0,0]
		lines = [0,16,32,48,56,64,72]
		self.assertEqual(test1.linesForPoint(point),lines)

		point = [1,0,0]
		lines = [0,17,36,49]
		self.assertEqual(test1.linesForPoint(point),lines)

		point = [2,1,2]
		lines = [6,26,41,54,57,70,74]
		self.assertEqual(test1.linesForPoint(point),lines)

		point = [3,1,2]
		lines = [6,27,45,55]
		self.assertEqual(test1.linesForPoint(point),lines)

	def test_openLinesForPoint(self):
		test1 = Board()
		point = [0,0,0]
		lines = [0,16,32,48,56,64,72]
		self.assertEqual(test1.openLinesForPoint(1,point,0),lines)

		point = [1,0,0]
		lines = [0,17,36,49]
		self.assertEqual(test1.openLinesForPoint(1,point,0),lines)

		point = [2,1,2]
		lines = [6,26,41,54,57,70,74]
		self.assertEqual(test1.openLinesForPoint(1,point,0),lines)

		point = [3,1,2]
		lines = [6,27,45,55]
		self.assertEqual(test1.openLinesForPoint(1,point,0),lines)

		# now with somewhat blocked board
		test1.b = self.fourMoveBoard
		point = [0,0,0]
		lines = []
		self.assertEqual(test1.openLinesForPoint(1,point,0),lines)
		lines = [0,16,32,48,56,64,72]
		self.assertEqual(test1.openLinesForPoint(1,point,1),lines)
		lines = []
		self.assertEqual(test1.openLinesForPoint(1,point,2),lines)
		self.assertEqual(test1.openLinesForPoint(2,point,0),lines)

		point = [1,0,0]
		lines = [17,36,49]
		self.assertEqual(test1.openLinesForPoint(1,point,0),lines)

		point = [2,1,2]
		lines = [6,26,41,54,57,70,74]
		self.assertEqual(test1.openLinesForPoint(1,point,0),lines)
		self.assertEqual(test1.openLinesForPoint(2,point,0),lines)
		lines = []
		self.assertEqual(test1.openLinesForPoint(1,point,2),lines)
		self.assertEqual(test1.openLinesForPoint(2,point,1),lines)

		point = [3,1,2]
		lines = [6,27,45]
		self.assertEqual(test1.openLinesForPoint(1,point,0),lines)
		lines = [55]
		self.assertEqual(test1.openLinesForPoint(1,point,1),lines)
		lines = []
		self.assertEqual(test1.openLinesForPoint(1,point,2),lines)
		self.assertEqual(test1.openLinesForPoint(2,point,1),lines)
		lines = [6,27,45]
		self.assertEqual(test1.openLinesForPoint(2,point,0),lines)

if __name__ == '__main__':
    unittest.main()






		