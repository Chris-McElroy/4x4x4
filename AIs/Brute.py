import pygame
import random

class Brute:
	""" moves into wins, out of check, and then in an open point """

	def __init__(self):
		""" Stores player info for easy access """
		self.undecided = False

	def move(self,board,n,display):
		"""
		The main function for this class.  Returns the point the person wants to move in.
		"""
		wins = board.findLines(n,3)
		if len(wins) > 0:
			for winLine in wins:
				for point in board.lineToPoints(winLine):
					if board.pointToValue(point) == 0:
						return point

		badChecks = board.findLines(board.otherNumber(n),3)
		if len(badChecks) > 0:
			for bC in badChecks:
				for point in board.lineToPoints(bC):
					if board.pointToValue(point) == 0:
						return point

		openPoints = board.getOpenPoints()
		return self.chooseMove(openPoints)


		
	def chooseMove(self,moves):
		"""
		chooses a move from the available one in the determined tiebreaking way
		Currently: Random
		"""

		return random.choice(list(moves))