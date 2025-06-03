import pygame as pg
import random
from helper import *
from setting import *
from particle import *
from math import sin
from audio import *
from ultimate import *

class MeleeAttackField(pg.sprite.Sprite):
    def __init__(self, boss, player):
        super().__init__()
        self.image = pg.image.load('../_assets/boss/field_of_attack/rect.png').convert_alpha()
        self.boss = boss
        self.player = player
        self.rect = self.image.get_rect(center = (screen_width / 2 - 50, 300))
        self.image = pg.transform.scale(self.image, (300, 400))
    
    def update(self):
        if self.boss.is_dealing_melee_attack:
            collide = pg.Rect.colliderect(self.rect, self.player.rect)
            if collide:
                self.player.get_damage(-10)
class AttackField(pg.sprite.Sprite):
    def __init__(self, boss, player):
        super().__init__()
        self.image = pg.image.load('../_assets/boss/field_of_attack/rect.png').convert_alpha()
        self.boss = boss
        self.player = player
        self.rect = self.image.get_rect(center = (screen_width / 2 - 125, 650))
        self.image = pg.transform.scale(self.image, (400, 150))
    
    def update(self):
        if self.boss.is_dealing_range_attack:
            collide = pg.Rect.colliderect(self.rect, self.player.rect)
            if collide:
                self.player.get_damage(-20)
        if self.boss.is_dealing_special_attack:
            collide = pg.Rect.colliderect(self.rect, self.player.rect)
            if collide:
                self.player.get_damage(-35)

class Boss(pg.sprite.Sprite):
    def __init__(self, player, update_health):
        super().__init__()
        self.getAssets()
        self.state = State.LIE_STATIC()
        self.frame_idx = 0
        self.image = self.animations[self.state][self.frame_idx]
        self.image = pg.transform.scale(self.image, (boss_sizes[self.state][0] * boss_scale, boss_sizes[self.state][1] * boss_scale))
        self.rect = self.image.get_rect(topleft = boss_init_position)
        self.facing_right = True
        self.is_wakeup = False
        self.position = boss_init_position
        self.player = player
        self.update_health = update_health
        self.current_health = 1000
        
        self.wait_move_interval_value = 3
        self.wait_move_interval = self.wait_move_interval_value
        self.move_speed = 8
        self.is_moving = False
        self.is_attacking = False

        self.attack_position = (0, 0)
        self.attack_facing = 1
        self.attack_perform = False
        self.attack_time = 0
        self.attack_start_time = 0
        self.attack_idx = -1
        self.is_moving = False
        
        self.is_dealing_melee_attack = False
        self.is_dealing_range_attack = False
        self.is_dealing_special_attack = False
        
        self.is_invincible = False
        self.invinciblity_duration = 1000
        self.hurt_time = 0
        
        self.is_death = False
        self.is_end_death = False
        
        self.loadSound()
    
    def loadSound(self):
        self.SFX = {
            SFXType.BOSS_ATTACK01() : SFX('../_audio/boss_attack1_SFX.wav', 0.75),
            SFXType.BOSS_ATTACK02() : SFX('../_audio/boss_attack2_sfx.wav', 0.75),
            SFXType.BOSS_ATTACK03() : SFX('../_audio/boss_attack3_sfx.wav', 0.75),
            SFXType.BOSS_PRE_ATTACK03() : SFX('../_audio/boss_preattack3_sfx.wav', 0.75),
            SFXType.BOSS_DIE() : SFX('../_audio/boss_die.wav', 0.75),
            SFXType.BOSS_AWAKE() : SFX('../_audio/boss_awake.wav', 0.75)
        }
    
    def killallsounds(self):
        for val in self.SFX.values():
            val.stop()
    
    def getAssets(self):
        path_Light = '../_assets/boss/'
        self.animations = {
            State.IDLE() : [],
            State.RUN() : [],
            State.ATTACK01() : [],
            State.ATTACK02() : [],
            State.ATTACK03() : [],
            State.AWAKE() : [],
            State.LIE_STATIC() : [],
            State.NOT_ATTACK() : [],
            State.DIE() : []
        }
        
        for animation in self.animations.keys():
            # print(animation.value)
            full_path = path_Light + animation
            self.animations[animation] = readFolder(full_path)
    
    def resetDealingDamage(self):
        self.is_dealing_melee_attack = False
        self.is_dealing_range_attack = False
        self.is_dealing_special_attack = False
    
    def animate(self):
        if self.is_end_death:
            return
        animation = self.animations[self.state]
        self.frame_idx += boss_anim_speed[self.state]
        if self.state == State.ATTACK01():
            if 11 - boss_anim_speed[self.state] <= self.frame_idx <= 11 + boss_anim_speed[self.state]:
                self.SFX[SFXType.BOSS_ATTACK01()].play()
            if 11 <= self.frame_idx <= 16:
                self.is_dealing_melee_attack = True
        if self.state == State.ATTACK02():
            if 10 - boss_anim_speed[self.state] <= self.frame_idx <= 10 + boss_anim_speed[self.state]:
                self.SFX[SFXType.BOSS_ATTACK02()].play()
            if 10 <= self.frame_idx < 12:
                self.is_dealing_range_attack = True
        if self.state == State.ATTACK03():
            if 6 - boss_anim_speed[self.state] <= self.frame_idx <= 6 + boss_anim_speed[self.state]:
                self.SFX[SFXType.BOSS_PRE_ATTACK03()].play()
            if 32 - boss_anim_speed[self.state] <= self.frame_idx <= 32 + boss_anim_speed[self.state]:
                self.SFX[SFXType.BOSS_ATTACK03()].play()
            if 32 <= self.frame_idx < 35:
                self.is_dealing_special_attack = True
        if self.frame_idx >= len(animation):
            self.frame_idx = 0
            self.resetDealingDamage()
            if self.state == State.DIE():
                self.is_end_death = True
            if self.state == State.ATTACK01() or self.state == State.ATTACK02() or self.state == State.ATTACK03() or self.state == State.NOT_ATTACK():
                self.is_attacking = False
                self.state = State.IDLE()
            if not boss_anim_loop[self.state]:
                self.state = State.IDLE()
            if self.state == State.AWAKE():
                self.state = State.IDLE()
        # else:
        image = animation[int(self.frame_idx)]
        image = pg.transform.scale(image, (boss_sizes[self.state][0] * boss_scale, boss_sizes[self.state][1] * boss_scale))

        if self.facing_right:
            self.image = image
        else:
            flipped_image = pg.transform.flip(image, True, False)
            self.image = flipped_image
            
        if self.is_invincible:
            alpha = self.sin_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    
    def wakeup(self):
        self.SFX[SFXType.BOSS_AWAKE()].play()
        self.state = State.AWAKE()
        self.frame_idx =  0
    
    def get_movement_data(self, currentx, currenty, targetx, targety):
        start = pg.math.Vector2(currentx, currenty)
        end = pg.math.Vector2(targetx, targety)
        new_vec = end - start
        if new_vec.length() == 0: return new_vec
        else: return new_vec.normalize()
    
    def attack(self, attackIdx, position, facing, perform, time):
        if self.is_death:
            return
        direction = self.get_movement_data(self.rect.centerx, self.rect.centery, position[0], position[1])
        if abs(self.position[0] - position[0]) <= 55:
            direction = pg.math.Vector2(0, 0)
        self.position += direction * 50
        self.rect.center = self.position
        self.facing_right = True if facing == 1 else False
        remaining_time = pg.time.get_ticks() - self.attack_start_time
        if remaining_time >= time:
            self.endattack()
            
        # * attack code goes bruhhhhhhhhhhh
        if not perform:
            return 
        if attackIdx == 1:
            self.state = State.ATTACK01()
        elif attackIdx == 2:
            self.state = State.ATTACK02()
        elif attackIdx == 3:
            self.state = State.ATTACK03()
        elif attackIdx == 4:
            self.state = State.NOT_ATTACK()
        
    
    def endattack(self):
        self.is_attacking = False
    
    def getCollide(self):
        collided_bullet = pg.sprite.spritecollide(self, self.player.VFX_sprites, False)
        if collided_bullet:
            if not self.is_invincible:
                damage = -50
                self.update_health(damage)
                self.current_health += damage
                if self.current_health <= 0:
                    self.death()
                self.is_invincible = True
                self.hurt_time = pg.time.get_ticks()
        collide = pg.Rect.colliderect(self.player.rect, self.rect)
        if collide:
            if self.player.is_attacking:
                if not self.is_invincible:
                    # self.SFX[SFXType.HIT()].play()
                    if self.player.is_ultimate and self.player.type == PlayerType.LIGHT():
                        damage = -100
                    else:
                        damage = -20
                    self.update_health(damage)
                    self.current_health += damage
                    if self.current_health <= 0:
                        self.death()
                    self.is_invincible = True
                    self.hurt_time = pg.time.get_ticks()
    
    def sin_value(self):
        value = sin(pg.time.get_ticks())
        if value >= 0 : return 255
        else: return 100
    
    def death(self):
        self.SFX[SFXType.BOSS_DIE()].play()
        self.frame_idx = 0
        self.is_death = True
        self.state = State.DIE()
    
    def invincibility_timer(self):
        if self.is_invincible: 
            current_time = pg.time.get_ticks()
            if current_time - self.hurt_time >= self.invinciblity_duration:
                self.is_invincible = False
    
    def update(self, delta_time):
        keys = pg.key.get_pressed()
        self.animate()
        self.getCollide()
        self.invincibility_timer()
        self.sin_value()
        
        if not self.is_death:
            if self.is_wakeup:
                if self.state == State.IDLE():
                    if not self.is_attacking:
                        self.attack_idx = random.randint(1, 4)
                    else:
                        self.attack_idx = -1
                
                    if self.attack_idx != -1 and not self.is_attacking:
                        self.attack_start_time = pg.time.get_ticks() + 2000
                        self.is_attacking = True
                        self.is_moving = True
                        
                        self.frame_idx = 0
                        attackString = 'attack ' + str(self.attack_idx)
                        attack_state_idx = random.randint(0, 2)
                        self.attack_position = boss_attack_state[attackString][attack_state_idx]['position']
                        self.attack_facing = boss_attack_state[attackString][attack_state_idx]['facing']
                        self.attack_perform = boss_attack_state[attackString][attack_state_idx]['attack']
                        self.attack_time = boss_attack_state[attackString][attack_state_idx]['time']
                            
                    
                if self.is_attacking:
                    self.attack(self.attack_idx, self.attack_position, self.attack_facing, self.attack_perform, self.attack_time)
            else:
                if self.rect.colliderect(self.player.rect):
                    self.is_wakeup = True
                    self.wakeup()
                    