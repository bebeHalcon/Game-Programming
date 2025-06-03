import pygame as pg
import random
from setting import *

class Rains(pg.sprite.Sprite):
    def __init__(self, screen, amount):
        super().__init__() 
        self.screen = screen
        self.rain_group = pg.sprite.Group()
        for _ in range(amount):
            rain = Rain()
            self.rain_group.add(rain)
    
    def update(self, x_shift):
        self.rain_group.update(x_shift)
        self.rain_group.draw(self.screen)

class Rain(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('../_levels/png/rain01.png').convert_alpha()
        self.image.set_alpha(random.randint(50, 255))
        self.rect = self.image.get_rect()
        self.speedx = -5
        self.speedy = random.randint(20,30)
        self.rect.x = random.randint(-100, screen_width + 100)
        self.rect.y = random.randint(-screen_height, -5)

    def update(self, x_shift):
        self.rect.x += x_shift
        if self.rect.bottom > screen_height:
            self.speedx = -5
            self.speedy = random.randint(20,30)
            self.rect.x = random.randint(-100, screen_width + 100)
            self.rect.y = random.randint(-screen_height, -5)
            
        self.rect.x = self.rect.x + self.speedx
        self.rect.y = self.rect.y + self.speedy     