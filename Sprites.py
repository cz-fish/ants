import pygame
import pygame.image
import Cards

class Sprites:
    def __init__(self, bitmaps, card_set, dimensions):
        self.sprites = {}
        self.bmp = bitmaps
        self.dimensions = dimensions
        self._cached_stats = {}
        self.font = pygame.font.SysFont(None, 20)
        self._init_card_sprites(card_set)
        self._init_other_sprites()

    def __getitem__(self, name):
        return self.sprites[name]

    def get_player_stats_sprite(self, sprite_name, values):
        key = "cached_stats_" + sprite_name
        if sprite_name in self._cached_stats and self._cached_stats[sprite_name] == values:
            return self.sprites[key]

        sprite = self._render_stats_sprite(values)
        self.sprites[key] = sprite
        self._cached_stats[sprite_name] = values
        return sprite

    def _render_stats_sprite(self, values):
        mx = self.dimensions['STATS_WIDTH']
        my = self.dimensions['STATS_HEIGHT']
        base = pygame.Surface((mx, my))
        base.fill((210,210,210))
        self._render_topleft_corner(base, (170,170,170), mx, my)
        self._render_bottomright_corner(base, (240,240,240), mx, my)

        #TODO: colors and overall scores
        text = self.font.render(values['player_name'], 1, (0,0,0))
        base.blit(text, (10, 5))
        
        base.blit(self.bmp['stats_castle'], (7, 20))
        base.blit(self.bmp['stats_wall'], (85, 20))
        base.blit(self.bmp['rsrc_architect'], (7, 83))
        base.blit(self.bmp['rsrc_soldier'], (7, 136))
        base.blit(self.bmp['rsrc_mage'], (7, 189))
        base.blit(self.bmp['rsrc_brick'], (85, 83))
        base.blit(self.bmp['rsrc_arm'], (85, 136))
        base.blit(self.bmp['rsrc_crystal'], (85, 189))

        text = self.font.render(str(values['castle']), 1, (0,0,0))
        base.blit(text, (58, 40))
        text = self.font.render(str(values['wall']), 1, (0,0,0))
        base.blit(text, (136, 40))
        text = self.font.render(str(values['architects']), 1, (0,0,0))
        base.blit(text, (58, 100))
        text = self.font.render(str(values['soldiers']), 1, (0,0,0))
        base.blit(text, (58, 150))
        text = self.font.render(str(values['mages']), 1, (0,0,0))
        base.blit(text, (58, 200))
        text = self.font.render(str(values['bricks']), 1, (0,0,0))
        base.blit(text, (136, 100))
        text = self.font.render(str(values['arms']), 1, (0,0,0))
        base.blit(text, (136, 150))
        text = self.font.render(str(values['crystals']), 1, (0,0,0))
        base.blit(text, (136, 200))
        return base


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

        pygame.draw.line(card, (0,0,0), (5, 46), (self.dimensions['CARD_WIDTH']-5, 46))

        top = 50
        if cardSpec[Cards.C_NAME] == 'curse':
            # special case: curse
            card.blit(self.bmp['action_curse_sm'], (5, top))
            text = self.font.render(str(cardSpec[Cards.C_LOSE][0]), 1, (0,0,0))
            card.blit(text, (29, top + 4))
        else:
            for i in [0, 1, 2, 3, 4, 5]:
                left = 5
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

            actions = cardSpec[Cards.C_BUILD] + cardSpec[Cards.C_DESTROY]
            for i in range(5):
                left = 5
                if actions[i] != 0:
                    card.blit(self.bmp['action_' + ['castle', 'wall', 'attack', 'castle_attack', 'wall_attack'][i] + '_sm'], (left, top))
                    text = self.font.render(str(actions[i]), 1, (0,0,0))
                    card.blit(text, (left + 24, top + 4))
                    top += 30

        if not enabled:
            overlay = pygame.Surface((self.dimensions['CARD_WIDTH'], self.dimensions['CARD_HEIGHT']))
            overlay.fill((25,25,25))
            pygame.draw.ellipse(overlay, (0,0,0), (-120,-100,240,200), 0)
            card.blit(overlay, (0,0), special_flags = pygame.BLEND_SUB)

        return card

    def _create_blank_card(self, fillColor):
        card = pygame.Surface((self.dimensions['CARD_WIDTH'], self.dimensions['CARD_HEIGHT']))
        card.fill(fillColor)
        pygame.draw.rect(card, (0,0,0), pygame.Rect(0,0,self.dimensions['CARD_WIDTH'],self.dimensions['CARD_HEIGHT']), 1)
        return card

    def _init_other_sprites(self):
        # TODO: put some icon on the dispose button
        mx = self.dimensions['DISCARD_WIDTH']
        my = self.dimensions['DISCARD_HEIGHT']
        dispose = pygame.Surface((mx, my))
        dispose.fill((180,180,180))
        self._render_topleft_corner(dispose, (140,140,140), mx, my)
        self._render_bottomright_corner(dispose, (240,240,240), mx, my)
        self.sprites['dispose_on'] = dispose

        dispose = pygame.Surface((mx, my))
        dispose.fill((210,210,210))
        self._render_topleft_corner(dispose, (240,240,240), mx, my)
        self._render_bottomright_corner(dispose, (140,140,140), mx, my)
        self.sprites['dispose_off'] = dispose

    def _render_topleft_corner(self, surface, color, mx, my):
        pygame.draw.polygon(surface,
            color,
            [(0,0), (0,my), (3, my-3), (3,3), (mx - 3, 3), (mx, 0)],
            0)

    def _render_bottomright_corner(self, surface, color, mx, my):
        pygame.draw.polygon(surface,
            color,
            [(0,my), (3,my-3), (mx-3, my-3),(mx-3,3), (mx, 0), (mx, my)],
            0)



