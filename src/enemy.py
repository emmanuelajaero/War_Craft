# enemy.py

import random

import pygame

from .constants import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, sprites, enemies):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/images/enemy.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, WIDTH)
        self.rect.top = 32
        direction = [1, -1]
        self.speedx = direction[random.randint(0, 1)] * ENEMY_SPEED_X
        self.speedy = ENEMY_SPEED_Y
        self.sprites = sprites
        self.enemies = enemies

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.speedx = -ENEMY_SPEED_X
        elif self.rect.left < 0:
            self.rect.left = 0
            self.speedx = ENEMY_SPEED_X
        if self.rect.y >= HEIGHT - 10:
            self.kill()
            for i in range(1):
                enemy = Enemy(self.sprites, self.enemies)
                self.sprites.add(enemy)
                self.enemies.add(enemy)
