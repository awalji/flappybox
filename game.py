__author__ = 'awalji'

import sys
import pygame
from pygame.constants import QUIT
from pygame.time import Clock
from pygame import Surface, display
from pygame.sprite import Sprite


SCREEN_RES = (640, 480)

SKY_BLUE = (135, 206, 250)

TANGERINE = (255, 204, 0)

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
screen.blit(fbox.image, fbox.rect)

while True:

    for event in pygame.event.get():

        if event.type == QUIT:
            sys.exit()

    clock.tick(60)

    display.flip()






