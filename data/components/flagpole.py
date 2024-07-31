__author__ = 'hades0413'

import pygame as pg
from .. import setup
from .. import constants as c

class Flag(pg.sprite.Sprite):
    """Bandera en la parte superior del asta de la bandera al final del nivel"""
    def __init__(self, x, y):
        super(Flag, self).__init__()
        self.sprite_sheet = setup.GFX['item_objects']
        self.setup_images()
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.y = y
        self.state = c.TOP_OF_POLE


    def setup_images(self):
        """Configura una lista de marcos de imagen"""
        self.frames = []

        self.frames.append(
            self.get_image(128, 32, 16, 16))


    def get_image(self, x, y, width, height):
        """Extrae la imagen de la hoja de sprites"""
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.BLACK)
        image = pg.transform.scale(image,
                                   (int(rect.width*c.BRICK_SIZE_MULTIPLIER),
                                    int(rect.height*c.BRICK_SIZE_MULTIPLIER)))
        return image


    def update(self, *args):
        """Actualiza el comportamiento"""
        self.handle_state()


    def handle_state(self):
        """Determina el comportamiento basado en el estado."""
        if self.state == c.TOP_OF_POLE:
            self.image = self.frames[0]
        elif self.state == c.SLIDE_DOWN:
            self.sliding_down()
        elif self.state == c.BOTTOM_OF_POLE:
            self.image = self.frames[0]


    def sliding_down(self):
        """Estado cuando Mario llega al asta de la bandera"""
        self.y_vel = 5
        self.rect.y += self.y_vel

        if self.rect.bottom >= 485:
            self.state = c.BOTTOM_OF_POLE


class Pole(pg.sprite.Sprite):
    """Asta sobre la que está la bandera"""
    def __init__(self, x, y):
        super(Pole, self).__init__()
        self.sprite_sheet = setup.GFX['tile_set']
        self.setup_frames()
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def setup_frames(self):
        """Crear la lista de marcos"""
        self.frames = []

        self.frames.append(
            self.get_image(263, 144, 2, 16))


    def get_image(self, x, y, width, height):
        """Extrae la imagen de la hoja de sprites"""
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.BLACK)
        image = pg.transform.scale(image,
                                   (int(rect.width*c.BRICK_SIZE_MULTIPLIER),
                                    int(rect.height*c.BRICK_SIZE_MULTIPLIER)))
        return image


    def update(self, *args):
        """Marcador de posición para actualizar, ya que no hay nada que actualizar"""
        pass


class Finial(pg.sprite.Sprite):
    """La parte superior del asta de la bandera"""
    def __init__(self, x, y):
        super(Finial, self).__init__()
        self.sprite_sheet = setup.GFX['tile_set']
        self.setup_frames()
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y


    def setup_frames(self):
        """Crea la lista self.frames"""
        self.frames = []

        self.frames.append(
            self.get_image(228, 120, 8, 8))


    def get_image(self, x, y, width, height):
        """Extrae la imagen de la hoja de sprites"""
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.BLACK)
        image = pg.transform.scale(image,
                                   (int(rect.width*c.SIZE_MULTIPLIER),
                                    int(rect.height*c.SIZE_MULTIPLIER)))
        return image


    def update(self, *args):
        pass
