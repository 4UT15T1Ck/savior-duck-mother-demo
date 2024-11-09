import pygame
from config import Config

class Boss(pygame.sprite.Sprite):
    
    def __init__(self, boss_set, config: Config) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.images = boss_set
        self.config = config
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.image = self.images[0]
        self.rect[0] = self.config.window_w - self.image.get_width()
        self.rect[1] = self.config.window_h  
        self.health = 20
        self.intro = True
        self.attack_choice = 0
        self.state = 0      

    def boss_fight(self):
        if self.intro:
            if abs(self.rect[1] - (self.config.avail_h - self.config.boss_h)/2) > self.config.speed:
                self.rect[1] -= self.config.speed
            else:
                self.rect[1] = (self.config.avail_h - self.image.get_height())/2 - 2 * self.config.pixel
                self.intro = False

    def boss_hurt(self, goal, direct):
        if self.state < 1:
            self.state += 0.05
            self.image = self.images[1]
        return self.boss_run(goal, direct)

    def boss_run(self, goal, direct):
        if self.health > 0:
            if abs(self.rect[1] - goal) > self.config.speed:
                self.rect[1] += direct * self.config.speed
            else:
                self.rect[1] = goal
                self.image = self.images[0]
                self.state = 0
        else:
            if self.rect[1] < goal:
                self.rect[1] += self.config.speed
        return self.rect[1] != goal
    
    def hit(self):
        self.health -= 1

    def die(self):
        if self.rect[1] < self.config.window_h:
            self.rect[1] += self.config.speed
            return False
        return True

    def boss_die(self):
        return self.health <= 0

    def phase_2(self):
        return self.health <= 10
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect[0], self.rect[1]))