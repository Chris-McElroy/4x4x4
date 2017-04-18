from Board import *
import unittest

class boardTest(unittest.TestCase):

	# Global boards for testing (add more up here as needed)
	openBoard = [[[0 for i in range(4)] for j in range(4)] for k in range(4)]
	onesBoard = [[[1 for i in range(4)] for j in range(4)] for k in range(4)]
	twosBoard = [[[2 for i in range(4)] for j in range(4)] for k in range(4)]
	# single 1 at 0,0,0
	oneMoveBoard = openBoard
	oneMoveBoard[0][0][0] = 1
	# 1 at 0,0,0, 1 at 3,2,1, 2 at 3,2,1, 2 at 0,1,2. 
	fourMoveBoard = oneMoveBoard
	fourMoveBoard[3][2][1] = 1
	fourMoveBoard[1][2][3] = 2
	fourMoveBoard[0][1][2] = 2
	# plane is z = 0
	onePlaneFull = [[[1 if (k%4 == 0) 0 else for i in range(4)] for j in range(4)] for k in range(4)]

	def test_clearBoard(self):
		test1 = Board()
		self.assertEqual(test1.b,openBoard)

		self.assertEqual(test1.clearBoard(), 0)
		self.assertEqual(test1.b,openBoard)

		test1.move(1,0,0,0)
		test1.move(2,0,0,1)
		test1.move(2,0,0,2)
		self.assertEqual(test1.clearBoard(), 3)
		self.assertEqual(test1.b,openBoard)

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
		self.assertEqual(otherNumber(1),2)
		self.assertEqual(otherNumber(2),1)
		self.assertEqual(otherNumber(0),0)
		self.assertEqual(otherNumber(4),0)

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
		test2 = [[[0 for i in range(4)] for j in range(4)] for k in range(4)]
		self.assertEqual(test1.b,test2)

		self.assertEqual(test1.move(1,0,0,0),True)
		self.assertEqual(test1.move(2,0,0,1),True)
		self.assertEqual(test1.move(2,1,0,2),True)
		self.assertEqual(test1.move(2,0,0,0),False)
		self.assertEqual(test1.move(2,1,0,2),False)

		test2[0][0][0] = 1
		test2[0][0][1] = 2
		test2[1][0][2] = 2

		self.assertEqual(test1.b,test2)

	def test_findLines(self):

	def test_lineToPoints(self):

	def test_pointsToLine(self):

	def test_lineToValues(self):

	def test_findForces(self):

	def test_linesForPoint(self):

	def test_openLinesForPoint(self):



if __name__ == '__main__':
    unittest.main()






		