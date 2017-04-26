class Human:
	""" functions as the player for a real life person """

	def __init__(self, currentBoard, playerNumber):
		""" Stores player info for easy access """
		self.n = playerNumber

	def move(self,board,n):
		"""
		The main function for this class.  Returns the point the person wants to move in.
		"""

		goodInput = False

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