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

class UICard:
    def __init__(self, x, y, name, enabled, blind, zorder):
        self.x = x
        self.y = y
        self.name = name
        self.enabled = enabled
        self.blind = blind
        self.zorder = zorder

class Painter:
    def __init__(self, surface, game):
        self.surface = surface
        self.game = game
        self.dimensions = {
            'STATS_WIDTH': 168,
            'STATS_HEIGHT': 250,
            'CARD_WIDTH': 100,
            'CARD_HEIGHT': 150,
            'DISCARD_WIDTH': 40,
            'DISCARD_HEIGHT': 40
        }

        self.bmp = Bitmaps()
        self.sprites = Sprites(self.bmp, self.game.cards, self.dimensions)
        self.cards = {}
        self.deck_position = ((self.surface.get_width() - self.dimensions['CARD_WIDTH']) / 2, 0)
        self.discard_rect = [self.surface.get_width() / 2 + 120, 30, self.dimensions['DISCARD_WIDTH'], self.dimensions['DISCARD_HEIGHT']]


    def drawScreen(self, players, disposing):
        """Draws the entire screen"""
        self.drawBackground()
        self.drawStats(players[0], True)
        self.drawStats(players[1], False)
        self.drawAnthills(players[0].castle, players[0].wall, players[1].castle, players[1].wall)
        self.drawDisposeButton(disposing)
        self.drawCards()

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

    def drawCards(self):
        """Draws all cards on the screen - i.e. player's hand (blind in case it's AI move) and the deck card"""
        for card in sorted(self.cards.values(), key = lambda c: c.zorder):
            if card.blind:
                sprite = self.sprites["card_blind"]
            else:
                if card.enabled:
                    sprite = self.sprites["card_e_" + card.name]
                else:
                    sprite = self.sprites["card_d_" + card.name]
            self.surface.blit(sprite, (card.x, card.y))

    def drawAnthills(self, castleP1, wallP1, castleP2, wallP2):
        """Draws both castles and walls
           castleP1 - height of P1's castle
           wallP1 - height of P1's wall
           castleP2 - height of P2's castle
           wallP2 - height of P2's wall"""
        #TODO
        pass

    def drawDisposeButton(self, disposing):
        sprite = self.sprites["dispose_" + ["off", "on"][disposing]]
        self.surface.blit(sprite, (self.discard_rect[0], self.discard_rect[1]))

    def updateDisplayedCards(self, player):
        blind = not player.isHuman()
        i = 0
        for card in zip(player.cards, player.playable):
            self.cards[i] = UICard(
                x = i * self.dimensions['CARD_WIDTH'],
                y = self.surface.get_height()-self.dimensions['CARD_HEIGHT'],
                name = card[0][Cards.C_NAME],
                enabled = card[1],
                blind = blind,
                zorder = 1
            )
            i += 1

    def card_rect(self, card_no):
        if card_no not in self.cards:
            return [-1,-1,0,0]
        return [self.cards[card_no].x, self.cards[card_no].y, self.dimensions['CARD_WIDTH'], self.dimensions['CARD_HEIGHT']]
        

