import pygame as pg
from setting import *
from helper import *
import random


class Potion(pg.sprite.Sprite):
    def __init__(self, x, y, type, is_boss = False, player = None, level = None, dir = 1):
        super().__init__()
        self.type = type
        self.getAsset()
        self.player = player
        self.on_ground = 0
        self.level = level
        self.image = self.animations
        self.image = pg.transform.scale(self.image, (48, 48)).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x-15*dir, y))
        self.animation_speed = 0.25
        
    def draw(self):
        scene = self.level.world_shift

        self.image.blit(scene,)

    def move(self):
        self.rect.x += self.speed
    
    def flip(self):
        if self.speed < 0:
            self.image = pg.transform.flip(self.image, True, False)
    
    def reverse(self):
        self.speed *= -1
    
    def getAsset(self):
        
        if self.type==1:
            path = '../_assets/items/heart.png'
            self.animations = pg.image.load(path)

        elif self.type==2:
            path = '../_assets/items/bluepotion.png'
            self.animations = pg.image.load(path)

        
    def animate(self):
        animation = self.animations        
        self.image = animation
        self.image = pg.transform.scale(self.image, (48, 48)).convert_alpha()
    
    def collide(self):
        collided_bullet = pg.sprite.spritecollide(self, self.player.VFX_sprites, False)
        if collided_bullet:
            self.vfx(self)
            self.kill()
    
    def update(self, offset, is_boss = False):
        self.animate()
        if not is_boss:
            self.rect.x += offset