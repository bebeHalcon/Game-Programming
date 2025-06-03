import pygame
import random
from pygame import *

clock = pygame.time.Clock()
FPS = 60
class Hammer:
    def __init__(self, screen, background):
        self.hammer_idle = pygame.image.load("images/HammerIdle.png")
        self.hammer_hit = pygame.image.load("images/HammerHit.png")
        self.image = self.hammer_idle
        self.screen = screen
    def update(self):
        self.image = pygame.transform.scale(self.image,(128,128))
        rect = self.image.get_rect(center=(mouse.get_pos()))
        self.screen.blit(self.image, rect)
    def draw_hit(self,hit):
        if hit==True:
            self.image = self.hammer_hit
        else:
            self.image = self.hammer_idle
        
class Assets:
    def __init__(self):
        self.zombie = []
        zombie_ss = pygame.image.load("images/Zombie.png")
        for i in range(0,2048//128):
            self.zombie.append(zombie_ss.subsurface(128*i,0,128,128))    
            self.zombie[-1].set_colorkey((0, 0, 0))
            #self.zombie[-1] = self.zombie[-1].convert_alpha()
class HurtEffect:
    def __init__(self, screen, background, position, duration = 0.25):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.image = pygame.image.load("images/hurt_effect.png")
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert_alpha()
        self.scale_ratio = 1
        self.position = position
        self.alpha = 255
        self.interval = 0
        self.count = 0
        self.previous = 0
        self.duration = duration
    def update(self):
        dt = self.clock.tick(FPS)/1000 #deltatime

        if (self.previous-my_game.hp>0):
            self.count +=1
        
        if self.interval>self.duration:
            pass
        elif (self.interval<=self.duration):
            temp = self.image
            temp.set_alpha(255-255*(self.interval-0)/self.duration)
            temp = pygame.transform.scale_by(temp,1.5*(self.interval)/self.duration)
            self.screen.blit(temp, temp.get_rect(center = self.position))
        self.interval+=dt
        self.previous = my_game.hp
        if (self.count>0 and self.interval>self.duration):
            self.count-=1
            self.interval = 0
        pass
class siren:
    def __init__(self, screen, background):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.background = background

        
        self.myfont = pygame.font.Font('./fonts/FbUsv8C5eI.ttf', 50)


        #self.siren_text = self.myfont.render(self.flag_form, False, (255, 0, 0))

 

        
        self.i = 1
        self.j = 0
        self.interval = 4
        self.scale_ratio = 100
    def reset(self):
        self.i = 1
        self.j = 0
        self.interval = 4
        self.scale_ratio = 100
    def update(self):
        dt = self.clock.tick(FPS)/1000 #deltatime
        self.siren_text = self.myfont.render("WAVE "+ str(my_game.wave), False, (255, 0, 0))
        if (my_game.wstate == True):
            if (self.scale_ratio<=2):
                self.scale_ratio = 2
                if (self.interval<=0):
                    pass
                else:
                    self.interval-=dt
                    self.screen.blit(pygame.transform.scale_by(self.siren_text,self.scale_ratio),pygame.transform.scale_by(self.siren_text,self.scale_ratio).get_rect(center = (my_game.SCREEN_WIDTH/2,my_game.SCREEN_HEIGHT/2)))
            else:
                self.screen.blit(pygame.transform.scale_by(self.siren_text,self.scale_ratio),pygame.transform.scale_by(self.siren_text,self.scale_ratio).get_rect(center = (my_game.SCREEN_WIDTH/2,my_game.SCREEN_HEIGHT/2)))
                self.scale_ratio-=150*dt
        else:
            self.reset()
class AnouncementText:
    def __init__(self, screen, background) -> None:
        self.surface = pygame.surface.Surface([327,228],  pygame.SRCALPHA, 32).convert_alpha()
        self.image = pygame.image.load("images/anouncement.png")
        
        self.clock = pygame.time.Clock()

        self.interval = 5

        self.screen = screen
        self.background = background
        self.scale_ratio = 1
        self.alpha = 255

        self.position = (400,90)
        self.previous = False
        self.image.set_colorkey((0, 0, 0))
        self.image = self.image.convert_alpha()
        self.image = pygame.transform.scale_by(self.image,1/4)
        self.spr = self.image
        self.font_obj = pygame.font.Font('./fonts/GROBOLD.ttf', 23)
        self.font_obj2 = pygame.font.Font('./fonts/FbUsv8C5eI.ttf', 20)
        self.text =  self.font_obj.render("WAVE COMPLETE",True, (0, 0, 0))
        self.text = pygame.transform.scale_by(self.text,1)


    def update(self):
        dt = self.clock.tick(FPS)/1000 #deltatime
        if (my_game.wstate == False and self.previous == True):
            self.interval = 0
        if (my_game.wstate == False):
            if self.interval>3.5:
                return
            
            score_text = self.text.convert_alpha()
            if (self.interval <= 0.5):
                self.image.set_alpha(255*self.interval/0.5)
            if (self.interval<=0.25):
                score_text = pygame.transform.scale_by(score_text,0.5+1*self.interval/0.25)
                
            if (self.interval>0.25 and self.interval<=0.5):
                score_text = pygame.transform.scale_by(score_text,1.5-0.5*(self.interval-0.25)/0.25)
                
            if (self.interval >= 3 and self.interval<=3.25):
                score_text = pygame.transform.scale_by(score_text,1+1*(self.interval-3)/0.25)
                
            if (self.interval >= 3.25 and self.interval <= 3.5):
                score_text = pygame.transform.scale_by(score_text,2-2*(self.interval-3.25)/0.25)
                self.image.set_alpha(255-255*(self.interval-3.25)/0.25)
            self.screen.blit(self.image,self.image.get_rect(center = self.position))
            score_rect  = score_text.get_rect(center = self.position)
            self.screen.blit(score_text, score_rect)
        self.interval+=dt
        



        self.previous = my_game.wstate
            #self.image = self.spr
            
            #self.screen.blit(self.surface,self.surface.get_rect(center = (400,80)))


                        

class TimerLabel:
    def __init__(self, screen, background) -> None:
        self.surface = pygame.surface.Surface([327/3,228/3],  pygame.SRCALPHA, 32).convert_alpha()
        self.image = pygame.image.load("images/ui_timer.png")
        self.clock = pygame.time.Clock()


        self.screen = screen
        self.background = background
        self.scale_ratio = 1
        self.alpha = 255
        self.interval = 0
        self.image.set_colorkey((0, 0, 0))
        self.image = self.image.convert_alpha()
        self.image = pygame.transform.scale(self.image,(327/3,228/3))
        self.spr = self.image
        self.font_obj = pygame.font.Font('./fonts/GROBOLD.ttf', 25)
        self.font_obj2 = pygame.font.Font('./fonts/FbUsv8C5eI.ttf', 20)



    def update(self):
        dt = self.clock.tick(FPS)/1000 #deltatime

        if (my_game.wstate == False):
            if (self.interval<3.5 and my_game.wave>0):
                self.interval+=dt
            else:
                self.screen.blit(self.surface,self.surface.get_rect(center = (400,80)))
                self.image = self.spr
                self.surface.blit(self.image,(0,0))

                score_text2 = self.font_obj2.render("WAVE " + str(int(my_game.wave+1))+ " IN:",True, (0, 0, 0))
                score_text_pos2 = score_text2.get_rect(center = (327/6,228/6-17))

                score_text = self.font_obj.render( str(int(my_game.wstarting)),True, (0, 0, 0))
                score_text_pos = score_text.get_rect(center = (327/6,228/6+13))
                self.surface.blit(score_text2, score_text_pos2)
                self.surface.blit(score_text, score_text_pos)
        else:
            self.interval=0
            

class ProgressBar:
    def __init__(self, screen, background) -> None:
        self.surface = pygame.surface.Surface([350,150],  pygame.SRCALPHA, 32).convert_alpha()
        self.screen = screen
        self.background = background
        self.scaleFactor = 2.5
        self.clock = pygame.time.Clock()
        self.WaveLabel = pygame.image.load("images/UI_Wave_label.png")
        self.WaveLabel.set_colorkey((0, 255, 0))
        self.WaveLabel = self.WaveLabel.convert_alpha()
        self.BarUnder = pygame.image.load("images/UI_progressbar.png")
        self.BarUnder.set_colorkey((0, 255, 0))
        
        self.BarFill = pygame.image.load("images/UI_progressbar_fill.png")
        #self.BarFill.set_colorkey((0, 0, 0))
        self.BarFill = self.BarFill.convert_alpha()
        
        self.WaveLabel = pygame.transform.scale_by(self.WaveLabel,1/self.scaleFactor)
        self.BarUnder = pygame.transform.scale_by(self.BarUnder,1/self.scaleFactor)
        self.BarFill = pygame.transform.scale_by(self.BarFill,1)



        self.interval = 2.0
        self.scale_ratio = 0
        self.alpha = 0
        self.font_obj2 = pygame.font.Font('./fonts/FbUsv8C5eI.ttf', 20)


    def reset(self):
        self.interval = 3.0
        self.scale_ratio = 0
        self.alpha = 0
        pass
    def update(self):
        dt = self.clock.tick(FPS)/1000 #deltatime
        if (my_game.wstate == True):
            if (self.interval<0):
                if (self.scale_ratio<1):
                    self.scale_ratio+=dt*3
                else:
                    self.scale_ratio = 1
                if (self.alpha<1):
                    self.alpha+=dt*2
                else:
                    self.alpha = 1
                self.surface.set_alpha(self.alpha*255)
                self.screen.blit(pygame.transform.scale_by(self.surface,self.scale_ratio),self.surface.get_rect(center = (415,65)))
            
                score_text2 = self.font_obj2.render("WAVE " + str(int(my_game.wave))+ "",True, (0, 0, 0))
                score_text_pos2 = score_text2.get_rect(center = (50,75))

                self.surface.blit(self.BarUnder,self.BarUnder.get_rect(center = (195,75)))
                self.surface.blit(self.WaveLabel,self.WaveLabel.get_rect(center = (50,75)))
                self.surface.blit(pygame.transform.scale(self.BarFill,(210*((my_game.goal-my_game.zleft)/my_game.goal),14)),(92.9,68.8))
                self.surface.blit(score_text2, score_text_pos2)
            else:
                self.interval-=dt
        else:
            self.reset

            


class Zombie:
    def __init__(self, screen, background, hole_position, cycle_time = 3, speed = 1):
        self.width = 105
        self.height = 110
        self.hp = 1
        self.clock = pygame.time.Clock()
        
        self.is_hide = False
        self.is_hit = False
        self.cycle_time = cycle_time
        self.interval_time = 0
        self.alive_time = 3
        self.frameTime = 0

        self.speed = speed

        self.screen = screen
        self.background = background
        self.current_hole_x = hole_position[0]
        self.current_hole_y = hole_position[1]
        self.image = asset.zombie[0]
        self.frameCounter = 0

        self.alpha = 255
        self.state = 0 #0 = init, 1 = idle, 2 = hit, 3 = escape
    
    def __del__(self):
        if self in my_game.zombies:
            my_game.zombies.remove(self)
            for z in my_game.zombies:
                z.update()
        for h in my_game.holes:
            if self.current_hole_x == h.current_pos_x and self.current_hole_y == h.current_pos_y:
                h.zombie = False
                break
    def is_zombie_hit(self, mouse_position):
        mouse_x = mouse_position[0]
        mouse_y = mouse_position[1]
        print(mouse_position)
        if (
            mouse_x > self.current_hole_x+15 - self.width/2
            and mouse_x < self.current_hole_x + 15 + self.width/2
            and mouse_y > self.current_hole_y - 62 - self.height/2
            and mouse_y < self.current_hole_y - 62 + self.height/2
        ):
            self.hp -= 1
            my_game.increase_score(1)
            if (self.hp<=0):
                self.draw(asset.zombie[int(self.frameCounter)])
                my_game.zleft-=1
                self.state = 2
            return True
        else:
            return False

    def draw(self, frame, alpha = 255):
        #ss_num = frame/20 ## cho nay là ss_num tinh theo frame sao do de ve
        if self.is_hide == True:
            pass
        elif self.is_hit == True:
            pass
        else:
            self.image = frame
            #pass
        self.image = pygame.transform.scale(self.image,(128,128))
        self.image.set_alpha(alpha)
        rect = self.image.get_rect(center=(self.current_hole_x+15, self.current_hole_y-62))
        self.screen.blit(self.image, rect)
    def update(self):
        dt = self.clock.tick(FPS)/1000 #deltatime
        #print(dt)
        if (self.state == 0):
            if (self.frameCounter<10):
                self.draw(asset.zombie[int(self.frameCounter)])
                if (self.frameTime > 1/60):
                    self.frameCounter+=1
                    self.frameTime = 0
                else:
                    self.frameTime += dt
            else:
                self.state = 1
                self.interval_time = self.cycle_time
                self.draw(asset.zombie[int(self.frameCounter)])
        elif (self.state==1):
            self.interval_time-=dt
            self.draw(asset.zombie[int(self.frameCounter)])
            if (self.interval_time<=0):
                self.state = 3
                self.draw(asset.zombie[int(self.frameCounter)])
        elif (self.state==3):
            if (self.frameCounter>=0):
                self.draw(asset.zombie[int(self.frameCounter)])
                if (self.frameTime > 1/200):
                    self.frameCounter-=90*dt
                    self.frameTime = 0
                else:
                    self.frameTime += dt
                #self.frameCounter-=60*dt
            else:
                my_game.zspawner.zombies_left+=1
                my_game.zom_escape += 1
                my_game.soundEffect.playSlurp()
                self.__del__()
                del self
        elif (self.state == 2):
            
            if (self.frameCounter<30):
                if (self.frameCounter>=15):
                    self.draw(asset.zombie[int(15)])
                else:
                    self.draw(asset.zombie[int(self.frameCounter)])
                self.frameCounter+=30*dt
            else:
                if (self.alpha >= 0):
                    self.draw(asset.zombie[int(15)],self.alpha)
                    self.alpha-= 1500*dt
                else:
                    self.__del__()
                    del self

                
            
class SmashEffect:
    def __init__(self, screen, background, position):
        self.width = 105
        self.height = 110
        self.scaleFactor = 1
        self.clock = pygame.time.Clock()
        


        self.interval = 0

        self.image = []
        eff_ss = pygame.image.load("images/HitVfx2.png")
        for i in range(0,8):
            self.image.append(eff_ss.subsurface(172.75*(i%4),186*(i//4),172.75,186))    
            self.image[-1].set_colorkey((0, 0, 0))
            self.image[-1].convert_alpha()


        self.screen = screen
        self.background = background
        self.position = position
        self.frameCounter = 0

        self.alpha = 255

    def update(self):
        dt = self.clock.tick(FPS)/1000
        if (self.interval>1/24):
            self.interval = 0
            self.frameCounter+=1
            if self.frameCounter>=len(self.image):
                if (self in my_game.effects):
                    my_game.effects.remove(self)
                del self
                return
        else:
            self.interval+=dt
        newimage = self.image[self.frameCounter]
        newimage = pygame.transform.scale_by(newimage,1/self.scaleFactor)
        rect = newimage.get_rect(center = self.position)
        self.screen.blit(newimage, rect)


class Spawner:
    def __init__(self) -> None:
        self.zombies_left = 5
        self.clock = pygame.time.Clock()
        self.spawn_interval = 5.0
        self.spawn_gap = 3.0
        self.livetime = 2
        self.spawn_clock = self.spawn_gap
        pass
    def update(self):
        dt = self.clock.tick(FPS)/1000
        if (my_game.wstate==True and self.spawn_interval<=0):
            if (self.zombies_left>0):
                if (self.spawn_clock<=0):
                    for i in range(0,100):
                        h = my_game.holes[random.randint(0,len(my_game.holes)-1)]
                        if not h.zombie:
                            #spawning zombie
                            self.zombies_left-=1
                            my_game.zombies.append(Zombie(my_game.screen,my_game.background,(h.current_pos_x,h.current_pos_y),self.livetime))
                            h.zombie = True
                            self.spawn_clock = self.spawn_gap
                            my_game.soundEffect.playPop()
                            break
                else:
                    self.spawn_clock -= dt
        elif (my_game.wstate==True):
            self.spawn_interval -= dt
        else:
            self.spawn_interval = 4


class Hole:
    def __init__(self, screen, background, hole_position) -> None:
        self.screen = screen
        self.background = background
        self.current_pos_x = hole_position[0]
        self.current_pos_y = hole_position[1]
        self.image = pygame.image.load("images/Hole.png")
        self.image.set_colorkey((0, 0, 0))
        self.image = self.image.convert_alpha()
        self.available = True
        self.zombie = False
    def update(self):
        #self.image = pygame.transform.scale(self.image,(210*1,44*1))
        if (self.available):
            rect = self.image.get_rect(center=(self.current_pos_x,self.current_pos_y))
            self.screen.blit(self.image, rect)




class GameManager:
    def __init__(self):
        # Define constants
        self.SCREEN_WIDTH = 797
        self.SCREEN_HEIGHT = 600

        self.MOLE_WIDTH = 90
        self.MOLE_HEIGHT = 81
        self.FONT_SIZE = 31
        self.FONT_TOP_MARGIN = 26
        self.LEVEL_SCORE_GAP = 4
        self.LEFT_MOUSE_BUTTON = 1
        self.GAME_TITLE = "ZombieWhackWhack - Game for Assignment 1"
        self.MAX_HP = 14 # Thuc ra so luong heart = MAX_HP/2
        self.clock = pygame.time.Clock()




        
        print("Hello")
        # Initialize screen
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption(self.GAME_TITLE)
        self.background = pygame.image.load("images/NewBg.png")
        # Font object for displaying text
        self.font_obj = pygame.font.Font('./fonts/GROBOLD.ttf', self.FONT_SIZE)
        # Initialize the mole's sprite sheet
        # 6 different states
        sprite_sheet = pygame.image.load("images/mole.png")
        self.mole = []

        self.holes = []
        self.zombies = []


        self.wave = 0
        self.zleft = 0
        self.goal = 1
        self.wstate = False #True mean during wave
        self.wstarting = 15

        # Positions of the holes in background
        self.hole_positions = []
        self.hole_positions.append((158, 380))
        self.hole_positions.append((464, 528))
        self.hole_positions.append((626, 457))
        self.hole_positions.append((637, 184))
        self.hole_positions.append((429, 399))
        self.hole_positions.append((161, 261))
        self.hole_positions.append((344, 213))
        self.hole_positions.append((154, 143))
        self.hole_positions.append((471, 147))
        self.hole_positions.append((247, 482))
        self.hole_positions.append((384, 314))
        self.hole_positions.append((647, 337))

        # UI Sprite
        self.font_obj1933 = pygame.font.Font('./fonts/FbUsv8C5eI.ttf', 25)

        self.heart = pygame.image.load("images/Heart.png")
        self.gray_heart = pygame.image.load("images/GrayHeart.png")
        self.haft_heart = pygame.image.load("images/HaftHeart.png")
        self.retry = pygame.image.load("images/Retry.png")
        self.retry_btn_size_x = 193
        self.retry_btn_size_y = 74
        self.retry__btn_pos = (300,270)
        self.hearteffect = HurtEffect(self.screen,self.background,(400,50),0.25)

        self.gameover = pygame.image.load("images/GameOverLabel.png")
        self.gameover_scale = 0.5
        self.gameover_pos = (self.SCREEN_WIDTH/2,self.SCREEN_HEIGHT/3)

        self.advertise_text = self.font_obj1933.render("- Tran Dan Huy - Phan Thanh Hai - Nguyen Minh Loc - Tran Thien Nhan -", False, (0, 0, 0))
        self.advertise_text = self.advertise_text.convert_alpha()
        self.advertise_pos = (self.SCREEN_WIDTH/2,self.SCREEN_HEIGHT*8/9)

        self.advertise2_text = self.font_obj1933.render("Hey! Check out my sh*t game Hexalink Demo Version at https://gedusx.itch.io/hexalink !", False, (0, 0, 0))
        self.advertise2_text = self.advertise2_text.convert_alpha()
        self.advertise2_pos = (self.SCREEN_WIDTH/2,self.SCREEN_HEIGHT*8.35/9)

        self.effects = []

        self.anouncement = AnouncementText(self.screen,self.background)
        self.hammer = Hammer(self.screen,self.background)
        self.timer = TimerLabel(self.screen,self.background)
        self.pbar = ProgressBar(self.screen,self.background)
        self.siren = siren(self.screen,self.background)
        # Init debugger
        self.debugger = Debugger("debug")
        # Sound effects
        self.soundEffect = SoundEffect()
        
        self.set_up()

    def set_up(self):
        # Initialize player's score, number of missed hits and level
        self.hp = self.MAX_HP
        self.score = 0
        self.misses = 0
        self.zom_escape = 0
        self.wave = 0
        self.goal=1
        self.wstarting = 15
        self.wstate = False
        self.zombies.clear()
        self.effects.clear()
        self.timer = TimerLabel(self.screen,self.background)
        self.pbar = ProgressBar(self.screen,self.background)
        self.anouncement = AnouncementText(self.screen,self.background)
        self.siren = siren(self.screen,self.background)
        self.soundEffect.playStandby()
        self.zspawner = Spawner()
        self.zombies.clear()
    


    def wave_prepare(self):
        self.wave +=1
        self.goal = self.wave*7+5
        self.zleft = self.goal
        self.zspawner.zombies_left = self.goal
        self.zspawner.spawn_gap = 2-1.85*(1-pow(0.7,self.wave+3))
        self.zspawner.livetime = 3.1-2.4*(1-pow(0.9,self.wave+3))
        self.wstate = True

    # Calculate the player level according to his current score & the LEVEL_SCORE_GAP constant
    def get_player_level(self):
        newLevel = 1 + int(self.score / self.LEVEL_SCORE_GAP)
        if newLevel != self.level:
            # if player get a new level play this sound
            self.soundEffect.playLevelUp()
        return 1 + int(self.score / self.LEVEL_SCORE_GAP)

    # Get the new duration between the time the mole pop up and down the holes
    # It's in inverse ratio to the player's current level
    def get_interval_by_level(self, initial_interval):
        new_interval = initial_interval - self.level * 0.15
        if new_interval > 0:
            return new_interval
        else:
            return 0.05


    
    def is_button_hit(self, mouse_position, button_position, button_size_x, button_size_y):
        mouse_x = mouse_position[0]
        mouse_y = mouse_position[1]
        btn_x = button_position[0]
        btn_y = button_position[1]
        if (mouse_x > btn_x) and (mouse_x < btn_x + button_size_x) and (mouse_y > btn_y) and (mouse_y < btn_y + button_size_y):
            return True
        else:
            return False
    
    def increase_score(self, value):
        self.score += value
    # Update the game states, re-calculate the player's score, misses, level
    def update(self):
        # Update the player's score
        current_score_string = "SCORE: " + str(self.score)
        score_text = self.font_obj.render(current_score_string, True, (255, 255, 0))
        score_text_pos = score_text.get_rect()
        # score_text_pos.centerx = self.background.get_rect().centerx
        # score_text_pos.centery = self.FONT_TOP_MARGIN
        score_text_pos.centerx = 90
        score_text_pos.centery = 28
        self.screen.blit(score_text, score_text_pos)
        
        for e in self.effects:
            e.update()
        self.anouncement.update()
        self.timer.update()
        self.pbar.update()
        self.siren.update()
        self.hammer.update()
        
        # # Update the player's misses
        # current_misses_string = "MISSES: " + str(self.misses)
        # misses_text = self.font_obj.render(current_misses_string, True, (255, 255, 255))
        # misses_text_pos = misses_text.get_rect()
        # misses_text_pos.centerx = self.SCREEN_WIDTH / 5 * 4
        # misses_text_pos.centery = self.FONT_TOP_MARGIN
        # self.screen.blit(misses_text, misses_text_pos)
        # # Update the player's level
        # current_level_string = "LEVEL: " + str(self.level)
        # level_text = self.font_obj.render(current_level_string, True, (255, 255, 255))
        # level_text_pos = level_text.get_rect()
        # level_text_pos.centerx = self.SCREEN_WIDTH / 5 * 1
        # level_text_pos.centery = self.FONT_TOP_MARGIN
        # self.screen.blit(level_text, level_text_pos)
        self.hearteffect.update()
        # Draw HP UI
        self.hp = self.MAX_HP-self.misses-self.zom_escape
        i = 0
        while i<self.MAX_HP:
            if i%2==0:
                if i<self.hp:
                    self.screen.blit(self.heart, (225 + i*25, 4))
                else:
                    self.screen.blit(self.gray_heart, (225 + i*25, 4))
            if i%2==1 and i==self.hp:
                self.screen.blit(self.haft_heart, (225 + (i-1)*25, 4))
            i += 1
        

    # Start the game's main loop
    def start(self):
        cycle_time = 0
        num = -1
        loop = True
        game_over = False
        is_down = False
        interval = 0.1
        initial_interval = 1
        frame_num = 0

        
        #tz = Zombie(self.screen,self.background,self.hole_positions[0])
        for pos in self.hole_positions:
            self.holes.append(Hole(self.screen,self.background,pos))
        
        
        left = 0
        # Time control variables
        

        for i in range(len(self.mole)):
            self.mole[i].set_colorkey((0, 0, 0))
            self.mole[i] = self.mole[i].convert_alpha()

        while loop:
            mil = self.clock.tick(FPS)
            sec = mil / 1000.0
            cycle_time += sec
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                if event.type == MOUSEBUTTONDOWN and event.button == self.LEFT_MOUSE_BUTTON:
                    self.hammer.draw_hit(True)
                    if self.is_button_hit(mouse.get_pos(),self.retry__btn_pos,self.retry_btn_size_x, self.retry_btn_size_y) and game_over == True:
                        self.set_up()
                        game_over = False
                        
                    elif game_over==False:
                        flag = False
                        self.soundEffect.playFire()
                        for z in (zz for zz in self.zombies if zz.state<=1):
                            if (z.state <= 1 and z.is_zombie_hit(mouse.get_pos())):
                                self.soundEffect.playHurt()
                                self.effects.append(SmashEffect(self.screen,self.background,mouse.get_pos()))
                                #self.update()
                                flag = True
                                break
                        if flag == False:
                            self.misses += 1
                            #self.update()
                if event.type == MOUSEBUTTONUP and event.button == self.LEFT_MOUSE_BUTTON:
                    self.hammer.draw_hit(False)

            if self.hp<=0:
                self.screen.blit(self.background, (0, 0))
                if (game_over==False):
                    self.soundEffect.loseMusic()
                game_over = True
                
                self.screen.blit(self.retry, self.retry__btn_pos)
                self.screen.blit(pygame.transform.scale_by(self.gameover,self.gameover_scale),pygame.transform.scale_by(self.gameover,self.gameover_scale).get_rect(center = self.gameover_pos))
                self.screen.blit(self.advertise_text,self.advertise_text.get_rect(center = self.advertise_pos))
                self.screen.blit(self.advertise2_text,self.advertise2_text.get_rect(center = self.advertise2_pos))

            else:
                #print(self.zombies)
                self.screen.blit(self.background, (0, 0))
                #self.update()

                
                
                for h in self.holes:
                    h.update()
                if (game_over == False):
                    if (self.wstate == False):
                        if (self.wstarting<=0):
                            self.wstate == True
                        
                            self.soundEffect.playstartWave()
                            self.wave_prepare()
                            if (self.wave<3):
                                self.soundEffect.playLow()
                            elif (self.wave<5):
                                self.soundEffect.playMedium()
                            else:
                                self.soundEffect.playHigh()
                        else:
                            self.wstarting -= sec
                    else:
                        if (len(self.zombies)==0 and self.zleft == 0):
                            self.wstate = False
                            self.wstarting = 13
                            self.pbar.reset()
                            self.siren.reset()
                            self.soundEffect.playComplete()
                            self.soundEffect.playStandby()
                        
                        else:
                            self.zspawner.update()
                            for tz in self.zombies:
                                tz.update()
                
            #print(game_over)
            self.update()
            # Update the display
            pygame.display.flip()


# The Debugger class - use this class for printing out debugging information
class Debugger:
    def __init__(self, mode):
        self.mode = mode

    def log(self, message):
        if self.mode is "debug":
            print("> DEBUG: " + str(message))


class SoundEffect:
    def __init__(self):



        self.clock = pygame.time.Clock()
        self.interval = -1
        self.fireSound = pygame.mixer.Sound("sounds/SFX_bonk.ogg")
        self.fireSound.set_volume(1.0)
        self.popSound = pygame.mixer.Sound("sounds/SFX_floop.ogg")
        self.hurtSound = pygame.mixer.Sound("sounds/Voices_yuck2.ogg")
        self.hurtSound2 = pygame.mixer.Sound("sounds/Voices_yuck.ogg")
        self.levelSound = pygame.mixer.Sound("sounds/point.wav")
        self.sirenSound = pygame.mixer.Sound("sounds/SFX_siren.ogg")
        self.slurpSound = pygame.mixer.Sound("sounds/slurp.ogg")

        self.hugeWaveSound = pygame.mixer.Sound("sounds/hugewave.ogg")
        self.musicController = pygame.mixer.music

    def playFire(self):
        self.fireSound.play()
    def playComplete(self):
        pygame.mixer.Sound("sounds/potato.ogg").play()
        pygame.mixer.Sound("sounds/ach.ogg").play()
        #pygame.mixer.Sound("sounds/potato.ogg").play()


    def stopFire(self):
        self.fireSound.sop()

    def playPop(self):
        self.popSound.play()

    def stopPop(self):
        self.popSound.stop()

    def playHurt(self):
        if (random.randint(1,2)==1):
            self.hurtSound.play()
        else:
            self.hurtSound2.play()

    def stopHurt(self):
        self.hurtSound.stop()

    def playLevelUp(self):
        self.levelSound.play()

    def stopLevelUp(self):
        self.levelSound.stop()

    def playstartWave(self):
        self.sirenSound.play()
        self.hugeWaveSound.play()
    def playSlurp(self):
        self.slurpSound.play()
    def stopstartWave(self):
        self.sirenSound.stop()
        self.hugeWaveSound.stop()
    def playStandby(self):
        interval = self.musicController.get_pos()
        self.musicController.stop()
        self.musicController.unload()
        self.musicController.load("sounds/standby.mp3")
        self.musicController.play(-1)
    def loseMusic(self):
        self.musicController.stop()
        self.musicController.unload()
        self.musicController.load("sounds/losemusic.mp3")
        self.musicController.play(1)
    def playLow(self):

        interval = self.musicController.get_pos()
        self.musicController.stop()
        self.musicController.unload()
        self.musicController.load("sounds/loon1.mp3")
        self.musicController.play(-1)
            
    def playMedium(self):

        interval = self.musicController.get_pos()
        print(interval)
        self.musicController.stop()
        self.musicController.unload()
        self.musicController.load("sounds/loon2.mp3")
        self.musicController.play(-1)
        #pygame.mixer.music.set_pos(interval)
            
    def playHigh(self):

        interval = pygame.mixer.music.get_pos()
        self.musicController.stop()
        self.musicController.unload()
        self.musicController.load("sounds/loon3.mp3")
        self.musicController.play(-1)
            



###############################################################
# Initialize the game
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.init()
pygame.mouse.set_visible(False)

# Run the main loop
asset = Assets()
my_game = GameManager()
my_game.start()
# Exit the game if the main loop ends
pygame.quit()
