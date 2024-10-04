import pygame
from math import ceil
pygame.display.init()

class Config:
    def __init__(self) -> None:
        self.info = pygame.display.Info()
        self.fps = 60
        self.width = self.info.current_w
        self.height = self.info.current_h
        self.window_w, self.window_h = self.window_size()
        self.pixel = ceil(self.window_w/450)
        self.num_w, self.num_h = 22.5*self.pixel, 36*self.pixel
        self.bird_w, self.bird_h = 54*self.pixel, 36*self.pixel
        self.pipe_w, self.pipe_h = 81*self.pixel, ceil(0.7 * self.window_h)
        self.base_w, self.base_h = self.window_w, (self.window_h - 4/3 * self.window_w)/2
        self.boss_w, self.boss_h = 81*self.pixel, 96*self.pixel
        self.ghost_w, self.ghost_h = 57*self.pixel, 50*self.pixel
        self.mush_w, self.mush_h = 36*self.pixel, 29*self.pixel
        self.patt_w, self.patt_h = 29*self.pixel, 22*self.pixel
        self.speed = int(5 * self.pixel)
        self.gravity = 0.2 * self.pixel
        self.ghost_vertic = self.window_w/180
        self.pipe_speed   = self.window_w/20
        self.avail_h = self.window_h - self.base_h
 
    def window_size(self):
        if self.width < self.height:
            return self.width - 100, self.height - 100
        else:
            return self.height * 9/16 - 100, self.height - 100
    def show_window(self):
        pygame.display.set_caption('SAVIOR DUCK MOTHER!!!')
        return pygame.display.set_mode((self.window_w, self.window_h))

        