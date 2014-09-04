#!/usr/bin/env python

__author__ = 'awalji'

import sys
from random import randrange

import pygame
from pygame.constants import QUIT, KEYUP, K_SPACE
from pygame.time import Clock
from pygame import Surface, display
from pygame.sprite import Sprite, OrderedUpdates, spritecollide
from pygame.transform import flip, rotate


SCREEN_RES = (480, 640)

SKY_BLUE = (135, 206, 250)

TANGERINE = (255, 204, 0)

TAN = (238, 207, 161)

KELLY_GREEN = (76, 187, 23)

BLACK = (0,0,0)

PIPE_RATE = 1750

MAX_VELOCITY = 650

pygame.init()

screen = display.set_mode(SCREEN_RES)

clock = Clock()

background = pygame.image.load("images/background.png")

screen.blit(background, background.get_rect())

game_over = False


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
        self.rotation = 0

    def update(self, ticks):
        if not self.rect.colliderect(ground.rect):
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
        if game_over and self.rotation > -90:
            self.rotation -= 5
        self.image = rotate(self.images[self.animation_order[self.animation_index]], self.rotation)




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
    def __init__(self, top=False):
        Sprite.__init__(self)
        self.image = pygame.image.load("images/pipe.png")
        if top:
            self.image = flip(self.image, False, True)
        self.rect = self.image.get_rect()
        self.rect.left = SCREEN_RES[0]

    def update(self, ticks):
        if not game_over:
            self.rect.left -= 3
            if self.rect.right < 0:
                bg_sprites.remove(self)

bg_sprites = OrderedUpdates()
fg_sprites = OrderedUpdates(ground, fbox)

pipe_timer = 0

def spawn_pipes():
    global pipe_timer
    pipe_gap = 180
    flange_padding = 45
    pipe_gap_center = randrange((pipe_gap/2)+flange_padding, SCREEN_RES[1]-ground.rect.height-flange_padding-(pipe_gap/2))
    top_pipe = Pipe(True)
    top_pipe.rect.bottom = pipe_gap_center - (pipe_gap/2)
    bottom_pipe = Pipe()
    bottom_pipe.rect.top = pipe_gap_center + (pipe_gap/2)
    pipe_timer = 0
    bg_sprites.add(top_pipe, bottom_pipe)


def collisions_detected():
    sprites_collided = [s for s in spritecollide(fbox, bg_sprites, False)]
    ground_collided = [s for s in spritecollide(fbox, fg_sprites, False) if s is not fbox]
    return len(sprites_collided + ground_collided) > 0


def end_game():
    global game_over
    print("You Hit Something!!!")
    game_over = True

def reset_game():
    global fbox, pipe_timer, game_over
    fg_sprites.remove(fbox)
    fbox = FlappyBox()
    fg_sprites.add(fbox)
    bg_sprites.empty()
    pipe_timer = 0
    game_over = False
    screen.blit(background, (0,0))

while True:

    bg_sprites.clear(screen, background)
    fg_sprites.clear(screen, background)
    screen.blit(background, [150, 250])

    for event in pygame.event.get():

        if event.type == QUIT:
            sys.exit()

        if event.type == KEYUP and event.key == K_SPACE:
            if not game_over:
                fbox.flap()
            else:
                reset_game()

    ticks = clock.tick(60)

    pipe_timer += ticks

    if not game_over and pipe_timer >= PIPE_RATE:
        spawn_pipes()

    bg_sprites.update(ticks)
    fg_sprites.update(ticks)

    if not game_over and collisions_detected():
        end_game()

    bg_sprites.draw(screen)
    fg_sprites.draw(screen)

    if game_over:
        font = pygame.font.Font(None ,50)
        text = font.render("Game over", True, BLACK)
        screen.blit(text, [150, 250])

    display.flip()
