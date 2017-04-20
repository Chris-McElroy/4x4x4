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
	fourMoveBoard[0][1][2] = 2
	# line boards
	oneLineXBoard = [[[1 if (i%4 == 0 and j%4 == 0) else 0 for i in range(4)] for j in range(4)] for k in range(4)]
	oneLineYBoard = [[[1 if (i%4 == 0 and k%4 == 0) else 0 for i in range(4)] for j in range(4)] for k in range(4)]
	oneLineZBoard = [[[1 if (k%4 == 0 and j%4 == 0) else 0 for i in range(4)] for j in range(4)] for k in range(4)]
	# plane is z = 0
	onePlaneBoard = [[[1 if (i%4 == 0) else 0 for i in range(4)] for j in range(4)] for k in range(4)]

	def test_clearBoard(self):
		test1 = Board()
		self.assertEqual(test1.b,self.openBoard)

		self.assertEqual(test1.clearBoard(), 0)
		self.assertEqual(test1.b,self.openBoard)

		test1.move(1,0,0,0)
		test1.move(2,0,0,1)
		test1.move(2,0,0,2)
		self.assertEqual(test1.clearBoard(), 3)
		self.assertEqual(test1.b,self.openBoard)

	def test_openPoints(self):
		test1 = Board()
		test2 = [[i,j,k] for i in range(4) for j in range(4) for k in range(4)]
		self.assertEqual(test1.openPoints(),test2)

		test1.move(1,0,0,0)
		test1.move(2,0,0,1)
		test1.move(2,1,0,2)

		test2 = test2[2:18] + test2[19:]
		self.assertEqual(test1.openPoints(),test2)

	def test_myPoints(self):
		n = 1
		test1 = Board()
		test2 = []
		self.assertEqual(test1.myPoints(n),test2)

		test1.move(1,0,0,0)
		test2 += [[0,0,0]]
		self.assertEqual(test1.myPoints(n),test2)

		test1.move(2,0,0,1)
		self.assertEqual(test1.myPoints(n),test2)

		test1.move(1,1,2,3)
		test2 += [[1,2,3]]
		self.assertEqual(test1.myPoints(n),test2)

		test1.move(1,0,0,1)
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

		test1.move(1,0,0,0)
		self.assertEqual(test1.numMoves(n),[1,0])

		test1.move(2,0,0,1)
		self.assertEqual(test1.numMoves(n),[1,1])

		test1.move(2,1,1,2)
		self.assertEqual(test1.numMoves(n),[1,2])

		test1.move(1,0,0,1)
		self.assertEqual(test1.numMoves(n),[1,2])

	def test_move(self):
		test1 = Board()
		test2 = self.openBoard
		self.assertEqual(test1.b,test2)

		self.assertEqual(test1.move(1,0,0,0),True)
		self.assertEqual(test1.move(2,0,1,2),True)
		self.assertEqual(test1.move(2,1,2,3),True)
		self.assertEqual(test1.move(1,3,2,1),True)
		self.assertEqual(test1.move(2,0,0,0),False)
		self.assertEqual(test1.move(2,1,2,3),False)

		test2 = self.fourMoveBoard
		self.assertEqual(test1.b,test2)

	def test_findLines(self):
		test1 = Board()
		lines = []
		self.assertEqual(test1.findLines(1,1),lines)

		test1.b = self.twosBoard
		self.assertEqual(test1.findLines(1,1),lines)

		test1.b = self.onesBoard
		lines = range(76)
		self.assertEqual(test1.findLines(1,1),lines)
		self.assertEqual(test1.findLines(1,2),lines)
		self.assertEqual(test1.findLines(1,3),lines)
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
		self.assertEqual(test1.findLines(1,1),lines)

		lines = range(76)
		self.assertEqual(test1.findLines(1,0),lines)

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

	# def test_pointsToLine(self):

	# def test_lineToValues(self):

	# def test_findForces(self):

	# def test_linesForPoint(self):

	# def test_openLinesForPoint(self):



if __name__ == '__main__':
    unittest.main()






		