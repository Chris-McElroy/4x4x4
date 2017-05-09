import pygame

class Human:
	""" functions as the player for a real life person """

	def __init__(self):
		""" Stores player info for easy access """

	def move(self,board,n,display):
		"""
		The main function for this class.  Returns the point the person wants to move in.
		"""

		move = False
		goodInput = False
		n = 0

		while not goodInput:
			pygame.time.wait(10)

			display.displayProgress("lol: ",n%100)
			display.displayBoard()
			move = display.getMove()

			if move and tuple(move) in board.getOpenPoints():
				goodInput = True
			elif move:
				print "Bad input, try again!"

			n+= 1

		return move











