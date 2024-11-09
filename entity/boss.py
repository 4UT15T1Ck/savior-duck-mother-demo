import pygame

class Boss(pygame.sprite.Sprite):
    
    def __init__(self, boss_set, config) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.images = boss_set
        self.config = config
        self.special = False
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.image = self.images[0]
        self.rect[0] = 1.5*self.config.window_w
        self.rect[1] = - self.image.get_height()  
        self.health = 20
        self.intro = True
        self.landed = False
        self.state = 0      
 
    def boss_fight(self):
        if self.intro:
            self.fly()
            if abs(self.rect[0] - self.config.window_w + 0.9 * self.image.get_width()) > 0.8 * self.config.speed:
                self.rect[0] -= 0.8 * self.config.speed
            else:
                self.rect[0] = self.config.window_w - 0.9 * self.image.get_width()

            if abs(self.rect[1] - (self.config.avail_h - self.config.boss_h)/2) > 0.8 * self.config.speed:
                self.rect[1] += 0.8 * self.config.speed
            else:
                self.rect[1] = (self.config.avail_h - self.image.get_height())/2
                self.intro = False
                self.land()

    def fly(self):
        self.landed = False
        self.state = (self.state + 1)%24
        self.image = self.images[self.state // 8 + 1]

    def land(self):
        self.landed = True
        self.image = self.images[0]

    def boss_run(self, goal, direct):
        if self.health > 0:
            if abs(self.rect[1] - goal) > 0.8 * self.config.speed:
                self.rect[1] += direct * 0.8 * self.config.speed
            else:
                self.rect[1] = goal
        else:
            if self.rect[1] < goal:
                self.rect[1] += 0.8 * self.config.speed

    
    def hit(self, player_attack):
        if player_attack.rect.colliderect(self.rect.scale_by(0.4,1)):
            self.health -= 1
            return True
        return False

    def die(self, px, py):
        if self.rect[0] + self.image.get_width() > 0:
            frame = abs(self.rect[0] - px)/self.config.speed if self.rect[0] != px else 0.1
            y_ratio = (py - self.rect[1])/(frame*self.config.speed) 
            self.rect[1] += y_ratio*self.config.speed if y_ratio < 0.9 else 0.9*self.config.speed
            self.rect[0] -= self.config.speed
        return self.rect[0] + self.image.get_width() <= 0

    def boss_die(self):
        return self.health <= 0

    def phase_2(self):
        return self.health <= 10
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect[0], self.rect[1]))