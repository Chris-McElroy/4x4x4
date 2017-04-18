from Brain import *
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
	

if __name__ == '__main__':
    unittest.main()






		