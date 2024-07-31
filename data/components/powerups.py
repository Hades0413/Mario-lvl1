__author__ = 'hades0413'

import pygame as pg
from .. import constants as c
from .. import setup


class Powerup(pg.sprite.Sprite):
    """Clase base para todo powerup_group"""
    def __init__(self, x, y):
        super(Powerup, self).__init__()


    def setup_powerup(self, x, y, name, setup_frames):
        """Esta función de configuración separada me permite pasar un
        método setup_frames dependiendo de cuál sea el encendido"""
        self.sprite_sheet = setup.GFX['item_objects']
        self.frames = []
        self.frame_index = 0
        setup_frames()
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.state = c.REVEAL
        self.y_vel = -1
        self.x_vel = 0
        self.direction = c.RIGHT
        self.box_height = y
        self.gravity = 1
        self.max_y_vel = 8
        self.animate_timer = 0
        self.name = name


    def get_image(self, x, y, width, height):
        """Obtener los marcos de imagen de la hoja de sprites"""

        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.BLACK)


        image = pg.transform.scale(image,
                                   (int(rect.width*c.SIZE_MULTIPLIER),
                                    int(rect.height*c.SIZE_MULTIPLIER)))
        return image


    def update(self, game_info, *args):
        """Actualiza el comportamiento de encendido"""
        self.current_time = game_info[c.CURRENT_TIME]
        self.handle_state()


    def handle_state(self):
        pass


    def revealing(self, *args):
        """Acción cuando el encendido deja la caja de monedas o el ladrillo."""
        self.rect.y += self.y_vel

        if self.rect.bottom <= self.box_height:
            self.rect.bottom = self.box_height
            self.y_vel = 0
            self.state = c.SLIDE


    def sliding(self):
        """Acción para cuando el encendido se desliza por el suelo"""
        if self.direction == c.RIGHT:
            self.x_vel = 3
        else:
            self.x_vel = -3


    def falling(self):
        """Cuando los powerups caen de una repisa"""
        if self.y_vel < self.max_y_vel:
            self.y_vel += self.gravity


class Mushroom(Powerup):
    """Powerup que hace que Mario sea más grande"""
    def __init__(self, x, y, name='mushroom'):
        super(Mushroom, self).__init__(x, y)
        self.setup_powerup(x, y, name, self.setup_frames)


    def setup_frames(self):
        """Configura la lista de marcos"""
        self.frames.append(self.get_image(0, 0, 16, 16))


    def handle_state(self):
        """Maneja el comportamiento basado en el estado"""
        if self.state == c.REVEAL:
            self.revealing()
        elif self.state == c.SLIDE:
            self.sliding()
        elif self.state == c.FALL:
            self.falling()


class LifeMushroom(Mushroom):
    """1up mushroom"""
    def __init__(self, x, y, name='1up_mushroom'):
        super(LifeMushroom, self).__init__(x, y)
        self.setup_powerup(x, y, name, self.setup_frames)

    def setup_frames(self):
        self.frames.append(self.get_image(16, 0, 16, 16))


class FireFlower(Powerup):
    """Powerup que le permite a Mario lanzar bolas de fuego"""
    def __init__(self, x, y, name=c.FIREFLOWER):
        super(FireFlower, self).__init__(x, y)
        self.setup_powerup(x, y, name, self.setup_frames)


    def setup_frames(self):
        """Configura la lista de marcos"""
        self.frames.append(
            self.get_image(0, 32, 16, 16))
        self.frames.append(
            self.get_image(16, 32, 16, 16))
        self.frames.append(
            self.get_image(32, 32, 16, 16))
        self.frames.append(
            self.get_image(48, 32, 16, 16))


    def handle_state(self):
        """Manejar el comportamiento basado en el estado"""
        if self.state == c.REVEAL:
            self.revealing()
        elif self.state == c.RESTING:
            self.resting()


    def revealing(self):
        """Animación de flor saliendo de caja"""
        self.rect.y += self.y_vel

        if self.rect.bottom <= self.box_height:
            self.rect.bottom = self.box_height
            self.state = c.RESTING

        self.animation()


    def resting(self):
        """Fire Flower permanece inmóvil en la caja abierta"""
        self.animation()


    def animation(self):
        """Método para hacer parpadear la Flor de Fuego"""
        if (self.current_time - self.animate_timer) > 30:
            if self.frame_index < 3:
                self.frame_index += 1
            else:
                self.frame_index = 0

            self.image = self.frames[self.frame_index]
            self.animate_timer = self.current_time


class Star(Powerup):
    """Un potenciador que le da invencibilidad a mario."""
    def __init__(self, x, y, name='star'):
        super(Star, self).__init__(x, y)
        self.setup_powerup(x, y, name, self.setup_frames)
        self.animate_timer = 0
        self.rect.y += 1  #looks more centered offset one pixel
        self.gravity = .4


    def setup_frames(self):
        """Creando la lista self.frames donde están las imágenes para la animación
        se almacenan"""
        self.frames.append(self.get_image(1, 48, 15, 16))
        self.frames.append(self.get_image(17, 48, 15, 16))
        self.frames.append(self.get_image(33, 48, 15, 16))
        self.frames.append(self.get_image(49, 48, 15, 16))


    def handle_state(self):
        """Maneja el comportamiento basado en el estado"""
        if self.state == c.REVEAL:
            self.revealing()
        elif self.state == c.BOUNCE:
            self.bouncing()


    def revealing(self):
        """Cuando la estrella sale de la caja"""
        self.rect.y += self.y_vel

        if self.rect.bottom <= self.box_height:
            self.rect.bottom = self.box_height
            self.start_bounce(-2)
            self.state = c.BOUNCE

        self.animation()


    def animation(self):
        """establece la imagen para la animación"""
        if (self.current_time - self.animate_timer) > 30:
            if self.frame_index < 3:
                self.frame_index += 1
            else:
                self.frame_index = 0
            self.animate_timer = self.current_time
            self.image = self.frames[self.frame_index]


    def start_bounce(self, vel):
        """Transiciones al estado de rebote"""
        self.y_vel = vel


    def bouncing(self):
        """Acción cuando la estrella rebota"""
        self.animation()

        if self.direction == c.LEFT:
            self.x_vel = -5
        else:
            self.x_vel = 5



class FireBall(pg.sprite.Sprite):
    """Disparo de Fuego Mario"""
    def __init__(self, x, y, facing_right, name=c.FIREBALL):
        super(FireBall, self).__init__()
        self.sprite_sheet = setup.GFX['item_objects']
        self.setup_frames()
        if facing_right:
            self.direction = c.RIGHT
            self.x_vel = 12
        else:
            self.direction = c.LEFT
            self.x_vel = -12
        self.y_vel = 10
        self.gravity = .9
        self.frame_index = 0
        self.animation_timer = 0
        self.state = c.FLYING
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.y = y
        self.name = name


    def setup_frames(self):
        """Configura fotogramas de animación."""
        self.frames = []

        self.frames.append(
            self.get_image(96, 144, 8, 8))    #Frame 1 of flying
        self.frames.append(
            self.get_image(104, 144, 8, 8))   #Frame 2 of Flying
        self.frames.append(
            self.get_image(96, 152, 8, 8))    #Frame 3 of Flying
        self.frames.append(
            self.get_image(104, 152, 8, 8))   #Frame 4 of flying
        self.frames.append(
            self.get_image(112, 144, 16, 16)) #frame 1 of exploding
        self.frames.append(
            self.get_image(112, 160, 16, 16)) #frame 2 of exploding
        self.frames.append(
            self.get_image(112, 176, 16, 16)) #frame 3 of exploding


    def get_image(self, x, y, width, height):
        """Obtener los marcos de imagen de la hoja de sprites"""

        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.BLACK)


        image = pg.transform.scale(image,
                                   (int(rect.width*c.SIZE_MULTIPLIER),
                                    int(rect.height*c.SIZE_MULTIPLIER)))
        return image


    def update(self, game_info, viewport):
        """Actualiza el comportamiento de la bola de fuego."""
        self.current_time = game_info[c.CURRENT_TIME]
        self.handle_state()
        self.check_if_off_screen(viewport)


    def handle_state(self):
        """Maneja el comportamiento basado en el estado"""
        if self.state == c.FLYING:
            self.animation()
        elif self.state == c.BOUNCING:
            self.animation()
        elif self.state == c.EXPLODING:
            self.animation()


    def animation(self):
        """ajusta el marco para la animación"""
        if self.state == c.FLYING or self.state == c.BOUNCING:
            if (self.current_time - self.animation_timer) > 200:
                if self.frame_index < 3:
                    self.frame_index += 1
                else:
                    self.frame_index = 0
                self.animation_timer = self.current_time
                self.image = self.frames[self.frame_index]


        elif self.state == c.EXPLODING:
            if (self.current_time - self.animation_timer) > 50:
                if self.frame_index < 6:
                    self.frame_index += 1
                    self.image = self.frames[self.frame_index]
                    self.animation_timer = self.current_time
                else:
                    self.kill()


    def explode_transition(self):
        """Transiciones bola de fuego al estado de EXPLOSIÓN"""
        self.frame_index = 4
        centerx = self.rect.centerx
        self.image = self.frames[self.frame_index]
        self.rect.centerx = centerx
        self.state = c.EXPLODING


    def check_if_off_screen(self, viewport):
        """Elimina del grupo de sprites si está fuera de la pantalla"""
        if (self.rect.x > viewport.right) or (self.rect.y > viewport.bottom) \
            or (self.rect.right < viewport.x):
            self.kill()
