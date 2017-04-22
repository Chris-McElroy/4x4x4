class Display:
	""" Displays the board """

	#constructor	
	def __init__(self, board):
		""" is given the board (object of class board) """
		self.b = board

	def displayShittyBoard(self):
		""" displays the board reallllyy shitty """
		for l in range(16):
			values = self.b.lineToValues(l)
			lineString = ""
			for v in values:
				lineString += str(v) + " "
			print lineString
			if (l%4 == 3):
				print ""

	def updateBoard(self,board):
		self.b = board
