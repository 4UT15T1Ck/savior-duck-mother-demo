import pygame
from config import Config

class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, x, y, pipe_set, config: Config) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.config = config
        self.inverted = inverted
        self.go_boss = True

        if inverted:
            self.image = pipe_set[1]
            self.rect = self.image.get_rect()
            self.rect[0] = x
            self.rect[1] = y - config.avail_h/4 - self.rect[3]
        else:
            self.image = pipe_set[0]
            self.rect = self.image.get_rect()
            self.rect[0] = x
            self.rect[1] = y
    
    def y_move(self, dir):
        if self.inverted:
            if self.rect[1] + self.rect[3] >= 2*self.config.speed:
                self.rect[1] += dir * self.config.speed * 0.6
            else:
                self.rect[1] = 2*self.config.speed - self.rect[3] 
                return True
        else:
            if self.config.avail_h - self.rect[1] >= 2*self.config.speed:
                self.rect[1] += dir * self.config.speed * 0.6
            else:
                self.rect[1] = self.config.avail_h - 2*self.config.speed 
                return True
        return False

    def update(self):
        self.rect[0] -= self.config.speed
    
    def boss(self):
        if self.rect[1] > (self.config.avail_h + self.config.boss_h)/2 and self.go_boss:
            self.rect[1] -= self.config.speed
        else:
            self.go_boss = False 
    
    def pipe_run(self, goal, direct):
        if abs(self.rect[1] - goal) > self.config.speed:
            self.rect[1] += direct * self.config.speed
        else:
            self.rect[1] = goal   