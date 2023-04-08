import pygame
from pygame.locals import *
import random
import sys
from src.constants import *
from src.media_control import load_music
from src.media_control import load_images
from src.interface import Window
from src.interface import Text
from src.spaceship import Spaceship
from src.spaceship import Shot
from src.enemy import Explosion
from src.enemy import Enemy


def main():
    temp_m = 0
    points = 0
    dead = 0
    level = 1
    count = 0
    random.seed()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Space")
    sound_shot = load_music('sounds/shoot.wav')
    sound_enemy = load_music('sounds/ufo_highpitch.wav')
    sound_explosion = load_music('sounds/explosion.wav')
    background_image = load_images('images/fondo.jpg')
    pygame.mouse.set_visible(False)

    g_sprite = pygame.sprite.RenderClear()
    g_enemy = pygame.sprite.RenderClear()
    g_shots = pygame.sprite.RenderClear()
    g_enemy_shots = pygame.sprite.RenderClear()
    g_main_character = pygame.sprite.RenderClear()

    text = Text()
    spaceship = Spaceship(WINDOW_HEIGHT - 50)
    g_sprite.add(spaceship)
    g_main_character.add(spaceship)

    clock = pygame.time.Clock()

    window = Window()
    ini = window.start()

    if ini == 1:
        while True:
            time = clock.tick(60)

            keys = pygame.key.get_pressed()

            for events in pygame.event.get():
                if events.type == QUIT:
                    sys.exit(0)
                elif keys[K_f] or keys[K_SPACE]:
                    shot_spaceship = Shot(spaceship.rect.center)
                    g_shots.add(shot_spaceship)
                    g_sprite.add(shot_spaceship)
                    sound_shot.play()

            for hit in pygame.sprite.groupcollide(g_enemy, g_shots, 1, 1):
                (x, y) = hit.rect.center
                g_sprite.add(Explosion(x, y))
                sound_explosion.play()
                points = points + (10 * level)

            for hit in pygame.sprite.groupcollide(g_main_character, g_enemy_shots, 1, 1):
                (x, y) = hit.rect.center
                g_sprite.add(Explosion(x, y))
                sound_explosion.play()
                dead = 1

            if dead == 1:
                pygame.display.quit()
                window = Window()
                window.game_over(s_points, s_level)

            temp_m += 1
            if temp_m >= 100 - (level * 5):
                enemies = Enemy(g_enemy_shots, g_sprite, sound_enemy)
                g_enemy.add(enemies)
                g_sprite.add(enemies)
                temp_m = 0
                count += 1

            if count >= 10:
                level += 1
                count = 0

            s_points = str(points)
            s_level = str(level)

            dead = g_sprite.update()

            spaceship.move(time, keys)

            screen.blit(background_image, (0, 0))

            g_sprite.clear(screen, background_image)
            g_sprite.draw(screen)

            text.render(screen, "Puntos: " + s_points, COLOR_WHITE, (10, 20))
            text.render(screen, "Nivel: " + s_level, COLOR_WHITE, (200, 20))

            pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    main()
