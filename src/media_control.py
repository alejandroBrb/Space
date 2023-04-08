import pygame
from pygame.locals import *


def load_music(filename):
    try:
        sound = pygame.mixer.Sound(filename)
    except pygame.error as message:
        print('No se pudo cargar el sonido: ', filename)
        raise SystemExit(message)
    return sound


def load_images(filename, transparent=False):
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        raise SystemExit(message)
    image = image.convert()
    if transparent:
        color = image.get_at((0, 0))
        image.set_colorkey(color, RLEACCEL)
    return image
