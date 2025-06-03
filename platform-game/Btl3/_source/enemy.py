import pygame as pg
from setting import *
from helper import *
import random

class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y, is_boss = False, player = None, vfx = None):
        super().__init__()
        self.getAsset()
        self.player = player
        self.vfx = vfx
        self.frame_idx = 0
        self.image = self.animations[self.frame_idx]
        self.image = pg.transform.scale(self.image, (65, 55)).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x, y + 17))
        self.animation_speed = 0.25
        
        self.speed = random.randint(1, 5)
    
    def move(self):
        self.rect.x += self.speed
    
    def flip(self):
        if self.speed < 0:
            self.image = pg.transform.flip(self.image, True, False)
    
    def reverse(self):
        self.speed *= -1
    
    def getAsset(self):
        path = '../_assets/enemy'
        self.animations = readFolder(path)
        
    def animate(self):
        animation = self.animations[int(self.frame_idx)]
        self.frame_idx += self.animation_speed
        if self.frame_idx >= len(self.animations):
            self.frame_idx = 0
        
        self.image = animation
        self.image = pg.transform.scale(self.image, (65, 55)).convert_alpha()
    
    def collide(self):
        collided_bullet = pg.sprite.spritecollide(self, self.player.VFX_sprites, False)
        if collided_bullet:
            self.vfx(self)
            self.kill()
    
    def update(self, offset, is_boss = False):
        self.collide()
        self.animate()
        self.flip()
        self.move()
        self.rect.x += offset