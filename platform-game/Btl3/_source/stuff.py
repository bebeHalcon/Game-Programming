from setting import vertical_tile_number, tile_size, screen_width
import pygame as pg
from tile import AnimatedTile, StaticTile
from helper import readFolder
from random import choice, randint

class Water:
    def __init__(self, top, level_width, is_boss = False):
        water_start = -screen_width
        water_tile_width = 192
        tile_x_amount = int((level_width + screen_width * 2) / water_tile_width)
        self.water_sprites = pg.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            y = top
            sprite = AnimatedTile(192, x, y, '../_assets/water', is_boss)
            self.water_sprites.add(sprite)

    def draw(self,surface,shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(surface)