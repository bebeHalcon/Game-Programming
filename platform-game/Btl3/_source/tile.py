import pygame as pg
from level_data import *
from setting import *
from helper import *

class StaticPng(pg.sprite.Sprite):
    def __init__(self, path, is_boss = False):
        super().__init__()
        self.image = pg.image.load(path).convert_alpha()
        self.image = pg.transform.scale(self.image, background_png_size).convert_alpha()
        self.rect = self.image.get_rect(topleft = (0, 0))
        if is_boss:
            self.rect.x +=-40

    def update(self, offset, is_boss = False):
        if not is_boss:
            self.rect.x += offset

class Tile(pg.sprite.Sprite):
    def __init__(self, size, x, y, is_boss = False):
        super().__init__()
        self.image = pg.Surface((size, size))
        self.image = pg.transform.scale(self.image, (tile_size, tile_size)).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x, y))
        if is_boss:
            self.rect.x += -40

    def update(self, offset, is_boss = False):
        if not is_boss:
            self.rect.x += offset
    
class StaticTile(Tile):
    def __init__(self, size, x, y, surface, is_boss = False):
        super().__init__(size, x, y, is_boss)
        self.image = surface
        self.image = pg.transform.scale(self.image, (tile_size, tile_size)).convert_alpha()

class AnimatedTile(Tile):
    def __init__(self,size,x,y,path, is_boss = False):
        super().__init__(size,x,y, is_boss)
        self.frames = readFolder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.image = pg.transform.scale(self.image, (self.image.get_size()[0] * 4, self.image.get_size()[0] * 4)).convert_alpha()

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self,shift, is_boss = False):
        self.animate()
        self.rect.x += shift

class Collectible(pg.sprite.Sprite):
    def __init__(self, path, x, y, is_boss = False):
        super().__init__()
        self.getAsset()
        self.frame_idx = 0
        self.image = self.animations[self.frame_idx]
        self.image = pg.transform.scale(self.image, (64, 64)).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x, y))
        self.animation_speed = 0.25
        if is_boss:
            self.rect.x += -40
    
    def getAsset(self):
        path = '../_levels/png/coin/'
        self.animations = readFolder(path)
        
    def animate(self):
        animation = self.animations[int(self.frame_idx)]
        self.frame_idx += self.animation_speed
        if self.frame_idx >= len(self.animations):
            self.frame_idx = 0
        
        self.image = animation
        self.image = pg.transform.scale(self.image, (64, 64)).convert_alpha()
    
    def update(self, offset, is_boss = False):
        self.animate()
        if not is_boss:
            self.rect.x += offset
            
class DoorTile(pg.sprite.Sprite):
    def __init__(self, x, y, is_boss = False):
        super().__init__()
        self.getAsset()
        self.frame_idx = 0
        self.image = self.animations[self.frame_idx]
        self.image = pg.transform.scale(self.image, (250, 250)).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x, y))
        self.animation_speed = 0.25
        if is_boss:
            self.rect.x += -40
    
    def getAsset(self):
        path = '../_assets/door/'
        self.animations = readFolder(path)
        
    def animate(self):
        animation = self.animations[int(self.frame_idx)]
        self.frame_idx += self.animation_speed
        if self.frame_idx >= len(self.animations):
            self.frame_idx = 0
        
        self.image = animation
        self.image = pg.transform.scale(self.image, (250, 250)).convert_alpha()
    
    def update(self, offset, is_boss = False):
        self.animate()
        if not is_boss:
            self.rect.x += offset