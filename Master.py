from Board import *
from Display import *
from Brain import *
import time

class Master:
	""" controls everything going on """

	#constructor	
	def __init__(self):
		""" Creates display and initial menu """
		# nothing much to do here yet until display is better
		self.b = Board()
		self.d = Display(self.b)

	def playGame(self, players, p1):
		"""
		starts game between players 1 and 2
		players holds both players, whether AI or real
		player 1 is X's, player 2 is O's
		p1 holds which player will play first
		"""

		self.b.clearBoard()
		continueGame = True
		n = p1

		while (continueGame):

			print "Player " + str(n) + "'s Turn:"

			self.d.updateBoard(self.b)
			self.d.displayShittyBoard()

			nextMove = players[n-1].move(self.b, n)
			self.b.move(n,nextMove)

			wins = len(self.b.findLines(n,4))
			checks = len(self.b.findLines(n,3))

			if (wins > 0 or checks > 1):
				continueGame = False

				print "Player " + str(n) + " Wins!"
				self.d.updateBoard(self.b)
				self.d.displayShittyBoard()

			if (checks == 1):
				print "Check! Player " + str(self.b.otherNumber(n)) + " must respond! \n"
			#n = self.b.otherNumber(n)
			n = 1 if (n == 2) else 2

			time.sleep(1)


		print "Game Over \n"


