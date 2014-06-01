import pygame
import pygame.image
import Cards

class Sprites:
    def __init__(self, bitmaps, card_set, card_width, card_height):
        self.sprites = {}
        self.bmp = bitmaps
        self.card_width = card_width
        self.card_height = card_height
        self.font = pygame.font.SysFont(None, 20)
        self._init_card_sprites(card_set)

    def __getitem__(self, name):
        return self.sprites[name]

    def _init_card_sprites(self, card_set):
        for card in card_set:
            self.sprites["card_e_" + card[Cards.C_NAME]] = self._create_card(card, True)
            self.sprites["card_d_" + card[Cards.C_NAME]] = self._create_card(card, False)
        self.sprites["card_blind"] = self._create_blind_card()
        
    def _create_blind_card(self):
        return self._create_blank_card((30,30,90))

    def _create_card(self, cardSpec, enabled):
        card = self._create_blank_card((255,255,255))

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

        pygame.draw.line(card, (0,0,0), (5, 46), (self.card_width-5, 46))

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
            overlay = pygame.Surface((self.card_width, self.card_height))
            overlay.fill((25,25,25))
            pygame.draw.ellipse(overlay, (0,0,0), (-120,-100,240,200), 0)
            #card.blit(overlay, (0,0))
            card.blit(overlay, (0,0), special_flags = pygame.BLEND_SUB)

        return card

    def _create_blank_card(self, fillColor):
        card = pygame.Surface((self.card_width, self.card_height))
        card.fill(fillColor)
        pygame.draw.rect(card, (0,0,0), pygame.Rect(0,0,self.card_width,self.card_height), 1)
        return card


