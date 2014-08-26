__author__ = 'awalji'

import sys
import pygame
from pygame.constants import QUIT
from pygame.time import Clock
from pygame import Surface, display
from pygame.sprite import Sprite, RenderUpdates, spritecollide
from random import randrange

SCREEN_RES = (640, 480)

SKY_BLUE = (135, 206, 250)

TANGERINE = (255, 204, 0)

PALE_GOLDENROD = (238, 232, 170)

KELLY_GREEN = (76, 187, 23)

PIPE_RATE = 4000

pygame.init()

screen = display.set_mode(SCREEN_RES)

clock = Clock()

background = Surface(SCREEN_RES)

background.fill(SKY_BLUE)

screen.blit(background, background.get_rect())

class FlappyBox(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = Surface((30, 30))
        self.rect = self.image.get_rect()
        self.image.fill(TANGERINE)
        self.rect.centery = 240
        self.rect.left = 60

    def update(self):
        self.rect.bottom += 3

fbox = FlappyBox()

class Ground(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = Surface((640, 60))
        self.rect = self.image.get_rect()
        self.image.fill(PALE_GOLDENROD)
        self.rect.bottom = 480

ground = Ground()

class Pipe(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = Surface((60, 480))
        self.rect = self.image.get_rect()
        self.image.fill(KELLY_GREEN)
        self.rect.left = 640

    def update(self):
        self.rect.left -= 1

sprites = RenderUpdates(fbox, ground)

pipe_timer = 0

def spawn_pipes():
    global pipe_timer
    pipe_gap = randrange(95, 325)
    top_pipe = Pipe()
    top_pipe.rect.bottom = pipe_gap - 90
    bottom_pipe = Pipe()
    bottom_pipe.rect.top = pipe_gap + 90
    pipe_timer = 0
    sprites.add(top_pipe, bottom_pipe)

def collisions_detected():
    sprites_collided = [s for s in spritecollide(fbox, sprites, False) if s is not fbox]
    return len(sprites_collided) > 0

def end_game():
    print("You Hit Something!!!")

while True:

    sprites.clear(screen, background)

    for event in pygame.event.get():

        if event.type == QUIT:
            sys.exit()

    pipe_timer += clock.tick(60)

    if pipe_timer >= PIPE_RATE:
        spawn_pipes()

    sprites.update()

    if collisions_detected():
        end_game()

    sprites.draw(screen)

    display.flip()








