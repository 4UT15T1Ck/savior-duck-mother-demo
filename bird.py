import pygame
from config import Config

class Bird(pygame.sprite.Sprite):

    def __init__(self, image_set: list, config: Config) ->None:
        pygame.sprite.Sprite.__init__(self)
        self.config = config
        self.images = image_set
        self.image = self.images[2]
        self.speed = config.speed
        self.max_fall_speed = config.speed
        self.power = 0
        self.debuff = 1
        self.current_image = 0
        self.image = self.images[2]
        self.rect = self.image.get_rect()
        self.reposition()
  
    def update(self, level):
        if self.rect[1] + self.rect[3] >= level:
            self.in_water = -1
        else:
            self.in_water = 1

        if self.speed < self.debuff * self.max_fall_speed:
            self.speed += self.debuff * self.config.gravity
            self.current_image = 0 if self.speed < -3 else 1 if self.speed < 0 else 2

        if self.rect[1] < self.config.avail_h - self.image.get_height() + 1:
            if abs(self.rect[1] + self.rect[3] - level) < self.speed:
                self.rect[1] = level - self.rect[3]
                self.angle = -30
            else: self.rect[1] += self.in_water * self.speed

        if self.angle > -60 and self.speed >= 0:
            self.angle -= 0.8 * abs(self.speed)
        if self.angle < 60 and self.speed < 0:
            self.angle += abs(self.speed)
        
    def fly(self):
        self.speed = -self.max_fall_speed / self.debuff
    
    def power_up(self, power):
        self.power = abs(power) if power != 0 else self.power
        if power < 0:
            self.debuff = 1.2
        if abs(power) == 1:
            return True
        elif abs(power) == 2:
            self.rect.scale_by_ip(0.7)
            return True
        return False
        
    def invincibility(self):
        if self.power == 1 and self.speed > 0:
            return True
        return False
    
    def settle(self, mov_x, mov_y):
        self.image = self.images[2]
        if self.config.avail_h - self.rect[3] - self.rect[1] <= mov_y:
            self.rect[1] = self.config.avail_h - self.rect[3]
            return True
        else:
            self.rect[1] += mov_y
            self.rect[0] += mov_x
            return False

    def reposition(self):
        self.image = self.images[2]
        self.rect[0] = self.config.window_w / 15
        self.rect[1] = self.config.avail_h /2
        self.angle = 0
        self.reset()
        self.in_water = 1

    def bird_image(self):
        if abs(self.power) == 1 and self.current_image == 2:
            self.image = self.images[3]
        elif abs(self.power) == 2:
            self.image = self.images[-self.current_image-1]
        else:
            self.image = self.images[self.current_image]

    def reset(self):
        if self.power != 0:
            self.rect = self.rect.scale_by(self.power)
            self.power = 0
            self.debuff = 1

    def draw(self, screen):
        self.bird_image()
        self.image = pygame.transform.rotozoom(self.image, int(self.in_water * self.angle), 1)
        screen.blit(self.image, (self.rect[0], self.rect[1]))