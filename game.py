__author__ = 'awalji'

import sys
import pygame
from pygame.constants import QUIT
from pygame.time import Clock
from pygame import Surface, display
from pygame.sprite import Sprite, RenderUpdates

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

while True:

    sprites.clear(screen, background)

    for event in pygame.event.get():

        if event.type == QUIT:
            sys.exit()

    pipe_timer += clock.tick(60)

    if pipe_timer >= PIPE_RATE:
        top_pipe = Pipe()
        top_pipe.rect.bottom = 150
        bottom_pipe = Pipe()
        bottom_pipe.rect.top = 330
        pipe_timer = 0
        sprites.add(top_pipe, bottom_pipe)

    sprites.update()

    sprites.draw(screen)

    display.flip()






