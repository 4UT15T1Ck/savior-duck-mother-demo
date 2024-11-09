import pygame

class Pipe(pygame.sprite.Sprite):
    direct = 0
    def __init__(self, inverted, x, y, pipe_set, config) -> None:
        pygame.sprite.Sprite.__init__(self)
        Pipe.direct = 0
        self.config = config
        self.inverted = inverted
        self.repo = True
        self.image = pipe_set[1 if inverted else 0]
        self.rect = self.image.get_rect()
        self.rect[0] = x
        if inverted:
            self.rect[1] = y - config.avail_h*0.3 - self.rect[3]
        else:
            self.rect[1] = y

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
    
    def y_move(self):
        if self.inverted:
            if self.rect[1] + self.rect[3] >= 2*self.config.speed:
                self.rect[1] += int(Pipe.direct * self.config.speed * 0.4)
            else:
                self.rect[1] = 2*self.config.speed - self.rect[3]
                Pipe.direct *= -1
        else:
            if self.config.avail_h - self.rect[1] >= 2*self.config.speed:
                self.rect[1] += int(Pipe.direct * self.config.speed * 0.4)
            else:
                self.rect[1] = self.config.avail_h - 2*self.config.speed
                Pipe.direct *= -1

    def reposi(self, y, dir):
        self.rect[0] = self.config.window_w 
        Pipe.direct = dir
        if self.inverted:
            self.rect[1] = y - self.config.avail_h*0.3 - self.rect[3] 
        else:
            self.rect[1] = y
        self.repo = True

    def update(self):
        self.rect[0] -= self.config.speed
        self.y_move()
    
    def out_the_window(self):
        return self.rect[0] < - self.rect[2]
    
    def boss(self):
        if not self.repo:
            return False
        if self.rect[0] - self.config.window_w + self.config.pipe_w > self.config.speed:
            self.rect[0] -= self.config.speed
            return False
        else:
            self.rect[0] = self.config.window_w - self.config.pipe_w - self.config.pixel
            self.repo = False
            return True
  
    def pipe_run(self):
        if self.rect[0] < self.config.window_w - self.config.pipe_w:
            self.rect[0] -= 0.8*self.config.speed
            self.rect[1] += 1.2*self.config.speed

  