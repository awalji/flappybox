#!/usr/bin/env python

__author__ = 'awalji'

import sys
import pygame
from pygame.constants import QUIT, KEYUP, K_SPACE
from pygame.time import Clock
from pygame import Surface, display
from pygame.sprite import Sprite, OrderedUpdates, spritecollide
from random import randrange

SCREEN_RES = (480, 640)

SKY_BLUE = (135, 206, 250)

TANGERINE = (255, 204, 0)

TAN = (238, 207, 161)

KELLY_GREEN = (76, 187, 23)

PIPE_RATE = 1750

MAX_VELOCITY = 650

pygame.init()

screen = display.set_mode(SCREEN_RES)

clock = Clock()

background = Surface(SCREEN_RES)

background.fill(SKY_BLUE)

screen.blit(background, background.get_rect())


class FlappyBox(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = Surface((35, 35))
        self.rect = self.image.get_rect()
        self.image.fill(TANGERINE)
        self.rect.centery = SCREEN_RES[0]/2
        self.rect.left = 60
        self.vy = 0
        self.ay = MAX_VELOCITY * 4
        self.images = {'up': None, 'mid': None, 'down': None}
        for key in self.images.keys():
            self.images[key] = pygame.image.load("images/fb-%s.png" % key)
        self.animation_order = ['up', 'mid', 'down', 'mid']
        self.animation_index = 0
        self.image = self.images[self.animation_order[self.animation_index]]
        self.update_counter = 0

    def update(self, ticks):
        t = ticks / 1000.0
        self.vy += self.ay * t
        if self.vy > MAX_VELOCITY:
            self.vy = MAX_VELOCITY
        elif self.vy < -MAX_VELOCITY:
            self.vy = -MAX_VELOCITY
        self.rect.bottom += self.vy * t
        if self.update_counter % 10 == 0:
            self.animation_index = (self.animation_index + 1) % len(self.animation_order)
            self.image = self.images[self.animation_order[self.animation_index]]
        self.update_counter += 1


    def flap(self):
        self.vy -= MAX_VELOCITY

fbox = FlappyBox()


class Ground(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = Surface((SCREEN_RES[0], 60))
        self.rect = self.image.get_rect()
        self.image.fill(TAN)
        self.rect.bottom = SCREEN_RES[1]

ground = Ground()


class Pipe(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = Surface((100, SCREEN_RES[1]))
        self.rect = self.image.get_rect()
        self.image.fill(KELLY_GREEN)
        self.rect.left = SCREEN_RES[0]

    def update(self, ticks):
        self.rect.left -= 3

sprites = OrderedUpdates(fbox, ground)

pipe_timer = 0


def spawn_pipes():
    global pipe_timer
    pipe_gap = randrange(95, SCREEN_RES[1]-60-5-90)
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

        if event.type == KEYUP and event.key == K_SPACE:
            fbox.flap()

    ticks = clock.tick(60)

    pipe_timer += ticks

    if pipe_timer >= PIPE_RATE:
        spawn_pipes()

    sprites.update(ticks)

    if collisions_detected():
        end_game()

    sprites.draw(screen)

    display.flip()
