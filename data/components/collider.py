__author__ = 'hades0413'

import pygame as pg
from .. import constants as c

class Collider(pg.sprite.Sprite):
    """Sprites invisibles colocados sobre partes de fondo superiores
    que puedan ser colisionados (tuberías, escalones, suelo, etc)"""
    def __init__(self, x, y, width, height, name='collider'):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width, height)).convert()
        #self.image.fill(c.RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.state = None

