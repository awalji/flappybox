__author__ = 'awalji'

import sys
import pygame
from pygame.constants import QUIT
from pygame.time import Clock


SCREEN_RES = (640, 480)

pygame.init()

screen = pygame.display.set_mode(SCREEN_RES)

clock = Clock()

while True:

    for event in pygame.event.get():

        if event.type == QUIT:
            sys.exit()

    clock.tick(60)

