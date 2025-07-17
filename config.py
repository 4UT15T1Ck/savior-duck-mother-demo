import pygame
from math import floor
import pickle
from sound import Sounds
pygame.display.init()

class Config:
    def __init__(self) -> None:
        self.info = pygame.display.Info()
        self.sound = Sounds()
        self.fps = 60
        self.width = self.info.current_w
        self.height = self.info.current_h
        self.window_w, self.window_h = self.window_size()
        self.pixel = self.window_w/450
        self.num_w, self.num_h = 24*self.pixel, 30*self.pixel
        self.mess_w, self.mess_h = 5 * 67 * self.pixel, 5 * 13 * self.pixel
        self.wiki_w, self.wiki_h = 103*3 * self.pixel, 33*3 * self.pixel
        self.bird_w, self.bird_h = 81*self.pixel, 54*self.pixel
        self.pipe_w, self.pipe_h = 90*self.pixel, 0.7 * self.window_h
        self.base_w, self.base_h = self.window_w, 84 * self.pixel
        self.boss_w, self.boss_h = 148*self.pixel, 120*self.pixel
        self.ghost_w, self.ghost_h = 42*self.pixel, 33*self.pixel
        self.mush_w, self.mush_h = 50*self.pixel, 20*self.pixel
        self.power_w, self.power_h = 29*self.pixel, 32*self.pixel
        self.patt_w, self.patt_h = 22*self.pixel, 16*self.pixel
        self.button_w, self.button_h = 174*self.pixel, 75*self.pixel
        self.gover_w, self.gover_h = 296*self.pixel, 232*self.pixel
        self.statboard_w, self.statboard_h = 5 * 74 * self.pixel, 5 * 72 * self.pixel
        self.count_w, self.count_h = 4*13*self.pixel, 4*19*self.pixel
        self.speed = floor(5 * self.pixel)
        self.gravity = 0.2 * self.pixel
        self.ghost_vertic = self.window_w/180
        self.pipe_speed   = self.window_w/20
        self.avail_h = 14/9*self.window_w
        self.fill_1, self.fill_2 = self.window_h - self.avail_h - self.base_h, 0
        self.load()
 
    def window_size(self):
        if self.width < self.height:
            return self.width , self.height 
        else:
            return 450, 800
    
    def load(self):
        with open('data/data.pkl', 'rb') as file:
            db = pickle.load(file)
            self.hi_score = db['hi_score']
            self.endless_play = db['endless_play']
            self.story_play = db['story_play']
            self.min_boss_hp = db['min_hp']
            self.victory_count = db['vic_count']

    def save(self):
        db = {'hi_score': self.hi_score, 
              'endless_play': self.endless_play, 
              'min_hp': self.min_boss_hp,
              'story_play': self.story_play, 
              'vic_count': self.victory_count}
        with open('data/data.pkl', 'wb') as file:
            pickle.dump(db, file)       

    def mute(self):
        self.sound.mute()

    def show_window(self):
        pygame.display.set_caption('SAVIOR DUCK MOTHER!!!')
        return pygame.display.set_mode((self.window_w, self.window_h))

        