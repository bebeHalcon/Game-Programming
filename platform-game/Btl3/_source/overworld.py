import pygame as pg
from level_data import *
from setting import *

class Node(pg.sprite.Sprite):
    def __init__(self, position, status, icon_speed, idx):
        super().__init__()
        self.image = pg.Surface((100, 80))
        if status:
            self.image = pg.image.load(levels[idx][LevelProperties.NODE_PNG()])
            self.image = pg.transform.scale(self.image, (200, 200))
        else:
            self.image = pg.image.load(levels[idx][LevelProperties.NODE_LOCK()])
            self.image = pg.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect(center = position)
        self.detection_zone = pg.Rect(self.rect.centerx - (icon_speed / 2), self.rect.centery - (icon_speed / 2), icon_speed, icon_speed)

class Icon(pg.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.image = pg.image.load(ICON_PATH)
        self.image = pg.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center = position)
        self.is_right = True
        flipped_image = pg.transform.flip(self.image, True, False)
        self.image = flipped_image
    
    def update(self):
        self.rect.center = self.position
    
    def flip(self):
        flipped_image = pg.transform.flip(self.image, True, False)
        self.image = flipped_image

class Overworld:
    def __init__(self, start_level, max_level, surface, create_level):
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level
        
        self.move_direction = pg.math.Vector2(0, 0)
        self.speed = 18
        self.is_moving = False
        
        self.setup_nodes()
        self.setup_icon()
    
    def setup_nodes(self):
        self.nodes = pg.sprite.Group()
        
        for node_idx, node_data in enumerate(levels.values()):
            if node_idx <= self.max_level:
                node_sprite = Node(node_data[LevelProperties.NODE_POS()], True, self.speed, node_idx)
            else:
                node_sprite = Node(node_data[LevelProperties.NODE_POS()], False, self.speed, node_idx)
            self.nodes.add(node_sprite)

    def draw_path(self):
        points = [node[LevelProperties.NODE_POS()] for idx, node in enumerate(levels.values()) if idx <= self.max_level]
        if len(points) < 2:
            return
        pg.draw.lines(self.display_surface, 'white', False, points, width=30)
        pg.draw.lines(self.display_surface, 'black', False, points, width=20)

    def setup_icon(self):
        self.icon = pg.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def gather_input(self):
        keys = pg.key.get_pressed()
        
        if not self.is_moving:
            if keys[pg.K_RIGHT] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data(1)
                self.current_level += 1
                self.is_moving = True
                if not self.icon.sprite.is_right:
                    self.icon.sprite.flip()
                self.icon.sprite.is_right = True
            elif keys[pg.K_LEFT] and self.current_level > 0:
                self.move_direction = self.get_movement_data(-1)
                self.current_level -= 1
                self.is_moving = True
                if self.icon.sprite.is_right:
                    self.icon.sprite.flip()
                self.icon.sprite.is_right = False
            elif keys[pg.K_RETURN]:
                self.create_level(self.current_level)
    
    def restart(self):
        self.create_level(self.current_level)
    
    def get_movement_data(self, move_factor):
        start = pg.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        idx = self.current_level + move_factor 
        if idx > len(self.nodes.sprites()) - 1:
            idx = len(self.nodes.sprites()) - 1
        if idx < 0:
            idx = 0
        end = pg.math.Vector2(self.nodes.sprites()[idx].rect.center)
        vec = end - start
        if vec.length() == 0:
            return vec
        return (end - start).normalize()
    
    def update_icon_position(self):
        if self.is_moving and self.move_direction:
            self.icon.sprite.position += self.move_direction * self.speed;
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.position):
                self.is_moving = False
                self.move_direction = pg.math.Vector2(0, 0)

    def run(self):
        self.gather_input()
        self.update_icon_position()
        self.draw_path()
        self.nodes.draw(self.display_surface)
        self.icon.update()
        self.icon.draw(self.display_surface)