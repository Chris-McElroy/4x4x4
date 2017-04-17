from Board import *
import unittest

class boardTest(unittest.TestCase):

	def test_clearBoard(self):
		test1 = Board()
		test2 = [[[0 for i in range(4)] for j in range(4)] for k in range(4)]
		self.assertEqual(test1.b,test2)

		self.assertEqual(test1.clearBoard(), 0)
		self.assertEqual(test1.b,test2)

		test1.move(1,0,0,0)
		test1.move(2,0,0,1)
		test1.move(2,0,0,2)
		self.assertEqual(test1.clearBoard(), 3)
		self.assertEqual(test1.b,test2)

	def test_move(self):
		return True

if __name__ == '__main__':
    unittest.main()
		