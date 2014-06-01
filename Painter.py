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
        self.dimensions = {
            'STATS_WIDTH': 168,
            'STATS_HEIGHT': 250,
            'CARD_WIDTH': 100,
            'CARD_HEIGHT': 150
        }

        self.font = pygame.font.SysFont(None, 20)
        
        self.bmp = Bitmaps()
        self.sprites = Sprites(self.bmp, self.game.cards, self.dimensions)


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
           player - player stats/info
           left - align to the left of the screen (True) or to the right (False)"""
        mx = self.dimensions['STATS_WIDTH']
        my = self.dimensions['STATS_HEIGHT']
        x = [self.surface.get_width() - mx, 0][left]

        values = {
            'player_name': 'Player ' + ['2', '1'][left],
            'castle': player.castle,
            'wall': player.wall,
            'architects': player.architects,
            'soldiers': player.soldiers,
            'mages': player.mages,
            'bricks': player.bricks,
            'arms': player.arms,
            'crystals': player.crystals
        }

        stats = self.sprites.get_player_stats_sprite(['right','left'][left], values)
        self.surface.blit(stats, (x, 0))

    def drawCards(self, hand, blind):
        """Draws all cards on the screen - i.e. player's hand (blind in case it's AI move) and the deck card
           hand - list of cards on player's hand; may be empty if blind is set
           blind - if true, the blind hand will be drawn (i.e. only backs of the cards, so that the player doesn't see AI player's hand)"""
        #self.drawSingleCard(
        #    ((self.surface.get_width()-self.CARD_WIDTH)/2, 0),
        #    deck[0], deck[1])

        for i in range(8):
            lefttop = (i * self.dimensions['CARD_WIDTH'], self.surface.get_height()-self.dimensions['CARD_HEIGHT'])
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


