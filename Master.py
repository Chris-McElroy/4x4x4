from Board import *
from Display import *
from AIs.Vaapad import *
from AIs.Wildfire import *
from AIs.Human import *
from AIs.Brute import *
import time

class Master:
	""" controls everything going on """

	#constructor	
	def __init__(self):
		""" Creates display and initial menu """
		self.b = Board()
		self.d = None
		self.n = 0
		self.forced = False
		self.wins = [0,0]
		self.AIList = [None,Human,Wildfire,Vaapad,Brute]

	def main(self):
		""" yano it does some shit """

		displayOn = True
		self.d = Display(self.b,self.AIList,[None, None, None])

		while displayOn:

			players = self.d.mainMenu()

			# setsN = raw_input("First to what?")
			
			# p1 = raw_input("Who plays first?")

			currentSet = True
			while currentSet:
				self.playGame(players)
				choice = self.d.playAgain()
				if choice == "Play Again":
					5
					# tally up who won and display that somehow

				if choice == "Switch Players":
					currentSet = False

				if choice == "View Replay":
					self.viewReplay(players, self.b.moveList)
					currentSet = False


				if choice == "Quit":
					currentSet = False
					displayOn = False

		pygame.quit()
		quit(0)

	def playGame(self, players):
		"""
		starts game between players 1 and 2
		players holds both players, whether AI or real
		player 1 is X's, player 2 is O's
		"""

		self.b = Board()
		self.d = Display(self.b,self.AIList,players)
		self.d.initializeBoard()
		continueGame = True
		self.forced = False
		self.n = 1

		while (continueGame):
			titleText = "Player " + str(self.n) + "'s Turn"
			if self.forced:
				titleText += " (forced)"
			self.d.title(titleText)

			self.d.updateBoard(self.b)

			i = 0
			while i < 10:
				self.d.displayBoard()
				pygame.time.wait(10)
				i += 1 # WHOOOPS FORGOT THIS

			nextMove = players[self.n].move(self.b, self.n, self.d)
			noProblem = self.b.move(self.n,nextMove)

			if not noProblem:
				print "move", nextMove, "failed for player", self.n
				break

			continueGame = self.checkBoard(nextMove)

			self.n = self.b.otherNumber(self.n)

	def viewReplay(self, players, moveList):
			"""
			starts game between players 1 and 2
			players holds both players, whether AI or real
			player 1 is X's, player 2 is O's
			"""

			self.b = Board()
			self.d = Display(self.b,self.AIList,players)
			self.d.initializeBoard()
			self.forced = False
			self.n = 1

			moveNumber = 0

			while (moveNumber < len(moveList)):
				titleText = "Player " + str(self.n) + "'s Turn"
				if self.forced:
					titleText += " (forced)"
				self.d.title(titleText)

				self.d.updateBoard(self.b)

				i = 0

				self.d.displayBoard()


				direction = self.d.checkReplayControl()

				currentMove = None
				if direction == 1:
					currentMove = moveList[moveNumber][0]
					self.n = moveList[moveNumber][1]					
					self.b.move(self.n, currentMove)
					moveNumber += 1
				elif direction == -1 and moveNumber > 0:
					moveNumber -= 1
					currentMove = moveList[moveNumber][0]
					self.n = moveList[moveNumber][1]					
					self.b.clearPoint(currentMove)
				

				if (currentMove):
					self.checkBoard(currentMove)


	def checkBoard(self,move):
		""" check board for wins and checks after a move """

		continueGame = True # can be assumed given that we got here

		wins = len(self.b.openLinesForPoint(self.n,move,4))
		checkMate = self.checkCheckmates(move)
		checks = self.b.findLines(self.n,3)

		if wins > 0:
			continueGame = False
			self.d.title("Player " + str(self.n) + " Wins! They got 4 in a row!")
			self.d.setWinningMove(move)
			self.d.updateBoard(self.b)

			i = 0
			while i < 17+36:
				self.d.displayBoard()
				pygame.time.wait(10)
				i += 1 # WHOOOPS FORGOT THIS

		elif checkMate:
			continueGame = False
			self.d.title("Player " + str(self.n) + " Wins! They got checkmate!")
			self.d.setWinningMove(move)
			self.d.updateBoard(self.b)

			i = 0
			while i < 17+36:
				self.d.displayBoard()
				pygame.time.wait(10)
				i += 1 # WHOOOPS FORGOT THIS

		elif len(checks) > 0:
			checkPoints = self.b.lineToPoints(next(iter(checks)))
			checkString = ""
			for point in checkPoints:
				if self.b.pointToValue(point) == 0:
					self.d.checkPoint(point)
					checkString = self.pointToString(point)
					self.forced = True
			self.d.title("Check! Player " + str(self.b.otherNumber(self.n)) + " must respond at " + checkString + "!				")
			self.d.updateBoard(self.b)

		else:
			self.d.uncheckPoint()
			self.forced = False

		return continueGame

	def pointToString(self, p):
		""" turns a point into a string of numbers that should be inputed """
		string = ""
		for n in p:
			string += str(1+n)
		return string

	def checkCheckmates(self,move):
		""" check board for checkmates after a move """

		checkMate = False
		points = self.b.myPoints(self.n)

		for p in points:
			checks = self.b.openLinesForPoint(self.n,p,3)
			if len(checks) > 1:
				checkMate = True

		return checkMate

tryTo = Master()

tryTo.main()

# tryTo.d = Display(tryTo.b)
# player1 = Wildfire()
# player2 = Wildfire()
# tryTo.playGame([None,player1,player2],1)






