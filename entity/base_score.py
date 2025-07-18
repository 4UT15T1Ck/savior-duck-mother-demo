import pygame
from math import floor

class Base(pygame.sprite.Sprite):
    
    def __init__(self, xpos, base_im, config) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = base_im
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.config = config
        self.rect[1] = config.avail_h 

    def update(self):
        self.rect[0] -= self.config.speed
        if self.rect[0] < - self.rect[2]:
            self.rect[0] = self.config.window_w - 5
class Score(pygame.sprite.Sprite):

    def __init__(self, origin_xpos, num_set, config) -> None:
        self.num = num_set
        self.xpos = origin_xpos
        self.config = config
        self.y_pos = config.avail_h/10
        self.score = 0
    
    def set(self, val):
        self.score = val

    def add(self):
        self.score += 1

    def sub(self):
        self.score -= 1

    def draw(self, xpos, ypos, screen):
        if not self.score:
            screen.blit(self.num[0],(xpos - self.config.num_w, ypos))
        else:
            offset_posi = xpos
            tmp_score = self.score
            while tmp_score > 0:
                offset_posi -= self.num[tmp_score%10].get_width()
                screen.blit(self.num[tmp_score%10], (offset_posi, ypos))
                tmp_score //= 10

                
    def draw2(self, screen):
        if not self.score:
            screen.blit(self.num[0],((self.config.window_w - self.config.num_w)/2, self.y_pos))
        iterate = 0
        numset = []
        offset = []
        tmp_score = self.score
        while tmp_score > 0:
            tail = tmp_score % 10
            numset.insert(0, tail)
            tmp_score //= 10
        if len(numset) % 2:
            offset.append(-0.5)
            iterate = floor(len(numset)/2) 
        else:
            iterate = len(numset)//2 - 2
            offset.append(-1)
            offset.append(0)
        for i in range(iterate):
            offset.insert(0, offset[0] - 1)
            offset.append(offset[-1] + 1)
        for j in range(len(numset)):
            screen.blit(self.num[numset[j]],
            (self.config.window_w/2 + offset[j] * self.num[numset[j]].get_width(), self.y_pos))