import pygame as pg
from setting import *

class Light(pg.sprite.Sprite):
    def __init__(self, screen, path, scale, dark_value, player = None):
        super().__init__()
        self.player = player
        self.screen = screen
        self.scale = scale
        self.image = pg.image.load(path).convert_alpha()
        self.image = pg.transform.scale(self.image, (self.image.get_size()[0] * self.scale, self.image.get_size()[1] * self.scale))
        self.rect = self.image.get_rect(bottomright = (0, 0))
        self.dark_value = dark_value
        self.status = True
    
    def update(self): 
        if self.player is None:
            return
        if not self.status:
            filter = pg.surface.Surface((screen_width, screen_height))
            filter.fill(pg.color.Color(self.dark_value, self.dark_value, self.dark_value, 255))
            self.rect = self.image.get_rect(bottomright = (self.player.sprite.rect.centerx, self.player.sprite.rect.centery))
            light_position = self.rect.center
            filter.blit(self.image, light_position, special_flags=pg.BLEND_RGBA_SUB)
            self.screen.blit(filter, (0, 0), special_flags=pg.BLEND_RGBA_SUB)
    
    def active(self, status):
        self.status = status
            