import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

class Human:
	""" functions as the player for a real life person """

	def __init__(self, currentBoard, playerNumber):
		""" Stores player info for easy access """
		self.n = playerNumber

	def move(self,board,n,display):
		"""
		The main function for this class.  Returns the point the person wants to move in.
		"""

		self.n = n
		numMoves = board.numMoves(self.n)[0]

		# if numMoves < 4:
		# 	#moves = [[1,2,1],[2,1,1],[3,1,2],[2,0,1],[3,3,3],[3,3,3]]
		# 	moves = [[1,2,1],[2,2,1],[3,2,1],[2,1,2],[3,3,3],[3,3,3]]
		# 	return moves[numMoves]
		
		goodInput = False

		chosenPoint = display.mostRecentClick
		enter = input("enter 'y' to confirm move")
		if enter == "y":
			return chosenPoint


		while(not goodInput):
			chosenPointTogether = input("Where do you want to move?\n(Enter the numbers (from 1-4) together: xyz)\n>>> ")
			chosenPoint = [0,0,0]
			goodInput = True

			for i in range(3):
				if (chosenPointTogether%10 - 1 in range(4)):
					chosenPoint[2-i] = chosenPointTogether%10-1
					chosenPointTogether = chosenPointTogether/10
				else:
					print "\nBad input, try again!"
					goodInput = False

			if chosenPoint not in board.openPoints() and goodInput:
				print "\nBad input, try again!"
				goodInput = False

		return chosenPoint














