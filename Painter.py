import pygame
from math import pi
import Cards
from Bitmaps import Bitmaps
from Sprites import Sprites

# TODO: unite colors of resources:
#   school/brick - red
#   soldier/arms - green
#   mages/crystals - blue

# TODO: perhaps don't draw anything at all if the scene is completely the same as previous frame

class Painter:
    def __init__(self, surface, game):
        self.surface = surface
        self.game = game
        self.STATS_WIDTH = 168
        self.STATS_HEIGHT = 250
        self.CARD_WIDTH = 100
        self.CARD_HEIGHT = 150

        self.font = pygame.font.SysFont(None, 20)
        
        self.bmp = Bitmaps()
        self.sprites = Sprites(self.bmp, self.game.cards, self.CARD_WIDTH, self.CARD_HEIGHT)


    def drawScreen(self, players):
        """Draws the entire screen"""
        self.drawBackground()
        self.drawStats(players[0], True)
        self.drawStats(players[1], False)
        self.drawAnthills(players[0].castle, players[0].wall, players[1].castle, players[1].wall)
        #FIXME
        hand = players[0].cards
        enabled = players[0].playable
        blind = False

        self.drawCards([(hand[i], enabled[i]) for i in range(len(hand))], blind)

    def drawBackground(self):
        """Draws the window background and controls (dispose button)"""
        w = self.surface.get_width()
        h = self.surface.get_height()
        self.surface.fill((50,50,220), pygame.Rect((0,0,w,h/2)))
        self.surface.fill((60,150,60), pygame.Rect((0,h/2,w,h)))

    def drawStats(self, player, left):
        """Draws game stats/info for one player
           stats - player stats/info
           left - align to the left of the screen (True) or to the right (False)"""
        mx = self.STATS_WIDTH
        my = self.STATS_HEIGHT
        x = [self.surface.get_width() - mx, 0][left]
        base = pygame.Surface((mx, my))
        base.fill((210,210,210))
        pygame.draw.polygon(base,
            (170,170,170),
            [(0,0), (0,my), (3, my-3), (3,3), (mx - 3, 3), (mx, 0)],
            0)
        pygame.draw.polygon(base,
            (240,240,240),
            [(0,my), (3,my-3), (mx-3, my-3),(mx-3,3), (mx, 0), (mx, my)],
            0)

        #FIXME: player names, colors and overall scores
        name = 'Player ' + ['2', '1'][left]
        text = self.font.render(name, 1, (0,0,0))
        base.blit(text, (10, 5))
        
        base.blit(self.bmp['stats_castle'], (7, 20))
        base.blit(self.bmp['stats_wall'], (85, 20))
        base.blit(self.bmp['rsrc_architect'], (7, 83))
        base.blit(self.bmp['rsrc_soldier'], (7, 136))
        base.blit(self.bmp['rsrc_mage'], (7, 189))
        base.blit(self.bmp['rsrc_brick'], (85, 83))
        base.blit(self.bmp['rsrc_arm'], (85, 136))
        base.blit(self.bmp['rsrc_crystal'], (85, 189))

        text = self.font.render(str(player.castle), 1, (0,0,0))
        base.blit(text, (58, 40))
        text = self.font.render(str(player.wall), 1, (0,0,0))
        base.blit(text, (136, 40))
        text = self.font.render(str(player.architects), 1, (0,0,0))
        base.blit(text, (58, 100))
        text = self.font.render(str(player.soldiers), 1, (0,0,0))
        base.blit(text, (58, 150))
        text = self.font.render(str(player.mages), 1, (0,0,0))
        base.blit(text, (58, 200))
        text = self.font.render(str(player.bricks), 1, (0,0,0))
        base.blit(text, (136, 100))
        text = self.font.render(str(player.arms), 1, (0,0,0))
        base.blit(text, (136, 150))
        text = self.font.render(str(player.crystals), 1, (0,0,0))
        base.blit(text, (136, 200))

        self.surface.blit(base, (x, 0))

    def drawCards(self, hand, blind):
        """Draws all cards on the screen - i.e. player's hand (blind in case it's AI move) and the deck card
           hand - list of cards on player's hand; may be empty if blind is set
           blind - if true, the blind hand will be drawn (i.e. only backs of the cards, so that the player doesn't see AI player's hand)"""
        #self.drawSingleCard(
        #    ((self.surface.get_width()-self.CARD_WIDTH)/2, 0),
        #    deck[0], deck[1])

        for i in range(8):
            lefttop = (i * self.CARD_WIDTH, self.surface.get_height()-self.CARD_HEIGHT)
            card = hand[i][0]
            enabled = hand[i][1]
            if blind:
                sprite = self.sprites["card_blind"]
            else:
                if enabled:
                    sprite = self.sprites["card_e_" + card[Cards.C_NAME]]
                else:
                    sprite = self.sprites["card_d_" + card[Cards.C_NAME]]
            self.surface.blit(sprite, lefttop)

    def drawAnthills(self, castleP1, wallP1, castleP2, wallP2):
        """Draws both castles and walls
           castleP1 - height of P1's castle
           wallP1 - height of P1's wall
           castleP2 - height of P2's castle
           wallP2 - height of P2's wall"""
        pass


