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

BLACK = (0,0,0)

PIPE_RATE = 1750

SCROLL_RATE = 3

MAX_VELOCITY = 650

pygame.init()

screen = display.set_mode(SCREEN_RES)

clock = Clock()

background = pygame.image.load("images/background.png").convert()

screen.blit(background, background.get_rect())

game_over = False

score = 0

pipe_pairs = []

pipes_entered = []


class FlappyBox(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = Surface((35, 35))
        self.rect = self.image.get_rect()
        self.rect.centery = SCREEN_RES[0]/2
        self.rect.left = 60
        self.vy = 0
        self.ay = MAX_VELOCITY * 4
        self.images = {'up': None, 'mid': None, 'down': None}
        for key in self.images.keys():
            self.images[key] = pygame.image.load("images/fb-%s.png" % key).convert_alpha()
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
            if self.rect.bottom < 0:
                self.rect.bottom = 0
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
        self.ground_image = pygame.image.load("images/ground.png").convert()
        self.rect.bottom = SCREEN_RES[1]
        self.boundary = SCREEN_RES[0]
        self.left_rect = self.image.get_rect()
        self.right_rect = self.image.get_rect()

        self.update()

    def update(self, *args):
        if not game_over:
            self.boundary = (self.boundary - SCROLL_RATE) % SCREEN_RES[0]
            self.left_rect.right = self.right_rect.left = self.boundary
            self.image.blit(self.ground_image, self.left_rect)
            self.image.blit(self.ground_image, self.right_rect)

ground = Ground()


class GameOverText(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        font = pygame.font.Font(None, 50)
        self.image = font.render("Game Over", True, BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = background.get_rect().centerx
        self.rect.centery = background.get_rect().centery

game_over_text = GameOverText()

class ScoreText(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.font = pygame.font.Font(None, 50)

    def update(self, ticks):
        self.image = self.font.render(str(score), True, BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = background.get_rect().centerx
        self.rect.centery = background.get_rect().centery - 150

score_text = ScoreText()


class Pipe(Sprite):
    def __init__(self, top=False):
        Sprite.__init__(self)
        self.image = pygame.image.load("images/pipe.png").convert_alpha()
        if top:
            self.image = flip(self.image, False, True)
        self.rect = self.image.get_rect()
        self.rect.left = SCREEN_RES[0]

    def update(self, ticks):
        global pipe_pairs
        if not game_over:
            self.rect.left -= SCROLL_RATE
            if self.rect.right < 0:
                bg_sprites.remove(self)
                pipe_pairs = [pair for pair in pipe_pairs if self not in pair]


bg_sprites = OrderedUpdates()
fg_sprites = OrderedUpdates(ground, fbox)
text_sprites = OrderedUpdates(score_text)

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
    pipe_pairs.append((top_pipe, bottom_pipe))


def collisions_detected():
    sprites_collided = [s for s in spritecollide(fbox, bg_sprites, False)]
    ground_collided = [s for s in spritecollide(fbox, fg_sprites, False) if s is not fbox]
    return len(sprites_collided + ground_collided) > 0

def detect_pipe_entry():
    global pipes_entered
    entries = [pair for pair in pipe_pairs if fbox.rect.right > pair[0].rect.left and fbox.rect.right <= pair[0].rect.right and not pair in pipes_entered]
    pipes_entered += entries

def compute_score():
    global score, pipes_entered
    for pair in pipes_entered:
        if fbox.rect.left > pair[0].rect.right:
            score += 1
            pipes_entered.remove(pair)

def end_game():
    global game_over
    text_sprites.add(game_over_text)
    game_over = True


def reset_game():
    global fbox, pipe_timer, game_over, score, pipes_entered, pipe_pairs
    fg_sprites.remove(fbox)
    fbox = FlappyBox()
    fg_sprites.add(fbox)
    bg_sprites.empty()
    pipe_timer = 0
    pipes_entered = []
    pipe_pairs = []
    game_over = False
    score = 0
    text_sprites.remove(game_over_text)

while True:

    bg_sprites.clear(screen, background)
    fg_sprites.clear(screen, background)
    text_sprites.clear(screen, background)

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
    text_sprites.update(ticks)

    detect_pipe_entry()
    compute_score()

    if not game_over and collisions_detected():
        end_game()

    bg_sprites.draw(screen)
    fg_sprites.draw(screen)
    text_sprites.draw(screen)

    display.flip()
