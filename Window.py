import sys
import pygame
from pygame.locals import *
from Painter import Painter
from Animation import Animation
from Player import *
from Game import *

SCR_WIDTH = 800
SCR_HEIGHT = 400
FPS = 30
pygame.init()
GAME_CLOCK = pygame.time.Clock()

class Window:
    def __init__(self, players, game):
        self.players = players
        self.game = game
        self.waitingForHuman = False
        self.disposing = False

        self.surface = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT), 0, 32)
        pygame.display.set_caption('Ants')
        self.painter = Painter(self.surface, self.game)
        self.anim = Animation(self.painter)

    def playGame(self):
        self.startGame()
        while not self.checkEvents():
            self.anim.tick()
            self.painter.drawScreen(self.players, self.disposing)
            pygame.display.update()
            GAME_CLOCK.tick(FPS)

    def startGame(self):
        self.finished = False
        self.currentPlayer = 0
        p = self.players[self.currentPlayer]
        self.painter.updateDisplayedCards(p)
        self.anim.start_game(self.nextTurn)

    def nextTurn(self):
        p = self.players[self.currentPlayer]
        self.game.nextTurn(self.currentPlayer)
        self.painter.updateDisplayedCards(p)

        if p.isHuman():
            self.waitingForHuman = True
        else:
            self.anim.ai_thinking(self.nextAiAction)

    def nextAiAction(self):
        p = self.players[self.currentPlayer]
        action = p.getNextAction()
        self.anim.animate_move(action, self.moveAnimationFinished)


    def moveAnimationFinished(self, action):
        # apply the actual action of the move
        if action[0] == TURN_PLAY:
            res = self.game.playCard(self.currentPlayer, action[1])
            if res == PLAY_ERROR:
                # FIXME: display on screen
                print "Error! an unplayable card was played"
                sys.exit(1)
            elif res == PLAY_WIN:
                # FIXME: display on screen
                print "Player %d wins!" % (self.currentPlayer+1)
                self.finished = True
        else:
            self.game.passCard(self.currentPlayer, action[1])

        self.anim.wait_before_next_turn(self.doneWaiting)

    def doneWaiting(self):
        if not self.finished:
            self.currentPlayer = -self.currentPlayer + 1
            self.nextTurn()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            if event.type == KEYUP:
                if event.key == K_ESCAPE: # pressing escape quits
                    return True
                #return event.key
            if event.type == MOUSEBUTTONDOWN:
                self.mouseClick(event.pos)
        return False

    def mouseClick(self, pos):
        if not self.waitingForHuman:
            return

        if self.positionInsideRect(pos, self.painter.discard_rect):
            self.disposing = not self.disposing
            return
        
        clickedCard = self.findCardOnPos(pos)
        if clickedCard is None:
            return

        if not self.disposing and not self.players[self.currentPlayer].playable[clickedCard]:
            # attempt to play a non-playable card
            return
        action = ([TURN_PLAY, TURN_DISPOSE][self.disposing], clickedCard)
        self.waitingForHuman = False
        self.disposing = False
        self.anim.animate_move(action, self.moveAnimationFinished)

    def positionInsideRect(self, position, rect):
        return position[0] >= rect[0] \
               and position[0] <= rect[0] + rect[2] \
               and position[1] >= rect[1] \
               and position[1] <= rect[1] + rect[3]

    def findCardOnPos(self, position):
        for i in range(8):
            if self.positionInsideRect(position, self.painter.card_rect(i)):
                return i
        return None


