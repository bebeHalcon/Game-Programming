import pygame as pg
import random
from setting import *
from helper import *
from light import *

class Meteors(pg.sprite.Sprite):
    def __init__(self, screen, amount, scale, anim_speed):
        super().__init__() 
        self.screen = screen
        self.meteor_group = pg.sprite.Group()
        for _ in range(amount):
            meteor = Meteor(screen, scale, anim_speed)
            self.meteor_group.add(meteor)
    
    def update(self, x_shift):
        self.meteor_group.update(x_shift)
        self.meteor_group.draw(self.screen)

class Meteor(pg.sprite.Sprite):
    def __init__(self, screen, scale, anim_speed):
        super().__init__()
        self.getAssets()
        self.frame_index = 0
        self.image = self.VFX[self.frame_index]
        self.image.set_alpha(random.randint(50, 255))
        self.rect = self.image.get_rect()
        self.speedx = -2
        self.speedy = random.randint(1,1)
        self.rect.x = random.randint(0, screen_width + 10)
        self.rect.y = random.randint(-screen_height, -5)
        self.scale = scale
        self.animation_speed = anim_speed
        
    def getAssets(self):
        path = '../_assets/meteor/'
        self.VFX = []
        
        full_path = path
        self.VFX = readFolder(full_path)
    
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.VFX):
            self.frame_index = -1
        else:
            self.image = self.VFX[int(self.frame_index)]
            self.image = pg.transform.scale(self.image, (self.image.get_size()[0] * self.scale, self.image.get_size()[1] * self.scale))
    
    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift
        if self.rect.bottom > screen_height:
            self.speedx = -2
            self.speedy = random.randint(1,1)
            self.rect.x = random.randint(0, screen_width + 10)
            self.rect.y = random.randint(-screen_height, -5)
            
        self.rect.x = self.rect.x + self.speedx
        self.rect.y = self.rect.y + self.speedy     