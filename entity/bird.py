import pygame
from math import floor

class Bird(pygame.sprite.Sprite):

    def __init__(self, image_set: list, config) ->None:
        pygame.sprite.Sprite.__init__(self)
        self.config = config
        self.images = image_set
        self.image = self.images[2]
        self.speed = config.speed
        self.max_fall_speed = config.speed
        self.ignore = False
        self.wait_time = 0
        self.imtable = {-5:0,-4:1,-3:2,-2:3,-1:4}
        self.power = 0
        self.debuff = 1
        self.current_image = 0
        self.rect = self.image.get_rect()
        self.reposition()
  
    def update(self, level):
        if self.rect[1] + self.image.get_height()/2 >= level:
            self.in_water = -1
        else:
            self.ignore = False
            self.in_water = 1

        if self.ignore:
            self.in_water = 1
            level = self.config.window_h

        if self.speed < self.debuff * self.max_fall_speed:
            self.speed += self.debuff * self.config.gravity
            self.current_image = self.imtable[floor(self.speed/(self.config.pixel*self.debuff))] if self.speed <= 0 else 3 

        if self.rect[1] <= self.config.avail_h + 0.3*self.config.base_h - self.image.get_height():
            if abs(self.rect[1] + 1 + self.image.get_height()/2 - level) <= self.speed:
                self.rect[1] = level - self.image.get_height()/2 + 1
            else: self.rect[1] += self.in_water * self.speed
        self.bird_image()

    def fly(self):
        self.speed = -self.max_fall_speed / self.debuff
        self.config.sound.wing.play()
    
    def power_up(self, power):
        if power != 0:
            self.power = abs(power)
            if power < 0:
                self.debuff = 1.2
            return True
        return False
        
    def invincibility(self):
        return self.power == 1 and self.speed > 0

    def reposition(self):
        self.image = self.images[2]
        self.rect[0] = self.config.window_w / 15
        self.rect[1] = self.config.avail_h /2
        self.reset()
        self.in_water = 1

    def bird_image(self):
        if self.power == 1 and self.speed > 0:
            self.image = self.images[5]
        elif self.power == 2:
            self.image = self.images[-self.current_image-1]
        else:
            self.image = self.images[self.current_image]

    def reset(self):
        if self.power != 0:
            self.power = 0
            self.debuff = 1

    def collided(self, pipe: pygame.sprite.Group, attack: pygame.sprite.Group):
        if self.rect[1] + self.rect[3] <= 0.9*self.image.get_height() or (self.rect[1] 
        + self.image.get_height() >= self.config.avail_h + 0.3*self.config.base_h):
            self.speed = 0
            return True
        if len(pipe) and -pipe.sprites()[0].rect[3] <= pipe.sprites()[0].rect[0] - self.rect[0] <= 1.5 * self.rect[3]:
            if pygame.sprite.spritecollide(self, pipe, False, pygame.sprite.collide_mask):
                    self.speed = 0
                    return True
        if len(attack) and (min(sprite.rect[0] for sprite in attack.sprites()) - 1.5*self.rect[3] <=
        self.rect[0] <= max(sprite.rect[0] for sprite in attack.sprites()) + attack.sprites()[0].image.get_width()):
            collide_attack = pygame.sprite.spritecollide(self, attack, False, pygame.sprite.collide_mask)
            if len(collide_attack) == 1:
                if collide_attack[0].special:
                    self.ignore = True
                    collide_attack[0].kill()
                elif self.invincibility():
                    self.reset()
                    collide_attack[0].kill()
                else:
                    self.speed = 0
                    return True
            elif len(collide_attack) > 1:
                self.speed = 0
                return True
        return False

    def wait(self):
        if self.wait_time == 24:
            self.config.sound.wing.play()
        self.wait_time = (self.wait_time + 1)%25
        self.image = self.images[self.wait_time//5]

    def draw(self, screen):
        screen.blit(self.image, (self.rect[0], self.rect[1]))