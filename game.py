__author__ = 'awalji'

import sys
import pygame
from pygame.constants import QUIT
from pygame.time import Clock
from pygame import Surface, display


SCREEN_RES = (640, 480)

SKY_BLUE = (135, 206, 250)

pygame.init()

screen = display.set_mode(SCREEN_RES)

clock = Clock()

background = Surface(SCREEN_RES)

background.fill(SKY_BLUE)

screen.blit(background, background.get_rect())


while True:

    for event in pygame.event.get():

        if event.type == QUIT:
            sys.exit()

    clock.tick(60)

    display.flip()






