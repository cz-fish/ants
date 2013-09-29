import pygame
import pygame.image
import Cards
from math import pi
import os

# TODO: unite colors of resources:
#   school/brick - red
#   soldier/arms - green
#   mages/crystals - blue

class Painter:
    def __init__(self, surface):
        self.surface = surface
        self.STATS_WIDTH = 168
        self.STATS_HEIGHT = 250
        self.CARD_WIDTH = 100
        self.CARD_HEIGHT = 150

        self.font = pygame.font.SysFont(None, 20)
        
        self.blindCard = []

        self.loadBitmaps()

    def loadBitmaps(self):
        self.bmp = {}
        ext = '.png'
        for v in ['brick', 'arm', 'crystal', 'architect', 'soldier', 'mage']:
            self.bmp['rsrc_' + v] = pygame.image.load(os.path.join('data', 'rsrc_' + v + ext))
            self.bmp['rsrc_' + v + '_sm'] = pygame.image.load(os.path.join('data', 'rsrc_' + v + '_sm' + ext))
        for v in ['attack', 'castle_attack', 'wall_attack', 'curse', 'transfer']:
            self.bmp['action_' + v] = pygame.image.load(os.path.join('data', 'action_' + v + ext))
        for v in ['castle', 'wall']:
            self.bmp['stats_' + v] = pygame.image.load(os.path.join('data', 'stats_' + v + ext))
        for v in ['castle', 'wall', 'transfer']:
            self.bmp['action_' + v + '_sm'] = pygame.image.load(os.path.join('data', 'action_' + v + '_sm' + ext))

    def drawScreen(self, players, game):
        """Draws the entire screen"""
        self.drawBackground()
        self.drawStats(players[0], True)
        self.drawStats(players[1], False)
        self.drawAnthills(players[0].castle, players[0].wall, players[1].castle, players[1].wall)
        #FIXME
        hand = players[0].cards
        enabled = players[0].playable
        blind = False
        deck = self.blindCard

        self.drawCards([(hand[i], enabled[i]) for i in range(len(hand))], blind, deck)

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

    def drawSingleCard(self, lefttop, card, enabled):
        """Draws a single card
           lefttop - tuple of (x,y) coordinates of the topleft corner of the card
           card - card information (TBD)
           enabled - if false, the card is drawn as grayscale only"""
        cardSurf = self.createCard(card, enabled, False)
        self.surface.blit(cardSurf, lefttop)

    def drawCards(self, hand, blind, deck):
        """Draws all cards on the screen - i.e. player's hand (blind in case it's AI move) and the deck card
           hand - list of cards on player's hand; may be empty if blind is set
           blind - if true, the blind hand will be drawn (i.e. only backs of the cards, so that the player doesn't see AI player's hand)
           deck - card at the top of the deck (with enabled/disabled flag)"""
        #self.drawSingleCard(
        #    ((self.surface.get_width()-self.CARD_WIDTH)/2, 0),
        #    deck[0], deck[1])

        for i in range(8):
            lefttop = (i * self.CARD_WIDTH, self.surface.get_height()-self.CARD_HEIGHT)
            if blind:
                self.surface.blit(self.createCard([], True, True), lefttop)
            else:
                self.drawSingleCard(lefttop, hand[i][0], hand[i][1])

    def drawAnthills(self, castleP1, wallP1, castleP2, wallP2):
        """Draws both castles and walls
           castleP1 - height of P1's castle
           wallP1 - height of P1's wall
           castleP2 - height of P2's castle
           wallP2 - height of P2's wall"""
        pass

    def createCard(self, cardSpec, enabled, blind):
        if blind:
            if not self.blindCard:
                self.blindCard = self.createBlankCard((30,30,90))
            return self.blindCard

        card = self.createBlankCard((255,255,255))

        #TODO: translate card name
        text = self.font.render(cardSpec[Cards.C_NAME], 1, (0,0,0))
        card.blit(text, (3, 3))
        left = 5
        for i in [0, 1, 2]:
            if cardSpec[Cards.C_COST][i] != 0:
                card.blit(self.bmp['rsrc_' + ['brick', 'arm', 'crystal'][i] + '_sm'], (left, 18))
                text = self.font.render(str(cardSpec[Cards.C_COST][i]), 1, (0,0,0))
                card.blit(text, (left + 24, 22))
                left += 35

        pygame.draw.line(card, (0,0,0), (5, 46), (self.CARD_WIDTH-5, 46))

        top = 50
        # TODO: special case: curse

        for i in [0, 1, 2, 3, 4, 5]:
            left = 5
            # FIXME: review the adding of '+' signs. Make sure that we never generate '+-'
            if cardSpec[Cards.C_GAIN][i] != 0 or cardSpec[Cards.C_LOSE][i] != 0:
                card.blit(self.bmp['rsrc_' + ['brick', 'arm', 'crystal', 'architect', 'soldier', 'mage'][i] + '_sm'], (left, top))
                if cardSpec[Cards.C_GAIN][i] != 0 and cardSpec[Cards.C_LOSE][i] != 0:
                    # this is a resource transfer
                    text = self.font.render(str(-cardSpec[Cards.C_LOSE][i]), 1, (0,0,0))
                    card.blit(text, (left + 24, top + 4))
                    left += 35
                    card.blit(self.bmp['action_transfer_sm'], (left, top))
                    text = self.font.render('+' + str(cardSpec[Cards.C_GAIN][i]), 1, (0,0,0))
                    card.blit(text, (left + 24, top + 4))
                    left += 35
                elif cardSpec[Cards.C_GAIN][i] != 0:
                    # plain positive effect
                    text = self.font.render('+' + str(cardSpec[Cards.C_GAIN][i]), 1, (0,0,0))
                    card.blit(text, (left + 24, top + 4))
                    left += 35
                else:
                    # plain negative effect
                    text = self.font.render(str(-cardSpec[Cards.C_LOSE][i]), 1, (0,0,0))
                    card.blit(text, (left + 24, top + 4))
                    left += 35
                top += 30

        # TODO: castle/wall and attack in a similar fashion

        if not enabled:
            overlay = pygame.Surface((self.CARD_WIDTH, self.CARD_HEIGHT))
            overlay.fill((25,25,25))
            pygame.draw.ellipse(overlay, (0,0,0), (-120,-100,240,200), 0)
            #card.blit(overlay, (0,0))
            card.blit(overlay, (0,0), special_flags = pygame.BLEND_SUB)

        return card

    def createBlankCard(self, fillColor):
        card = pygame.Surface((self.CARD_WIDTH, self.CARD_HEIGHT))
        card.fill(fillColor)
        pygame.draw.rect(card, (0,0,0), pygame.Rect(0,0,self.CARD_WIDTH,self.CARD_HEIGHT), 1)
        return card


