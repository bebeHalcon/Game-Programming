import pygame as pg
from helper import *
from setting import *

class Ultimate(pg.sprite.Sprite):
    def __init__(self, pos, init_type, player, scale, speed, offset, shoot_interval = 0.5, loops = 0):
        super().__init__()
        self.type = init_type
        self.getAssets()
        self.frame_index = 0
        self.animation_speed = speed
        self.image = self.VFX[self.frame_index]
        self.scale = scale
        self.image = pg.transform.scale(self.image, (self.image.get_size()[0] * self.scale, self.image.get_size()[1] * self.scale))
        self.rect = self.image.get_rect(midbottom = (pos[0] + offset[0], pos[1] + offset[1]))
        self.is_active = False
        self.player = player
        self.loops = loops
        self.direction = 1 if self.player.facing_right else -1
        self.shoot_interval = shoot_interval
        self.shoot_interval_value = self.shoot_interval
        self.facing_right = self.player.facing_right
        if not self.facing_right:
            self.image = pg.transform.flip(self.image, True, False)

    def getAssets(self):
        path = '../_assets/ultimate/light/'
        if True:
            path = '../_assets/ultimate/bullets/Charged/'
        self.VFX = []
        
        full_path = path
        self.VFX = readFolder(full_path)
        
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.VFX):
            if self.loops > 0:
                self.frame_index = -1
                self.loops -= 1
            else:
                if self.type == PlayerType.LIGHT():
                    self.player.is_ultimate = False
                self.kill()
        else:
            self.image = self.VFX[int(self.frame_index)]
            self.image = pg.transform.scale(self.image, (self.image.get_size()[0] * self.scale, self.image.get_size()[1] * self.scale))
            if self.type == PlayerType.DARK():
                if not self.facing_right:
                    self.image = pg.transform.flip(self.image, True, False)

        
    
    def update(self,x_shift):
        self.animate()
        self.rect.x += x_shift
        if True:
            self.rect.x += self.direction * 8
            if self.shoot_interval > 0:
                self.shoot_interval -= 0.05
            else:
                self.player.is_ultimate = False
                self.shoot_interval = self.shoot_interval_value


class Bullet(pg.sprite.Sprite):
    def __init__(self, pos, player, scale, speed, offset, shoot_interval = 0.5, loops = 0):
        super().__init__()
        self.getAssets()
        self.frame_index = 0
        self.animation_speed = speed
        self.image = self.VFX[self.frame_index]
        self.scale = scale
        self.image = pg.transform.scale(self.image, (self.image.get_size()[0] * self.scale, self.image.get_size()[1] * self.scale))
        self.rect = self.image.get_rect(midbottom = (pos[0] + offset[0], pos[1] + offset[1]))
        self.is_active = False
        self.player = player
        self.loops = loops
        self.direction = 1 if self.player.facing_right else -1
        self.shoot_interval = shoot_interval
        self.shoot_interval_value = self.shoot_interval
        self.facing_right = self.player.facing_right
        if not self.facing_right:
            self.image = pg.transform.flip(self.image, True, False)

    def getAssets(self):
        path = '../_assets/ultimate/light/'
        if self.type == PlayerType.DARK():
            path = '../_assets/ultimate/bullets/Charged/'
        self.VFX = []
        
        full_path = path
        self.VFX = readFolder(full_path)
        
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.VFX):
            if self.loops > 0:
                self.frame_index = -1
                self.loops -= 1
            else:
                if self.type == PlayerType.LIGHT():
                    self.player.is_ultimate = False
                self.kill()
        else:
            self.image = self.VFX[int(self.frame_index)]
            self.image = pg.transform.scale(self.image, (self.image.get_size()[0] * self.scale, self.image.get_size()[1] * self.scale))
            if self.type == PlayerType.DARK():
                if not self.facing_right:
                    self.image = pg.transform.flip(self.image, True, False)

        
    
    def update(self,x_shift):
        self.animate()
        self.rect.x += x_shift
        if self.type == PlayerType.DARK():
            self.rect.x += self.direction * 8
            if self.shoot_interval > 0:
                self.shoot_interval -= 0.05
            else:
                self.player.is_ultimate = False
                self.shoot_interval = self.shoot_interval_value