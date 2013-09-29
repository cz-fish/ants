#!/usr/bin/env python

from Player import *
from Cards import *
from Game import *
from CLI import Cli
from Window import Window
import random

if __name__ == '__main__':
	random.seed()
	players = [HumanPlayer(), RandomAIPlayer()]
	game = Game(players, cards_traditional)

	#ui = Cli(players, game)
	ui = Window(players, game)
	ui.playGame()

