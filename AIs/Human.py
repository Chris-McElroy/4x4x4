import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import time

class Human:
	""" functions as the player for a real life person """

	def __init__(self, currentBoard, playerNumber):
		""" Stores player info for easy access """
		self.n = playerNumber
		print "Double click to move!"

	def move(self,board,n,display):
		"""
		The main function for this class.  Returns the point the person wants to move in.
		"""

		move = False
		goodInput = False

		while not goodInput:
			pygame.time.wait(10)

			display.displayBoard()
			move = display.getMove()

			if move in board.openPoints():
				goodInput = True
			elif move:
				print "Bad input, try again!"

		return move












