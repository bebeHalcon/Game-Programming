import pygame as pg
from setting import *

global_volume = 1
class SFX:
    def __init__(self, path, volume = 1):
        self.sound = pg.mixer.Sound(path)
        self.is_mute = False
        self.volume = volume
        self.sound.set_volume(volume)
        self.init_volume = volume
    
    def set_volume(self, volume):
        self.volume = volume
    
    def mute(self):
        self.sound.set_volume(0)
    
    def unmute(self):
        self.sound.set_volume(self.init_volume)
    
    def playloop(self):
        if self.is_mute:
            self.sound.stop()
            self.sound.set_volume(0)
            return
        self.sound.set_volume(self.volume)
        self.sound.play(-1)
    
    def play(self):
        if self.is_mute:
            return
        self.sound.set_volume(self.volume)
        self.sound.play()
    
    def stop(self):
        self.sound.stop()