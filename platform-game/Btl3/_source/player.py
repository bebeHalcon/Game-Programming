import pygame as pg
from helper import *
from setting import *
from particle import *
from math import sin
from audio import *
from ultimate import *

class Player(pg.sprite.Sprite):
    def __init__(self, position, surf, update_health, update_light, update_energy, world_shift):
        super().__init__()
        self.display_surf = surf
        self.getAssets()
        self.frame_idx = 0
        self.type = PlayerType.LIGHT()
        self.image = self.animations_Light[State.IDLE()][self.frame_idx]
        self.image = pg.transform.scale(self.image, (player_sizes[self.type][State.IDLE()][0] * player_scale, player_sizes[self.type][State.IDLE()][1] * player_scale))
        imrect = self.image.get_rect(topleft = position)
        self.rect = pg.Rect(imrect.left, imrect.top+10,imrect.width,imrect.height-10)
        self.state = State.IDLE()
        self.facing_right = True
        self.on_ground = False 
        self.on_left = False
        self.on_right = False
        self.on_ceiling = False
        self.is_attacking = False
        self.attack_idx = 0
        self.attack_buffer = 1.5
        self.attack_buffer_counter = 1.5
        self.is_transforming = False
        
        self.update_health = update_health
        self.update_energy = update_energy
        self.update_light = update_light
        self.update_light(False)

        # move
        self.direction = pg.math.Vector2(0, 0)
        self.speed = 5
        self.gravity = 0.8
        self.jump_short_speed = -15.0
        self.jump_speed = -8.0
        self.max_jump_speed = -11.0
        self.jump_buffer = -1.0
        self.get_peak = False
        
        self.particle = pg.sprite.GroupSingle()
        particle = VFX_Transform(position, self.type, self)
        self.particle.add(particle)
        
        self.is_invincible = False
        self.invinciblity_duration = 1250
        self.hurt_time = 0
        
        self.loadSound()
        
        self.SFX[SFXType.RUN()].playloop()
        
        self.current_energy = 0
        self.max_energy = 100
        self.can_transform = False
        
        self.increase_factor = 0.05
        self.decrease_factor = -0.1
        
        self.VFX_sprites = pg.sprite.Group()
        self.is_ultimate = False
        
        self.worldShift = world_shift
        self.ultimate_cost = {
            PlayerType.LIGHT() : 40,
            PlayerType.DARK() : 40,
        }
    
    def loadSound(self):
        self.SFX = {
            SFXType.RUN() : SFX('../_audio/run.wav', 0.15),
            SFXType.JUMP() : SFX('../_audio/jump.wav', 0.6),
            SFXType.SWORD() : SFX('../_audio/sword_splash.wav', 0.75),
            SFXType.HIT() : SFX('../_audio/player_hit_by_enemy.wav', 0.75),
            SFXType.TRANSFORMATION() : SFX('../_audio/transformation_02.wav', 0.5),
            SFXType.ULTIMATE01() : SFX('../_audio/ultimate01.wav', 0.75),
            SFXType.ULTIMATE02() : SFX('../_audio/bullet_shoot.wav', 0.5),
        }
    
    def killallsounds(self):
        for val in self.SFX.values():
            val.stop()
    
    def getAssets(self):
        path_Light = '../_assets/Character/'
        path_Dark = '../_assets/Dark/Dark/'
        self.animations_Light = {
            State.IDLE() : [],
            State.RUN() : [],
            State.JUMP() : [],
            State.FALL() : [],
            State.ATTACK01() : [],
            State.ATTACK02() : [],
            State.ATTACK03() : [],
            State.TRANSFORM() : []
        }
        self.animations_Dark = {
            State.IDLE() : [],
            State.RUN() : [],
            State.JUMP() : [],
            State.FALL() : [],
            State.ATTACK01() : [],
            State.ATTACK02() : [],
            State.ATTACK03() : [],
            State.TRANSFORM() : []
        }
        self.animations = {
            PlayerType.LIGHT() : self.animations_Light,
            PlayerType.DARK() : self.animations_Dark
        }
        
        self.attack_states = [
            State.ATTACK01(),
            State.ATTACK02(),
            State.ATTACK03()
        ]
        
        for animation in self.animations_Light.keys():
            # print(animation.value)
            full_path = path_Light + animation
            self.animations_Light[animation] = readFolder(full_path)
        for animation in self.animations_Dark.keys():
            # print(animation.value)
            full_path = path_Dark + animation
            self.animations_Dark[animation] = readFolder(full_path)
    
    def animate(self):
        animation = self.animations[self.type][self.state]
        self.frame_idx += player_anim_speed[self.type][self.state]
        if self.frame_idx >= len(animation):
            self.frame_idx = 0
            if self.is_transforming:
                self.is_transforming = False
                if self.type == PlayerType.LIGHT():
                    self.type = PlayerType.DARK()
                    self.update_light(True)
                else:
                    self.type = PlayerType.LIGHT()
                    self.get_peak = False
                    self.update_light(False)
                self.state = State.IDLE()
            if self.is_attacking:
                self.is_attacking = False
                #print(self.rect.midbottom)
                imrect = self.image.get_rect(midbottom = (self.rect.midbottom[0], self.rect.midbottom[1]))
                self.rect = pg.Rect(imrect.left, imrect.top+10,imrect.width,imrect.height-10)
        
        image = animation[int(self.frame_idx)]
        image = pg.transform.scale(image, (player_sizes[self.type][self.state][0] * player_scale, player_sizes[self.type][self.state][1] * player_scale))

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
        
        if self.is_transforming:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ground and self.on_right:
            imrect = self.image.get_rect(bottomright = self.rect.bottomright)
            self.rect = pg.Rect(imrect.left, imrect.top+10,imrect.width,imrect.height-10)
        elif self.on_ground and self.on_left:
            imrect = self.image.get_rect(bottomleft = self.rect.bottomleft)
            self.rect = pg.Rect(imrect.left, imrect.top+10,imrect.width,imrect.height-10)
        elif self.on_ground:
            imrect = self.image.get_rect(midbottom = self.rect.midbottom)
            self.rect = pg.Rect(imrect.left, imrect.top+10,imrect.width,imrect.height-10)
            
            
        elif self.on_ceiling and self.on_right:
            imrect = self.image.get_rect(topright = self.rect.topright)
            self.rect = pg.Rect(imrect.left, imrect.top-10,imrect.width,imrect.height-10)
        elif self.on_ceiling and self.on_left:
            imrect = self.image.get_rect(topleft = self.rect.topleft)
            self.rect = pg.Rect(imrect.left, imrect.top-10,imrect.width,imrect.height-10)
            
        elif self.on_ceiling:
            imrect = self.image.get_rect(midtop = self.rect.midtop)
            self.rect = pg.Rect(imrect.left, imrect.top-10,imrect.width,imrect.height-10)
        

    
    def gatherInput(self):
        keys = pg.key.get_pressed()
        
        if self.is_transforming:
            return
        if self.is_attacking:
            return
        
        if keys[pg.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pg.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0 
       #print(self.direction.x)
        if self.direction.x != 0 and self.on_ground:
            self.SFX[SFXType.RUN()].unmute()
        else:
            self.SFX[SFXType.RUN()].mute()
        
        if not self.can_transform and self.type == PlayerType.DARK() and self.on_ground:
            self.SFX[SFXType.TRANSFORMATION()].play()
            self.transform()
        
        if keys[pg.K_z] and not self.is_attacking and not self.is_ultimate:
            self.ultimate()
            
        if keys[pg.K_x] and self.on_ground and not self.is_transforming and self.can_transform:
            self.SFX[SFXType.TRANSFORMATION()].play()
            self.transform()
        if keys[pg.K_c] and not self.is_attacking and self.on_ground and not self.is_transforming:
            self.attack()
            self.direction.x = 0
        if self.type == PlayerType.LIGHT():
            if keys[pg.K_SPACE]:
                if self.on_ground:
                    self.jump()
        elif self.type == PlayerType.DARK():
            if keys[pg.K_SPACE]:
                if self.on_ground:
                    self.jump()
                elif not self.get_peak:
                    self.long_jump()
    
    def getState(self):
        if self.is_transforming:
            self.state = State.TRANSFORM()
        elif self.is_attacking:
            self.state = self.attack_states[self.attack_idx]
        elif self.direction.y < 0:
            self.state = State.JUMP()
        elif self.direction.y > self.gravity + 0.1:
            self.state = State.FALL()
        else:
            if self.direction.x != 0:
                self.state = State.RUN()
            else:
                self.state = State.IDLE()
    
    def applyGravity(self):
        if self.is_transforming:
            return
        if self.is_attacking:
            return
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
    
    def jump(self):
        self.SFX[SFXType.JUMP()].play()
        self.direction.y = self.jump_speed if self.type == PlayerType.DARK() else self.jump_short_speed
    
    def long_jump(self):
        y_val = self.direction.y
        y_buff = self.jump_buffer
        y_val = y_val + y_buff
        if y_val < self.max_jump_speed:
            self.get_peak = True
            y_val = self.max_jump_speed
        self.direction.y = y_val

    def countdownAttackBuffer(self, delta_time):
        if self.attack_buffer_counter > 0:
            self.attack_buffer_counter -= delta_time
        else:
            self.attack_idx = 0
            self.attack_buffer_counter = self.attack_buffer
            
    def transform(self):
        self.particle.sprite.frame_idx = 0
        self.frame_idx = 0
        self.direction.x = 0
        self.is_transforming = True 
    
    def attack(self):
        self.SFX[SFXType.SWORD()].play()
        self.frame_idx = 0
        self.is_attacking = True
        self.direction.y = 0
        self.attack_buffer_counter = self.attack_buffer
        self.attack_idx == 2
        self.attack_idx %= len(self.attack_states)

    def get_damage(self, damage = -1):
        if not self.is_invincible:
            self.SFX[SFXType.HIT()].play()
            self.update_health(damage)
            self.is_invincible = True
            self.hurt_time = pg.time.get_ticks()

    def invincibility_timer(self):
        if self.is_invincible: 
            current_time = pg.time.get_ticks()
            if current_time - self.hurt_time >= self.invinciblity_duration:
                self.is_invincible = False
                
    def sin_value(self):
        value = sin(pg.time.get_ticks())
        if value >= 0 : return 255
        else: return 0
    
    def ultimate(self):
        if self.current_energy < self.ultimate_cost[self.type]:
            return
        self.is_ultimate = True
        self.update_energy(-self.ultimate_cost[self.type])
        self.current_energy += -self.ultimate_cost[self.type]
        if self.type == PlayerType.LIGHT():
            self.SFX[SFXType.ULTIMATE01()].play()
            ultimate = Ultimate(self.rect.midbottom, self.type, self, 4, 0.35, (0, 63))
        else:
            self.SFX[SFXType.ULTIMATE02()].play()
            ultimate = Ultimate(self.rect.midbottom, self.type, self, 2, 0.5, (0, 5), 3, 15)
        self.VFX_sprites.add(ultimate)
    
    def update(self, delta_time):
        self.countdownAttackBuffer(delta_time)
        self.gatherInput()
        self.getState()
        self.animate()
        self.invincibility_timer()
        self.sin_value()
        
        if self.type == PlayerType.LIGHT():
            self.current_energy += self.increase_factor
            if self.current_energy >= self.max_energy:
                self.can_transform = True
                self.current_energy = self.max_energy
            self.update_energy(self.increase_factor)
        elif self.type == PlayerType.DARK():
            self.current_energy += self.decrease_factor
            if self.current_energy <= 0:
                self.can_transform = False
                self.current_energy = 0
            self.update_energy(self.decrease_factor)
        if self.is_transforming:
            self.particle.update(self.rect, self)
            self.particle.draw(self.display_surf)
        self.VFX_sprites.update(self.worldShift())
        self.VFX_sprites.draw(self.display_surf)
