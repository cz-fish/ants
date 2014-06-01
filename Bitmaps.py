import pygame.image
import os

class Bitmaps:
    def __init__(self):
        self._bmp = {}
        self._load_bitmaps()

    def _load_bitmaps(self):
        ext = '.png'
        for v in ['brick', 'arm', 'crystal', 'architect', 'soldier', 'mage']:
            self._bmp['rsrc_' + v] = pygame.image.load(os.path.join('data', 'rsrc_' + v + ext))
            self._bmp['rsrc_' + v + '_sm'] = pygame.image.load(os.path.join('data', 'rsrc_' + v + '_sm' + ext))
        for v in ['attack', 'castle_attack', 'wall_attack', 'curse', 'transfer']:
            self._bmp['action_' + v] = pygame.image.load(os.path.join('data', 'action_' + v + ext))
        for v in ['castle', 'wall']:
            self._bmp['stats_' + v] = pygame.image.load(os.path.join('data', 'stats_' + v + ext))
        for v in ['castle', 'wall', 'transfer']:
            self._bmp['action_' + v + '_sm'] = pygame.image.load(os.path.join('data', 'action_' + v + '_sm' + ext))

    def __getitem__(self, name):
        return self._bmp[name]

