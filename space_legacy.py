#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import random
import sys

# Modulos

# Constantes
ancho = 1000
alto = 800
blanco = (255, 255, 255)


# Clases

class Nave(pygame.sprite.Sprite):
    def __init__(self, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = carga_imagenes("assets/images/baseshipb.ico", True)
        self.rect = self.image.get_rect()

        self.rect.centery = y
        self.rect.centerx = ancho / 2
        self.vel = 0.5

    def mover(self, time, keys):
        if self.rect.right <= ancho:
            if keys[K_RIGHT] or keys[K_d]:
                self.rect.centerx += self.vel * time
        if self.rect.left >= 0:
            if keys[K_LEFT] or keys[K_a]:
                self.rect.centerx -= self.vel * time


# ---------------------------------------------------------------------
class Disparo(pygame.sprite.Sprite):

    def __init__(self, posicion):
        pygame.sprite.Sprite.__init__(self)
        self.image = carga_imagenes("assets/images/disparo.png")
        self.rect = self.image.get_rect()
        self.rect.center = posicion

    def update(self):
        if self.rect.top <= 0:
            self.kill()
        else:
            self.rect.move_ip((0, -5))


# ---------------------------------------------------------------------

class Disparo_malo(pygame.sprite.Sprite):

    def __init__(self, posicion):
        pygame.sprite.Sprite.__init__(self)
        self.image = carga_imagenes("assets/images/disparo.png")
        self.rect = self.image.get_rect()
        self.rect.center = posicion

    def update(self):
        if self.rect.bottom >= alto:
            self.kill()
        else:
            self.rect.move_ip((0, 5))


# ---------------------------------------------------------------------

class Malo_random(pygame.sprite.Sprite):

    def __init__(self, disparos_malos, grupo_sprite, sonido_dism):
        pygame.sprite.Sprite.__init__(self)
        self.sonido = sonido_dism
        self.gdisparos = disparos_malos
        self.gsprite = grupo_sprite
        self.eleccion = random.randint(0, 100)
        if self.eleccion <= 50:
            self.image = carga_imagenes("assets/images/mysteryb.ico", True)
        if 100 >= self.eleccion > 50:
            self.image = carga_imagenes("assets/images/mysterya.ico", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(100, 900)
        self.rect.y = 0
        self.velx = random.randint(-5, 5)
        self.vely = random.randint(1, 5)

    def update(self):
        muerto = 0
        self.rect.move_ip((self.velx, self.vely))
        if self.rect.left <= 0:
            self.velx = -self.velx
        if self.rect.right >= ancho:
            self.velx = -self.velx
        if self.rect.bottom >= alto:
            self.kill()

        dis = random.randint(1, 80)
        if (dis == 1):
            self.disparo()

    def disparo(self):
        disparo_m = Disparo_malo(self.rect.midbottom)
        self.gdisparos.add(disparo_m)
        self.gsprite.add(disparo_m)
        self.sonido.play()


# ---------------------------------------------------------------------
class Explosion(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = carga_imagenes("assets/images/explosion.png", True)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.delay = 3

    def update(self):
        if self.delay >= 0:
            self.delay -= 1
        else:
            self.kill()


# ---------------------------------------------------------------------
class Text(pygame.font.Font):
    def __init__(self, FontName=None, FontSize=30):
        pygame.font.init()
        self.font = pygame.font.Font(FontName, FontSize)
        self.size = FontSize

    def render(self, surface, text, color, pos):
        text = str(text)
        x, y = pos
        for i in text.split("z"):
            surface.blit(self.font.render(i, True, color), (x, y))
            y += self.size


# ---------------------------------------------------------------------
class Ventanas(Text):

    def __init__(self):
        self.text = Text()
        pygame.init()
        self.screen = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Space")
        self.background_image = carga_imagenes('assets/images/fondo.jpg')
        pygame.mouse.set_visible(False)
        self.screen.blit(self.background_image, (0, 0))

    def Game_over(self, p, n):
        while True:
            keys = pygame.key.get_pressed()
            self.text.render(self.screen, "GAME OVER", blanco, (430, 300))
            self.text.render(self.screen, "Puntos: " + p, blanco, (350, 470))
            self.text.render(self.screen, "Nivel: " + n, blanco, (550, 470))
            self.text.render(self.screen, "R para continuar", blanco, (50, 650))
            self.text.render(self.screen, "Q para salir", blanco, (50, 700))
            pygame.display.flip()
            for eventos in pygame.event.get():
                if eventos.type == QUIT or keys[K_q]:
                    sys.exit()
                if keys[K_r]:
                    return main()

    def inicio(self):
        # musica = carga_musica('sounds/')
        while True:
            keys = pygame.key.get_pressed()
            self.text.render(self.screen, "SPACE", blanco, (430, 300))
            self.text.render(self.screen, "R para iniciar", blanco, (50, 600))
            self.text.render(self.screen, "Mover: Flechas o A y D", blanco, (50, 650))
            self.text.render(self.screen, "Disparar: F o Espacio ", blanco, (50, 700))
            pygame.display.flip()
            for eventos in pygame.event.get():
                if eventos.type == QUIT:
                    sys.exit()
                if keys[K_r]:
                    pygame.display.quit()
                    return 1


# ---------------------------------------------------------------------
# Funciones

def carga_imagenes(filename, transparent=False):
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        raise SystemExit(message)
    image = image.convert()
    if transparent:
        color = image.get_at((0, 0))
        image.set_colorkey(color, RLEACCEL)
    return image


# ---------------------------------------------------------------------

# ---------------------------------------------------------------------

def carga_musica(filename):
    try:
        sound = pygame.mixer.Sound(filename)
    except pygame.error as message:
        print('No se pudo cargar el sonido: ', filename)
        raise SystemExit(message)
    return sound


# ---------------------------------------------------------------------

def main():
    temp_m = 0
    puntos = 0
    muerto = 0
    nivel = 1
    contador = 0
    ini = 0
    random.seed()

    screen = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Space")
    sonido_dis = carga_musica('assets/sounds/shoot.wav')
    sonido_dism = carga_musica('assets/sounds/ufo_highpitch.wav')
    sonido_exp = carga_musica('assets/sounds/explosion.wav')
    background_image = carga_imagenes('assets/images/fondo.jpg')
    pygame.mouse.set_visible(False)

    grupo_sprite = pygame.sprite.RenderClear()
    grupo_malos = pygame.sprite.RenderClear()
    disparos = pygame.sprite.RenderClear()
    disparos_malos = pygame.sprite.RenderClear()
    grupo_buenos = pygame.sprite.RenderClear()

    text = Text()
    nave = Nave(alto - 50)
    grupo_sprite.add(nave)
    grupo_buenos.add(nave)

    clock = pygame.time.Clock()

    ventana = Ventanas()
    ini = ventana.inicio()

    screen = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Space")
    sonido_dis = carga_musica('assets/sounds/shoot.wav')
    sonido_dism = carga_musica('assets/sounds/ufo_highpitch.wav')
    sonido_exp = carga_musica('assets/sounds/explosion.wav')
    background_image = carga_imagenes('assets/images/fondo.jpg')
    pygame.mouse.set_visible(False)

    if ini == 1:

        while True:
            time = clock.tick(60)

            keys = pygame.key.get_pressed()

            for eventos in pygame.event.get():
                if eventos.type == QUIT:
                    sys.exit(0)
                elif keys[K_f] or keys[K_SPACE]:
                    disparo_nave = Disparo(nave.rect.center)
                    disparos.add(disparo_nave)
                    grupo_sprite.add(disparo_nave)
                    sonido_dis.play()

            for hit in pygame.sprite.groupcollide(grupo_malos, disparos, True, True):
                (x, y) = hit.rect.center
                grupo_sprite.add(Explosion(x, y))
                sonido_exp.play()
                puntos = puntos + (10 * nivel)

            for hit in pygame.sprite.groupcollide(grupo_buenos, disparos_malos, True, True):
                (x, y) = hit.rect.center
                grupo_sprite.add(Explosion(x, y))
                sonido_exp.play()
                muerto = 1

            if muerto == 1:
                pygame.display.quit()
                ventana = Ventanas()
                ventana.Game_over(p, n)

            temp_m += 1
            if temp_m >= 100 - (nivel * 5):
                malos = Malo_random(disparos_malos, grupo_sprite, sonido_dism)
                grupo_malos.add(malos)
                grupo_sprite.add(malos)
                temp_m = 0
                contador += 1

            if contador >= 10:
                nivel += 1
                contador = 0

            p = str(puntos)
            n = str(nivel)

            muerto = grupo_sprite.update()

            nave.mover(time, keys)

            screen.blit(background_image, (0, 0))

            grupo_sprite.clear(screen, background_image)
            grupo_sprite.draw(screen)

            text.render(screen, "Puntos: " + p, blanco, (10, 20))
            text.render(screen, "Nivel: " + n, blanco, (200, 20))

            pygame.display.flip()

        return 0


if __name__ == '__main__':
    pygame.init()
    main()
