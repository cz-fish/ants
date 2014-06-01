import sys
import pygame
from pygame.locals import *
from Painter import Painter

SCR_WIDTH = 800
SCR_HEIGHT = 400
FPS = 30
pygame.init()
GAME_CLOCK = pygame.time.Clock()

class Window:
    def __init__(self, players, game):
        self.players = players
        self.game = game

        self.surface = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT), 0, 32)
        pygame.display.set_caption('Ants')
        self.painter = Painter(self.surface, self.game)

    def playGame(self):
        while not self.checkEvents():
            self.painter.drawScreen(self.players)
            pygame.display.update()
            GAME_CLOCK.tick(FPS)

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            if event.type == KEYUP:
                if event.key == K_ESCAPE: # pressing escape quits
                    return True
                #return event.key
        return False

