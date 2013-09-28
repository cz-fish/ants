# Command line interface of Ants
from Player import *
from Cards import *
from Game import *
import sys

def print_card(card, verbose):
	str = card[C_NAME] + " ("
	if verbose: str += "costs "
	if card[C_COST][0]:
		str += "%d bricks " % card[C_COST][0]
	if card[C_COST][1]:
		str += "%d arms " % card[C_COST][1]
	if card[C_COST][2]:
		str += "%d crystals " % card[C_COST][2]
	str += ") "
	if filter(lambda x: x != 0, card[C_GAIN]):
		if verbose: str += "you gain "
		else: str += "you "
		if card[C_GAIN][0]:
			str += "%d bricks " % card[C_GAIN][0]
		if card[C_GAIN][1]:
			str += "%d arms " % card[C_GAIN][1]
		if card[C_GAIN][2]:
			str += "%d crystals " % card[C_GAIN][2]
		if card[C_GAIN][3]:
			str += "%d architects " % card[C_GAIN][3]
		if card[C_GAIN][4]:
			str += "%d soldiers " % card[C_GAIN][4]
		if card[C_GAIN][5]:
			str += "%d mages " % card[C_GAIN][5]
		str += ", "
	if filter(lambda x: x != 0, card[C_LOSE]):
		if verbose: str += "oponent loses "
		else: str += "opo "
		if card[C_LOSE][0]:
			str += "-%d bricks " % card[C_LOSE][0]
		if card[C_LOSE][1]:
			str += "-%d arms " % card[C_LOSE][1]
		if card[C_LOSE][2]:
			str += "-%d crystals " % card[C_LOSE][2]
		if card[C_LOSE][3]:
			str += "-%d architects " % card[C_LOSE][3]
		if card[C_LOSE][4]:
			str += "-%d soldiers " % card[C_LOSE][4]
		if card[C_LOSE][5]:
			str += "-%d mages " % card[C_LOSE][5]
		str += ", "
	if filter(lambda x: x != 0, card[C_BUILD]):
		if verbose: str += "you build "
		else: str += "you "
		if card[C_BUILD][0]:
			str += "%d castle " % card[C_BUILD][0]
		if card[C_BUILD][1]:
			str += "%d wall " % card[C_BUILD][1]
		str += ", "
	if filter(lambda x: x != 0, card[C_DESTROY]):
		if verbose: str += "oponent's damage "
		else: str += "dmg "
		if card[C_DESTROY][0]:
			str += "%d " % card[C_DESTROY][0]
		if card[C_DESTROY][1]:
			str += "%d direct castle " % card[C_DESTROY][1]
		if card[C_DESTROY][2]:
			str += "%d direct wall" % card[C_DESTROY][2]
		str += ", "
	str = str[:-2]
	print str

def print_cards(cards, playable=[]):
	i = 1
	if playable:
		# print cards, hilite playable
		for cp in zip(cards, playable):
			print str(i) + " " + [". ", "+ "][cp[1]],
			print_card(cp[0], 0)
			i += 1
	else:
		# print all cards the same
		for c in cards:
			print str(i) + " " + print_card(c, 0)
			i += 1

class Cli:
	def __init__(self, players, game):
		self.players = players
		self.game = game
	
	def playGame(self):
		done = 0
		while not done:
			for i in [0, 1]:
				p = self.players[i]
				self.game.nextTurn(i)
				if p.isHuman():
					if i == 0:
						op = self.players[1]
					else:
						op = self.players[0]
					while 1:
						print "--------------------------------------"
						print "Turn %d" % (p.turn)
						print "     Brick  Arms Cryst  Arch  Sold Mages   Castle Wall"
						print "You  %5d %5d %5d %5d %5d %5d   %6d %4d" % (p.bricks, p.arms, p.crystals,\
							p.architects, p.soldiers, p.mages, p.castle, p.wall)
						print "Opo  %5d %5d %5d %5d %5d %5d   %6d %4d" % (op.bricks, op.arms, op.crystals,\
							op.architects, op.soldiers, op.mages, op.castle, op.wall)
						print "----------"
						print_cards(p.cards, p.playable)
						print "----------"
						again = 0
						while 1:
							print "Your turn (Px - play x-th card, Dx - dispose x-th card, I - info again, Q - quit)"
							l = sys.stdin.readline()
							if len(l) < 1:
								continue
							if l[0] in ['P','p']:
								try:
									card = int(l[1:])
								except ValueError:
									continue
								if card < 1 or card > 8: continue
								if not p.playable[card-1]: continue
								act = TURN_PLAY
							elif l[0] in ['D','d']:
								try:
									card = int(l[1:])
								except ValueError:
									continue
								if card < 1 or card > 8: continue
								act = TURN_DISPOSE
							elif l[0] in ['I','i']:
								again = 1
							elif l[0] in ['Q','q']:
								sys.exit(0)
							else:
								continue
							break
						if again:
							continue
						action = (act, card-1)
						break
				else:
					action = p.getNextAction()
				if action[0] == TURN_PLAY:
					print "Player %d played: %s" % (i+1, p.cards[action[1]][C_NAME])
					res = self.game.playCard(i, action[1])
					if res == PLAY_ERROR:
						print "Error! an unplayable card was played"
						sys.exit(1)
					elif res == PLAY_WIN:
						print "Player %d wins!" % (i+1)
						done = 1
						break
				else:
					print "Player %d disposed: %s" % (i+1, p.cards[action[1]][C_NAME])
					self.game.passCard(i, action[1])
					

