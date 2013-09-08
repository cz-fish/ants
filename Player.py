import random

# a general player
class Player:
	# resources
	bricks = 0
	arms = 0
	crystals = 0
	architects = 0
	soldiers = 0
	mages = 0
	# castle
	castle = 0
	wall = 0
	# number of turns already played
	turn = 0
	# list of cards in the hand
	cards = []
	# for each card, info whether it is playable (updated every turn)
	playable = []
	# number of wins
	wins = 0

	def newGame(self):
		self.bricks = 5
		self.arms = 5
		self.crystals = 5
		self.architects = 2
		self.soldiers = 2
		self.mages = 2

		self.castle = 30
		self.wall = 10

		self.cards = [0 for i in range(8)]
		self.playable = [0 for i in range(8)]
		self.turn = 0

# player actions
TURN_DISPOSE = 0
TURN_PLAY = 1

# human player, whose actions will be obtained another way (from the console, from gui, etc.)
class HumanPlayer(Player):
	def isHuman(self):
		return 1

# an AI player which plays a random playable card each turn
class RandomAIPlayer(Player):
	def isHuman(self):
		return 0
	
	def getNextAction(self):
		if sum(self.playable) == 0:
			# there's no card to play, dispose one
			return (TURN_DISPOSE, random.choice(range(len(self.cards))))
		options = filter(lambda x: x[1] == 1, zip(range(len(self.cards)), self.playable))
		return (TURN_PLAY, random.choice(options)[0])


