from Board import *
from Display import *
from AIs.Vaapad import *
from AIs.weakVaapad import *
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
		self.AIList = [None,Vaapad,Human,Wildfire,Brute]

	def main(self):
		""" Main controller of everything, likeyado """

		displayOn = True
		self.d = Display(self.b,self.AIList,[None, None, None])

		while displayOn:

			players = self.d.mainMenu()

			currentSet = True
			while currentSet:
				self.playGame(players)

				inExit = True
				while inExit:
					choice = self.d.playAgain()

					if choice == "Play Again":
						inExit = False
						# tally up who won and display that somehow

					elif choice == "Switch Players":
						inExit = False
						currentSet = False

					elif choice == "View Replay":
						self.viewReplay(players)

					elif choice == "Quit":
						inExit, currentSet, displayOn = (False,)*3

		pygame.quit()
		quit(0)

	def presetBoard(self, players):
		self.b = Board()
		self.d = Display(self.b,self.AIList,players)
		self.d.initializeBoard()
		continueGame = True
		self.forced = False
		self.n = 1

		while (continueGame) and self.d.preset:
			titleText = "Player " + str(self.n) + "'s Turn"
			self.d.changeTitleText(titleText)
			self.d.displayProgress("",0)

			if self.forced:
				self.d.checkPoint(self.b.otherNumber(self.n))

			self.d.updateBoard(self.b)

			for i in range(10):
				self.d.displayBoard()
				pygame.time.wait(10)

			if not self.d.preset:
				break

			nextMove = players[0].move(self.b, self.n, self.d)

			if not self.d.preset:
				break

			noProblem = self.b.move(self.n,nextMove)

			if not noProblem:
				print "move", nextMove, "failed for player", self.n
				break

			continueGame = self.checkBoard(nextMove)

			self.n = self.b.otherNumber(self.n)

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


		if players[0]:
			self.presetBoard(players)

		while (continueGame):
			titleText = "Player " + str(self.n) + "'s Turn"
			self.d.changeTitleText(titleText)
			self.d.displayProgress("",0)

			if self.forced:
				self.d.checkPoint(self.b.otherNumber(self.n))

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

	def viewReplay(self, players):
			"""
			starts game between players 1 and 2
			players holds both players, whether AI or real
			player 1 is X's, player 2 is O's
			"""

			self.fakeB = Board()
			self.fakeB.copyAll(self.b)
			moveList = self.b.moveList
			self.d = Display(self.fakeB,self.AIList,players)
			self.d.initializeBoard()
			self.d.displayProgress("",0)
			self.forced = False
			self.n = 1

			moveNumber = len(moveList) - 1
			self.checkBoardForReplay(moveList[moveNumber][0])

			while (moveNumber < len(moveList)) and moveNumber >= -1:
				self.d.displayReplayBoard()
				pygame.time.wait(10)

				direction = self.d.checkReplayControl()

				if direction != 0:
					currentMove = None
					if direction == 1:
						moveNumber += 1
						if moveNumber < len(moveList):
							currentMove = moveList[moveNumber][0]
							self.n = moveList[moveNumber][1]					
							self.fakeB.move(self.n, currentMove)
					elif direction == -1:
						if moveNumber >= 0:
							currentMove = moveList[moveNumber][0]
							self.n = self.b.otherNumber(moveList[moveNumber][1])
							self.fakeB.clearPoint(currentMove)
						moveNumber -= 1

					self.d.updateBoard(self.fakeB)
					if moveNumber in range(len(moveList)):
						self.checkBoardForReplay(currentMove)

	def checkBoardForReplay(self,move):
		""" check board for wins and checks after a replayed move """
		numMoves = 64 - len(self.fakeB.openPoints())
		wins = self.fakeB.openLinesForPoint(self.n,move,4)
		checkMate = self.checkCheckmates(True)
		checks = self.fakeB.findLines(self.n,3)

		if len(wins) > 0:
			self.forced = False
			self.d.changeTitleText("Player " + str(self.n) + " Wins! They got 4 in a row!")
			self.d.setWinningMove(move)
			self.d.setFlashLines(wins)

		elif checkMate:
			self.forced = False
			self.d.changeTitleText("Player " + str(self.n) + " Wins! They got checkmate!")
			self.d.setWinningMove(move)

		else:
			self.forced = False
			self.d.setWinningMove([])
			self.d.changeTitleText("Player " + str(self.b.otherNumber(self.n)) + "'s Turn")

			if len(checks) > 0:
				self.d.setFlashLines(checks)
				self.forced = True
				self.d.checkPoint(self.n)

		if numMoves == 64:
			self.d.changeTitleText("Wow! You filled the board!")

	def checkBoard(self,move):
		""" check board for wins and checks after a move """

		continueGame = True # can be assumed given that we got here

		numMoves = 64 - len(self.b.openPoints())
		wins = self.b.openLinesForPoint(self.n,move,4)
		checkMate = self.checkCheckmates(False)
		checks = self.b.findLines(self.n,3)

		if len(wins) > 0:
			continueGame = False
			self.forced = False
			self.d.displayProgress("",0)
			self.d.changeTitleText("Player " + str(self.n) + " Wins! They got 4 in a row!")
			self.d.setWinningMove(move)
			self.d.setFlashLines(wins)
			self.d.updateBoard(self.b)

			i = 0
			while i < 17+36:
				self.d.displayBoard()
				pygame.time.wait(10)
				i += 1 # WHOOOPS FORGOT THIS

		elif checkMate:
			self.forced = False
			continueGame = False
			self.d.displayProgress("",0)
			self.d.changeTitleText("Player " + str(self.n) + " Wins! They got checkmate!")
			self.d.setWinningMove(move)
			self.d.updateBoard(self.b)

			i = 0
			while i < 17+36:
				self.d.displayBoard()
				pygame.time.wait(10)
				i += 1 # WHOOOPS FORGOT THIS

		elif len(checks) > 0:
			self.d.setFlashLines(checks)
			self.d.checkPoint(self.n)
			self.forced = True

		else:
			self.forced = False
			self.d.setFlashLines([])

		if numMoves == 64:
			continueGame = False
			self.d.displayProgress("",0)
			self.d.changeTitleText("Wow! You filled the board!")
			self.d.updateBoard(self.b)

			i = 0
			while i < 17+36:
				self.d.displayBoard()
				pygame.time.wait(10)
				i += 1 # WHOOOPS FORGOT THIS

		return continueGame

	def checkCheckmates(self,fake):
		""" check board for checkmates after a move """

		checkMate = False
		checkLines = []
		board = self.b
		if fake:
			board = self.fakeB

		points = board.myPoints(self.n)

		for p in points:
			checks = board.openLinesForPoint(self.n,p,3)
			if len(checks) > 1:
				checkMate = True
				checkLines += checks

		self.d.setFlashLines(checkLines)
		return checkMate

tryTo = Master()

tryTo.main()

# tryTo.d = Display(tryTo.b)
# player1 = Wildfire()
# player2 = Wildfire()
# tryTo.playGame([None,player1,player2],1)




