from pygame.locals import *
import pygame

from src.media_control import load_images
import sys
import random
from src.constants import *


class Text(pygame.font.Font):
    def __init__(self, font_name=None, font_size=30):
        pygame.font.init()
        self.font = pygame.font.Font(font_name, font_size)
        self.size = font_size

    def render(self, surface, text, color, pos):
        text = str(text)
        x, y = pos
        for i in text.split("z"):
            surface.blit(self.font.render(i, True, color), (x, y))
            y += self.size


class Window(Text):

    def __init__(self):
        self.text = Text()
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Space")
        self.background_image = load_images('images/fondo.jpg')
        pygame.mouse.set_visible(False)
        self.screen.blit(self.background_image, (0, 0))

    def game_over(self, p, n):
        while True:
            keys = pygame.key.get_pressed()
            self.text.render(self.screen, "GAME OVER", COLOR_WHITE, (430, 300))
            self.text.render(self.screen, "Puntos: " + p, COLOR_WHITE, (350, 470))
            self.text.render(self.screen, "Nivel: " + n, COLOR_WHITE, (550, 470))
            self.text.render(self.screen, "R para continuar", COLOR_WHITE, (50, 650))
            self.text.render(self.screen, "Q para salir", COLOR_WHITE, (50, 700))
            pygame.display.flip()
            for events in pygame.event.get():
                if events.type == QUIT or keys[K_q]:
                    sys.exit()
                if keys[K_r]:
                    return init.main()

    def start(self):
        while True:
            keys = pygame.key.get_pressed()
            self.text.render(self.screen, "SPACE", COLOR_WHITE, (430, 300))
            self.text.render(self.screen, "R para iniciar", COLOR_WHITE, (50, 600))
            self.text.render(self.screen, "Mover: Flechas o A y D", COLOR_WHITE, (50, 650))
            self.text.render(self.screen, "Disparar: F o Espacio ", COLOR_WHITE, (50, 700))
            pygame.display.flip()
            for events in pygame.event.get():
                if events.type == QUIT:
                    sys.exit()
                if keys[K_r]:
                    # pygame.display.quit()
                    return 1
