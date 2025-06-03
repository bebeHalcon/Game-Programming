import pygame as pg 
import sys     
from setting import *
#from rain import *
from level import Level
from level_data import *
from light import *
from overworld import *
from ui import *
from audio import *

class Game:
    def __init__(self):
        self.max_level = 2
        self.max_health = 100
        self.current_health = self.max_health
        self.max_energy = 100
        self.current_energy = 0
        self.coins = 0
        self.max_boss_health = 1000
        self.current_boss_health = 1000
        
        self.ui = UI(screen)
        
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = GameState.OVERWORLD()
        
        self.loadSound()
        
        self.SFX[SFXType.OVERWORLD_THEME()].playloop()
        self.SFX[SFXType.LEVEL_THEME()].stop()
        #self.SFX[SFXType.RAIN()].stop()
        
        self.current_level = 0
    
    def loadSound(self):
        self.SFX = {
            SFXType.OVERWORLD_THEME() : SFX('../_audio/overworld_theme.wav', 0.5),
            SFXType.LEVEL_THEME() : SFX('../_audio/normal_level_theme.wav', 0.35),
            #SFXType.RAIN() : SFX('../_audio/rain.wav', 0.25),
            SFXType.BOSS_THEME() : SFX('../_audio/boss_theme.wav', 0.5)
        }
    
    def create_overworld(self, current_level, new_max_level):
        if new_max_level >= self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)

        self.max_health = 100
        self.current_health = self.max_health
        self.max_energy = 100
        self.current_energy = 0
        self.coins = 0
        
        self.status = GameState.OVERWORLD()
        self.SFX[SFXType.OVERWORLD_THEME()].playloop()
        self.SFX[SFXType.LEVEL_THEME()].stop()
        #self.SFX[SFXType.RAIN()].stop()
        self.SFX[SFXType.BOSS_THEME()].stop()
    
    def create_level(self, current_level):
        self.current_level = current_level
        self.level = Level(current_level, screen, self.create_overworld, self.update_coins, self.update_health, self.update_energy, self.update_boss_health)
        self.status = GameState.LEVEL()
        self.SFX[SFXType.OVERWORLD_THEME()].stop()
        if current_level == 2:
            self.SFX[SFXType.BOSS_THEME()].playloop()
        else:
            self.SFX[SFXType.LEVEL_THEME()].playloop()
            #self.SFX[SFXType.RAIN()].playloop()
    
    def update_coins(self, amount):
        self.coins += amount
    
    def update_boss_health(self, amount):
        self.current_boss_health += amount
        if self.current_boss_health >= self.max_boss_health:
            self.current_boss_health = self.max_boss_health
        if self.current_boss_health <= 0:
            self.current_boss_health = 0
    
    def update_health(self, amount):
        self.current_health += amount
        if self.current_health >= self.max_health:
            self.current_health = self.max_health
        if self.current_health <= 0:
            self.current_health = 0
    
    def update_energy(self, amount):
        self.current_energy += amount
        if self.current_energy >= self.max_energy:
            self.current_energy = self.max_energy
        if self.current_energy <= 0:
            self.current_energy = 0
    
    def check_game_over(self):
        if self.current_health <= 0:
            self.level.killallsoudns()
            self.current_health = 100
            self.current_energy = 0
            self.coins = 0
            self.overworld = Overworld(0, self.max_level, screen, self.create_level)
            self.status = GameState.OVERWORLD()
    
    def run(self):
        if self.status == GameState.OVERWORLD():
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.current_health, self.max_health)
            self.ui.show_energy(self.current_energy, self.max_energy)
            if self.current_level == 2:
                self.ui.show_boss_health(self.current_boss_health, self.max_boss_health)
            self.ui.show_coin(self.coins)
            self.check_game_over()

class Menu:
    def __init__(self):
        self.is_start = False
        self.is_quit = False
        
        self.background = pg.image.load(HOME_SCREEN_PATH).convert_alpha()
        self.background = pg.transform.scale(self.background, (screen_width, screen_height))
        self.rect = self.background.get_rect(topleft = (0, 0))
        
        self.unmute_button = pg.image.load(UNMUTE_PATH).convert_alpha()
        self.mute_button = pg.image.load(MUTE_PATH).convert_alpha()
        
        self.sound_timer_click = 1000
        self.sound_clicked = False
        self.sound_start_timer = 0
        
        self.sound_button = self.unmute_button
        self.sound_button = pg.transform.scale(self.sound_button, (50, 50))
        self.sound_rect = self.sound_button.get_rect(topright = (screen_width - 5, 5))
        self.is_mute = False
        
        self.start_button = pg.image.load('../_assets/boss/field_of_attack/rect.png')
        self.quit_button = pg.image.load('../_assets/boss/field_of_attack/rect.png')
        self.start_button = pg.transform.scale(self.start_button, (150, 60))
        self.quit_button = pg.transform.scale(self.quit_button, (150, 60))
        
        self.start_rect = self.start_button.get_rect(topleft = (850, 530))
        self.quit_rect = self.quit_button.get_rect(topleft = (850, 610))
    
    def gatherInput(self, mouse_pos):
        global global_volume
        if self.start_rect.collidepoint(mouse_pos):
            self.is_start = True
        if self.quit_rect.collidepoint(mouse_pos):
            self.is_quit = True
        if self.sound_rect.collidepoint(mouse_pos):
            if not self.sound_clicked:
                self.sound_start_timer = pg.time.get_ticks()
                self.is_mute = not self.is_mute
                if self.is_mute:
                    pg.mixer.pause()
                else:
                    pg.mixer.unpause()
                self.sound_button = self.mute_button if self.is_mute else self.unmute_button
                self.sound_button = pg.transform.scale(self.sound_button, (50, 50))
    
    def timerSoundButton(self):
        if self.sound_clicked:
            cur_time = pg.time.get_ticks()
            if cur_time - self.sound_start_timer >= self.sound_timer_click:
                self.sound_clicked = False
    
    def run(self):
        self.timerSoundButton()
        screen.blit(self.background, self.rect)
        screen.blit(self.sound_button, self.sound_rect)

pg.init()
screen = pg.display.set_mode((screen_width, screen_height))
clock = pg.time.Clock()
home = Menu()
game = Game()

if __name__ == '__main__':
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit() 
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                home.gatherInput(event.pos)
                
        screen.fill('black')
        if home.is_quit:
            pg.quit()
        if home.is_start:
            game.run()
        else:
            home.run()
        
        pg.display.update()
        clock.tick(60)