from csv import reader
import pygame as pg
from setting import *
from os import walk

def readFolder(path):
    surface_list = []
    for _,__,img_files in walk(path):
        for img in img_files:
            full_path = path + '/' + img
            img_surf = pg.image.load(full_path).convert_alpha()
            surface_list.append(img_surf)
    return surface_list

def readCSVLayout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map

def readCutGraphics(path):
    surface = pg.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_real_size)
    tile_num_y = int(surface.get_size()[1] / tile_real_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_real_size
            y = row * tile_real_size
            new_surface = pg.Surface((tile_real_size, tile_real_size), flags=pg.SRCALPHA)
            new_surface.blit(surface, (0, 0), pg.Rect(x, y, tile_real_size, tile_real_size))
            cut_tiles.append(new_surface)
            
    return cut_tiles