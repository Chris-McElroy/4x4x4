from Brain import *
import unittest

class boardTest(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()






