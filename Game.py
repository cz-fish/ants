#from Player import *
from Cards import *
import random

# responses of the playCard method
PLAY_ERROR = 0
PLAY_OK = 1
PLAY_WIN = 2

# variants of probability list initialization
VAR_UNDEF = -1
VAR_BEGINNING = 0
VAR_ADVANCED = 1
VAR_ALL = 2
VAR_END = 3

class Game:
	def __init__(self, players, cards):
		self.players = players
		self.cards = cards
		self.probVariant = VAR_UNDEF
		self.initProbabilityLists(VAR_BEGINNING)
		for p in self.players:
			p.newGame()
			self.dealCards(p)
		
	def initProbabilityLists(self, variant):
		# initializes list of cards with unequal probability based on
		# card levels and given game variant
		if self.probVariant == variant:
			return
		if not variant in [VAR_BEGINNING, VAR_ADVANCED, VAR_ALL, VAR_END]:
			# error
			raise ValueError()
		self.cardlist = []
		for c in self.cards:
			if variant == VAR_BEGINNING:
				# strongly prefer level 1 cards
				if c[C_LEVEL] == 1:
					self.cardlist += [c] * 6
				elif c[C_LEVEL] == 2:
					self.cardlist += [c] * 3
				else:
					self.cardlist += [c]
			elif variant == VAR_ADVANCED:
				# linear levels, prefer lower
				self.cardlist += [c] * (4-c[C_LEVEL])
			elif variant == VAR_ALL:
				# all cards with equal probabilities
				self.cardlist += [c]
			elif variant == VAR_END:
				# linear levels, prefer higher
				self.cardlist += [c] * c[C_LEVEL]
		random.shuffle(self.cardlist)
		self.probVariant = variant

	def playCard(self, player, card):
		p = self.players[player]
		if player == 0:
			ot = self.players[1]
		else:
			ot = self.players[0]
		c = p.cards[card]
		# check that the player has enough resources
		if not p.playable[card]:
			return PLAY_ERROR
		# play the card
		p.bricks -= c[C_COST][0]
		p.arms -= c[C_COST][1]
		p.crystals -= c[C_COST][2]
		
		p.bricks += c[C_GAIN][0]
		p.arms += c[C_GAIN][1]
		p.crystals += c[C_GAIN][2]
		p.architects += c[C_GAIN][3]
		p.soldiers += c[C_GAIN][4]
		p.mages += c[C_GAIN][5]

		ot.bricks -= c[C_LOSE][0]
		ot.arms -= c[C_LOSE][1]
		ot.crystals -= c[C_LOSE][2]
		ot.architects -= c[C_LOSE][3]
		ot.soldiers -= c[C_LOSE][4]
		ot.mages -= c[C_LOSE][5]

		p.castle += c[C_BUILD][0]
		p.wall += c[C_BUILD][1]

		ot.castle -= c[C_DESTROY][1]
		ot.wall -= c[C_DESTROY][2]
		if c[C_DESTROY][0] > ot.wall:
			ot.castle -= c[C_DESTROY][0] - ot.wall
			ot.wall = 0
		else:
			ot.wall -= c[C_DESTROY][0]

		if p.wall < 0: p.wall = 0
		if ot.bricks < 0: ot.bricks = 0
		if ot.arms < 0: ot.arms = 0
		if ot.crystals < 0: ot.crystals = 0
		if ot.architects < 1: ot.architects = 1
		if ot.soldiers < 1: ot.soldiers = 1
		if ot.mages < 1: ot.mages = 1
		if ot.castle < 0: ot.castle = 0
		# check whether the player has won
		if p.castle >= 100 or ot.castle == 0:
			p.wins += 1
			return PLAY_WIN
		# give the player a new card
		self.giveCard(p, card)
		return PLAY_OK

	def passCard(self, player, card):
		p = self.players[player]
		self.giveCard(p, card)

	def dealCards(self, player):
		for i in range(8):
			self.giveCard(player, i)
	
	def giveCard(self, player, card):
		player.cards[card] = random.choice(self.cardlist)
	
	def nextTurn(self, player):
		p = self.players[player]
		if p.turn != 0:
			p.bricks += p.architects
			p.arms += p.soldiers
			p.crystals += p.mages
		p.turn += 1
		# update playable info
		for i in range(len(p.cards)):
			c = p.cards[i]
			if p.bricks < c[C_COST][0] or \
			   p.arms < c[C_COST][1] or \
			   p.crystals < c[C_COST][2]:
				p.playable[i] = 0
			else:
				p.playable[i] = 1
		# change cards' probabilities as the game advances
		if p.turn == 8:
			self.initProbabilityLists(VAR_ADVANCED)
		elif p.turn == 30:
			self.initProbabilityLists(VAR_ALL)
		#elif p.turn == 60:
		#	self.initProbabilityLists(VAR_END)
	

