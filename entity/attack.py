import pygame

class Boss_attack(pygame.sprite.Sprite):
    def __init__(self, x, y, y_offset, pat, att_set, config, special) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.images = att_set[pat]
        self.image = self.images[0]
        self.config = config
        self.special = special
        self.movement = 1 if pat == 1 else 2 if pat == 2 else 3
        self.speed = (pat % 2 * 3.5 + 1) * config.speed
        self.rect = self.image.get_rect()
        self.rect[1] = y
        self.rect[0] = x
        self.pat = pat
        self.offset = y_offset
        self.direct = 1
        self.imchange = 0
        if pat == 2:
            self.up, self.down = y + config.avail_h/7, y - config.avail_h/7
        else:
            self.up, self.down = y + config.window_h, y - config.window_h

    def update(self):
        self.imchange = (self.imchange + 1)%(self.movement * 8)
        if self.special:
            self.image = self.images[-self.imchange//8] 
        else:
            self.image = self.images[self.imchange//8] 
        if self.rect[0] > self.config.window_w - self.config.pipe_w:
            self.rect[0] -= self.config.pixel
        else:
            self.rect[0] -= self.speed
            self.vertic_move()
        if abs(self.rect[0] - self.config.window_w/12) < self.speed: 
            if self.pat == 0:
                self.config.sound.chirp.play()
            else:
                self.config.sound.swoosh.play()
        if self.rect[0] < - self.rect[2]:
            self.kill()
    
    def vertic_move(self): 
        if self.rect[1] > self.up or self.rect[1] < self.down:
            self.direct *= -1
        self.rect[1] -= self.direct * self.offset

class Player_attack(pygame.sprite.Sprite):
    def __init__(self, x, y, patt_set, config) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.images = patt_set
        self.image = self.images[0]
        self.config = config
        self.rect = self.image.get_rect()
        self.rect[1] = y + config.boss_h/2
        self.rect[0] = x
        self.speed = config.speed
        self.limit = config.window_w / 15

    def update(self, bird):
        if self.rect[0] < self.limit:
            self.rect[0] += self.config.speed
        self.collide(bird)
    
    def collide(self, bird):
        if abs(bird.rect[1] - self.rect[1]) <= 2*self.config.speed and (
             abs(bird.rect[0] - self.rect[0]) <= 2*self.config.speed):
            self.config.sound.quack.play()
            self.image = self.images[1]
            self.speed *= 5
            self.limit = self.config.window_w
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect[0], self.rect[1]))
