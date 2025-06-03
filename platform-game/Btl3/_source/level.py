import pygame as pg
from level_data import *
from helper import *
from setting import *
from tile import *
from enemy import *
from stuff import *
from player import *
import time
from rain import *
from light import *
from audio import *
from meteor import *
from boss import *
from item import *
import random

# rain setup

# light

class Level:
    def __init__(self, current_level, surface, create_overworld, update_coins, update_health, update_energy, update_boss_health):
        self.display_surface = surface 
        self.world_shift = 0
        self.current_shift = 0
        
        self.update_coins = update_coins
        self.update_boss_health = update_boss_health
        
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.coins_required = level_data['coins']
        self.current_coins = 0
        self.current_items = pg.sprite.Group()
        self.new_max_level = level_data[LevelProperties.UNLOCK()]
        
        self.old_time = time.time()
        self.delta_time = 0
        self.clock = pg.time.Clock()
        
        self.light = Light(
            screen = surface,
            path = '../_assets/light.png',
            scale = 100,
            dark_value = 250
        )
        
        player_layout = readCSVLayout(level_data[LevelType.PLAYER()])
        self.player = pg.sprite.GroupSingle()
        self.goal = pg.sprite.GroupSingle()
        self.player_setup(player_layout, update_health, update_energy)
        
        self.boss_attack = pg.sprite.Group()
        self.boss = pg.sprite.GroupSingle()
        self.boss_setup()
        
        terrain_layout = readCSVLayout(level_data[LevelType.TERRAIN()])
        self.terrain_sprites = self.createTileGroup(terrain_layout, LevelType.TERRAIN())[0]

        coin_layout = readCSVLayout(level_data[LevelType.COLLECTIBLE()])
        self.coin_sprites = self.createTileGroup(coin_layout, LevelType.COLLECTIBLE())[0]
        self.star_sprite = self.createTileGroup(coin_layout, LevelType.COLLECTIBLE())[1]

        enemy_layout = readCSVLayout(level_data[LevelType.ENEMY()])
        self.enemy_sprites = self.createTileGroup(enemy_layout, LevelType.ENEMY())[0]

        constraints_layout = readCSVLayout(level_data[LevelType.CONSTRAINTS()])
        self.constraints_sprites = self.createTileGroup(constraints_layout, LevelType.CONSTRAINTS())[0]
        
        if self.current_level != 2:
            self.back_sprites = self.createBackgroundImage(BACK_PATH)
            self.front_sprites = self.createBackgroundImage(FRONT_PATH)
            self.background_sprites = self.createBackgroundImage(BACKGROUND_PATH)
        else:
            self.back_sprites = None
            self.front_sprites = None
            self.background_sprites = self.createBackgroundImage(BACKGROUND_BOSS_PATH)
            
        
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 20, level_width, self.current_level == 2)
        
        self.explosion_sprites = pg.sprite.Group()
        
        self.rains = Rains(
            screen = surface,
            amount = 200
        )
        
        self.meteors = Meteors(
            screen = surface,
            amount = 10,
            scale = random.randint(1, 3),
            anim_speed = 0.45
        )
        
        self.loadSound()
        self.initVolume()
    
    def loadSound(self):
        self.SFX = {
            SFXType.COIN_COLLECT() : SFX('../_audio/coin_collect.wav'),
            SFXType.ENEMY_DIE() : SFX('../_audio/enemy_explosion.wav'),
            SFXType.ITEM_COLLECT() : SFX('../_audio/item.mp3')
            
        }
    
    def initVolume(self):
        self.SFX[SFXType.COIN_COLLECT()].set_volume(0.5)
        self.SFX[SFXType.ENEMY_DIE()].set_volume(0.5)
    
    def boss_setup(self):
        sprite = Boss(self.player.sprite, self.update_boss_health)
        attack_sprite = AttackField(sprite, self.player.sprite)
        melee_sprite = MeleeAttackField(sprite, self.player.sprite)
        self.boss.add(sprite)
        self.boss_attack.add(attack_sprite)
        self.boss_attack.add(melee_sprite)
    
    def player_setup(self, layout, update_health, update_energy):
        for row_idx, row in enumerate(layout):
            for col_idx, value in enumerate(row):
                x = col_idx * tile_size
                y = row_idx * tile_size
                if value == '0':
                    sprite = Player((x, y), self.display_surface, update_health, self.update_light, update_energy, self.getWorldShift)
                    self.player.add(sprite)
                    self.light.player = self.player
        
    def createBackgroundImage(self, path):
        sprite_group = pg.sprite.Group()
        sprite = StaticPng(path, self.current_level == 2)
        sprite_group.add(sprite)
        
        return sprite_group
        
    def createTileGroup(self, layout, type):
        sprite_group = pg.sprite.Group()
        star_group = pg.sprite.Group()

        for row_idx, row in enumerate(layout):
            for col_idx, value in enumerate(row):
                if value != '-1' and value != '-2':
                    x = col_idx * tile_size
                    y = row_idx * tile_size
                    
                    if type == LevelType.TERRAIN():
                        terrain_tile_list = readCutGraphics(TERRAIN_TILESET_PATH)
                        tile_surface = terrain_tile_list[int(value)]
                        sprite = StaticTile(tile_size, x, y, tile_surface, self.current_level == 2)
                    
                    if type == LevelType.COLLECTIBLE():
                        sprite = Collectible(COIN_PATH, x, y, self.current_level == 2)
                    
                    if type == LevelType.ENEMY():
                        sprite = Enemy(x, y, self.current_level == 2, self.player.sprite, self.play_enemy_vfx)
                    
                    if type == LevelType.CONSTRAINTS():
                        sprite = Tile(tile_size, x, y, self.current_level == 2)
                        
                    sprite_group.add(sprite)
                elif value == '-2':
                    if type == LevelType.COLLECTIBLE():
                        x = col_idx * tile_size
                        y = row_idx * tile_size
                        sprite = DoorTile(x, y, self.current_level == 2)
                        
                        star_group.add(sprite)
        
        return (sprite_group, star_group)
    
    def collision_enemy_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pg.sprite.spritecollide(enemy, self.constraints_sprites, False):
                enemy.reverse()
    
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    diff = abs(player.rect.left - sprite.rect.right)
                    print(player.rect.left, sprite.rect.right)
                    if diff > 50:
                        return
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    diff = abs(player.rect.right - sprite.rect.left)
                    if diff > 50:
                        return
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False
    
    def vertical_movement_collision(self):
        player = self.player.sprite
        if not player.is_attacking and not player.is_transforming:
            player.applyGravity()
        else:
            return

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    
                    diff = abs(player.rect.bottom - sprite.rect.top)

                    if diff > 50:
                        return
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                    player.get_peak = False
                elif player.direction.y < 0:
                    diff = abs(player.rect.top - sprite.rect.bottom)
                    if diff > 50:
                        return
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                    player.get_peak = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > player.gravity + 0.1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False
    
    def scroll_horizontally(self):
        player = self.player.sprite    
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 5
            player.speed = 0
        elif player_x > screen_width * 3 / 4 and direction_x > 0:
            self.world_shift = -5
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 5
    
    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            self.player.sprite.killallsounds()
            self.create_overworld(self.current_level, 0)
    
    def killallsoudns(self):
        self.player.sprite.killallsounds()
        for val in self.SFX.values():
            val.stop()
    
    def check_win(self):
        if self.current_level == 2:
            if self.boss.sprite.is_end_death:
                self.player.sprite.killallsounds()
                self.create_overworld(self.current_level, self.new_max_level)
    
    def check_star_collision(self):
        collided_coins = pg.sprite.spritecollide(self.player.sprite, self.star_sprite, True)
        if collided_coins:
            self.player.sprite.killallsounds()
            self.create_overworld(self.current_level, self.current_level + 1 if self.current_level + 1 <= 2 else 2)
    
    def check_coin_collision(self):
        collided_coins = pg.sprite.spritecollide(self.player.sprite, self.coin_sprites, True)
        if collided_coins:
            for _ in collided_coins:
                self.SFX[SFXType.COIN_COLLECT()].play()
                self.update_coins(1)

    def check_item_collision(self):
        collided_items = pg.sprite.spritecollide(self.player.sprite, self.current_items, True)
        if collided_items:
            for _ in collided_items:
                self.SFX[SFXType.ITEM_COLLECT()].play()
                if (_.type==2):
                    self.player.sprite.update_health(10)
                elif (_.type==2):
                    self.player.sprite.update_energy(10)
                _.kill()
    
    def play_enemy_vfx(self, enemy):
        explosion_sprite = ParticleEffect(enemy.rect.center, 'explosion')
        self.explosion_sprites.add(explosion_sprite)
        self.SFX[SFXType.ENEMY_DIE()].play()
    
    def check_enemy_collision(self):
        enemy_collisions = pg.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    explosion_sprite = ParticleEffect(enemy.rect.center, 'explosion')
                    self.explosion_sprites.add(explosion_sprite)
                    self.player.sprite.direction.y = -10
                    self.SFX[SFXType.ENEMY_DIE()].play()
                    if 1 == random.randint(1,15):
                            enemy_rect = enemy.rect
                            self.current_items.add(Potion(enemy_rect.left,enemy_rect.top,random.randint(1,2),False,self.player,self,enemy.speed/abs(enemy.speed)))
                    enemy.kill()
                else:
                    if self.player.sprite.is_attacking:
                        self.play_enemy_vfx(enemy)
                        
                        if 1 == random.randint(1,15):
                            enemy_rect = enemy.rect
                            self.current_items.add(Potion(enemy_rect.left,enemy_rect.top,random.randint(1,2),False,self.player,self,enemy.speed/abs(enemy.speed)))
                        enemy.kill()

                        
                    else:
                        self.player.sprite.get_damage()
    
    def update_light(self, status):
        self.light.active(status)
    
    def getWorldShift(self):
        return self.world_shift
    
    def run(self):
        self.check_death()
        self.check_win()
        self.check_coin_collision()
        self.check_enemy_collision()
        self.check_star_collision()
        self.check_item_collision()
        
        now = time.time()
        self.delta_time = now - self.old_time
        self.old_time = now
        
        self.background_sprites.draw(self.display_surface)
        self.background_sprites.update(self.world_shift, self.current_level == 2)
        
        if self.back_sprites is not None:
            self.back_sprites.draw(self.display_surface)
            self.back_sprites.update(self.world_shift, self.current_level == 2)
        
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift, self.current_level == 2)
        
        self.coin_sprites.draw(self.display_surface)
        self.coin_sprites.update(self.world_shift, self.current_level == 2)
        self.star_sprite.draw(self.display_surface)
        self.star_sprite.update(self.world_shift, self.current_level == 2)
        self.current_items.draw(self.display_surface)
        self.current_items.update(self.world_shift, self.current_level == 3)


        self.enemy_sprites.update(self.world_shift, self.current_level == 2)
        self.constraints_sprites.update(self.world_shift, self.current_level == 2)
        self.collision_enemy_reverse()
        self.enemy_sprites.draw(self.display_surface)
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)
        
        
        if self.current_level == 2:
            self.boss_attack.update()
            self.boss.update(self.delta_time)
            self.boss.draw(self.display_surface)
            # self.boss_attack.draw(self.display_surface)
        
        self.player.update(self.delta_time)
        self.player.draw(self.display_surface)
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        
        if self.front_sprites is not None:
            self.front_sprites.draw(self.display_surface)
            self.front_sprites.update(self.world_shift, self.current_level == 2)
        
        self.water.draw(self.display_surface,self.world_shift)
        if self.current_level != 2:
            self.rains.update(self.world_shift)
            self.light.update()

        if self.current_level != 2:
            self.scroll_horizontally()
        
        