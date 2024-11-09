import pygame

class Power_up(pygame.sprite.Sprite):
    def __init__(self, power, power_set, config) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.power = power
        self.group = pygame.sprite.Group()
        self.group.add(self)
        self.config = config
        self.image = power_set[abs(power)]
        self.rect  = self.image.get_rect()
        self.rect[0] = config.window_w / 12
        self.rect[1] = config.avail_h + 0.2*config.base_h
        self.wait = 0

    def update(self, wait):
        if 3 <= wait < 7:
            if self.rect[1] + self.rect[3] > self.config.avail_h + 0.2*self.config.base_h:
                self.rect[1] -= self.config.pixel
        elif wait == 7:
            self.rect[1] = self.config.avail_h + 0.2*self.config.base_h
    
    def use(self, bird):
        if pygame.sprite.spritecollide(bird, self.group, True, pygame.sprite.collide_mask):
            return self.power
        return 0
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect[0], self.rect[1]))

class Water(pygame.sprite.Sprite):
    def __init__(self, flood_im, config) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = flood_im
        self.config = config
        self.level = config.window_h
        self.desired_level = config.window_h
        self.direction = -1 
    
    def reset(self):
        self.level = self.config.window_h
    def update(self):
        if self.level > self.desired_level:
            self.direction = -1
        elif self.level < self.desired_level:
            self.direction = 1
        if abs(self.level - self.desired_level) > self.config.speed:
            self.level += self.direction * self.config.speed
        else:
            self.level = self.desired_level
        return self.level

    def fluctuate(self, level):
        self.desired_level = level   

    def changing(self):
        return self.level != self.desired_level 

    def draw(self, screen):
        screen.blit(self.image, (0, self.level))