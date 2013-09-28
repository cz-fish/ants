#!/usr/bin/env python

from Player import *
from Cards import *
from Game import *
from CLI import *
import random

if __name__ == '__main__':
	random.seed()
	players = [HumanPlayer(), RandomAIPlayer()]
	game = Game(players, cards_traditional)

	ui = Cli(players, game)
	ui.playGame()

