from pygame.locals import *
import pygame

from src.media_control import load_images
from src.constants import *


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = load_images("images/baseshipb.ico", True)
        self.rect = self.image.get_rect()

        self.container_width = WINDOW_WIDTH
        self.rect.centery = y
        self.rect.centerx = WINDOW_WIDTH / 2
        self.vel = 0.5

    def move(self, time, keys):
        if self.rect.right <= self.container_width:
            if keys[K_RIGHT] or keys[K_d]:
                self.rect.centerx += self.vel * time
        if self.rect.left >= 0:
            if keys[K_LEFT] or keys[K_a]:
                self.rect.centerx -= self.vel * time


class Shot(pygame.sprite.Sprite):

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_images("images/disparo.png")
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self):
        if self.rect.top <= 0:
            self.kill()
        else:
            self.rect.move_ip((0, -5))
