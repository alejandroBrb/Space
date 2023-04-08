import pygame

from src.media_control import load_images
import random
from src.constants import *

PATH_IMAGES = "assets/images"


class Enemy(pygame.sprite.Sprite):

    def __init__(self, shots, g_sprite, sound):
        pygame.sprite.Sprite.__init__(self)
        self.sound = sound
        self.g_shots = shots
        self.g_sprite = g_sprite
        self.respawn = random.randint(0, 100)
        if self.respawn <= 50:
            self.image = load_images(PATH_IMAGES + "/mysteryb.ico", True)
        if 100 >= self.respawn > 50:
            self.image = load_images(PATH_IMAGES + "/mysterya.ico", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(100, 900)
        self.rect.y = 0
        self.velx = random.randint(-5, 5)
        self.vely = random.randint(1, 5)

    def update(self):
        self.rect.move_ip((self.velx, self.vely))
        if self.rect.left <= 0:
            self.velx = -self.velx
        if self.rect.right >= WINDOW_WIDTH:
            self.velx = -self.velx
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.kill()

        dis = random.randint(1, 80)
        if dis == 1:
            self.shot()

    def shot(self):
        shot_enemy = EnemyShot(self.rect.midbottom)
        self.g_shots.add(shot_enemy)
        self.g_sprite.add(shot_enemy)
        self.sound.play()


class EnemyShot(pygame.sprite.Sprite):

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_images(PATH_IMAGES + "/disparo.png")
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self):
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.kill()
        else:
            self.rect.move_ip((0, 5))


class Explosion(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_images(PATH_IMAGES + "/explosion.png", True)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.delay = 3

    def update(self):
        if self.delay >= 0:
            self.delay -= 1
        else:
            self.kill()
