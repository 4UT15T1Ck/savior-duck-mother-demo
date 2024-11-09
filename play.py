import pygame, sys
from pygame.locals import *
from random import randint, choice
from math import floor
from config import Config
from image import Image
from entity import (Boss_attack, 
    Player_attack,
    Base,
    Score,
    Bird,
    Boss,
    Pipe,
    Power_up,
    Water,
    Button)

def random_power_up(): 
    return choice([1,1,1,-1,1,2,2,2,2,-2])

def random_attack(hp, level, attack_set, config: Config):
    a, b = (1, 6) if hp > 15 else (4, 9) if hp > 10 else (1, 9)
    pat = randint(a,b)
    val = []
    if (pat - 1) // 3 == 1:
        for i in range(1,4):
            c,d = (2,4) if i == 3 else (-4,-1) if i == 1 else (-4,4)
            x_offset = pat // 5 * i * choice([0.02, 0.03])
            x = config.window_w * (1 + i % 2 * x_offset)
            y = (3*(i - 1) + choice([-0.5, -0.25, 0, 1, 1.5])) * config.avail_h/8.5
            y_offset = pat // 6 * randint(c,d)
            pipe = Boss_attack(x, y, y_offset, (pat-1)//3, attack_set, config, False)
            val.append(pipe)
    elif (pat - 1) // 3 == 0:
        oui = [-2, -1, 0, 1, 2]
        for i in range(5):
            x_offset = (pat + 1) % 2 * 0.05 * config.pixel
            x = config.window_w * (1 + i * x_offset)
            y = config.avail_h / 2 + pat // 3 * oui[i] * (config.avail_h/5)
            y_offset =  (1 - pat // 3 * i%2 * 2) * oui[i] * config.ghost_vertic
            bird = Boss_attack(x, y, int(y_offset), (pat-1)//3, attack_set, config, False)
            val.append(bird)
    else:
        flyless = randint(0,5) if level <= 0.2 * config.avail_h else 4
        for i in range(4):
            y = (i + 0.5) * (config.avail_h - config.mush_h)/4
            y_offset = pat % 5 * (1 - pat // 8 * i % 2 * 2)*(1 - pat// 9 * (i + 1)%2)
            fish = Boss_attack(config.window_w, y, y_offset, (pat-1)//3, attack_set, config, i == flyless) 
            val.append(fish)
    return val

def random_water(level, config: Config):
    if level > config.avail_h/2:
        return choice([0.1, 0.2, 0.3])*config.avail_h
    else:
        return choice([0.9, 0.7, 0.8])*config.avail_h

class Play():
    def __init__(self) -> None:
        self.clock = pygame.time.Clock()
        self.config = Config()
        self.screen = self.config.show_window()
        self.image = Image(self.config)
        pygame.event.set_blocked(MOUSEMOTION) 
        self.state = 0
        self.reseted = False
        self.endless = True
        self.quit = False
        self.pause = False
        self.button = Button(self.config, self.image.button_set, self.image.number_set) 
        self.valid_key = [K_SPACE, K_p, K_s, K_t, K_m, K_w, K_RIGHT, K_r]
        self.attack = pygame.sprite.Group()
        self.base = pygame.sprite.Group()
        self.pipe = pygame.sprite.Group()
        self.score = Score(0, self.image.number_set, self.config)
        self.bird = Bird(self.image.bird_set, self.config)
        self.boss = Boss(self.image.boss_set, self.config)
        self.water = Water(self.image.water_im, self.config)
        self.mode = [self.menu,self.wait, self.play, self.boss_fight, self.game_over, self.win, self.win_message]
        self.reset()
        self.run()

    def menu(self):
        if not self.reseted:
            self.reset()
    
    def wait(self):
        if not self.reseted:
            self.reset()
        self.bird.wait()
     

    def play(self): 
        self.reseted = False   
        if self.pipe.sprites()[0].out_the_window():
            self.score.add()
            self.config.sound.point.play()
            if self.endless:
                direct = choice([-1,0,1,0]) if self.score.score > 10 else 0
                offset = choice([0.7, 0.6, 0.5])*self.config.avail_h
                for pipe in self.pipe.sprites():
                    pipe.reposi(offset, direct)
            else:
                self.pipe.empty()
                self.score.set(self.boss.health)
                boss_pipe = Pipe(False, self.config.window_w, 
                (self.config.avail_h + self.boss.rect[3])/2, self.image.pipe_set, self.config)
                self.pipe.add(boss_pipe)
                self.state = 3

        if self.score.score != 0 and self.score.score % 23 == 0:
            self.water.fluctuate(0)
        elif self.score.score % 29 == 0:
            self.water.fluctuate(self.config.window_h)
        if self.pause == False:
            self.water.update()
            self.base.update()
            self.pipe.update()
            self.bird.update(self.water.level)

    def boss_fight(self):
        self.bg = 1
        boss_pipe = self.pipe.sprites()[0].boss()
        self.boss.boss_fight()
        self.power_cycle()
        self.boss_control(boss_pipe)

        if len(self.attack) == 0:
            self.power_wait += 1 if self.power_wait <= 6 else 0
            self.power_last += 1 if self.power_last >= 0 else 0
            self.water_last += 1 if self.water_last >= 0 else 0
            self.attack.empty()
            new_attack = random_attack(self.boss.health, self.de_level, self.image.bos_att_set, self.config)
            self.attack.add(new_attack)

        self.water.fluctuate(self.de_level)
        self.bird.update(self.water.level) 
        self.attack.update()
        self.power.update(self.power_wait)
        self.player_attack.update(self.bird)

    def boss_control(self, boss_pipe):
        if self.boss.hit(self.player_attack):
            self.score.sub()
            self.hurt = True 
            if self.boss.rect[1] >= (self.config.avail_h - self.config.boss_h)/2:
                self.offset = choice([0.2, 0.3, 0.4]) * (self.config.avail_h - self.config.boss_h)
            else: 
                self.offset = choice([0.6, 0.7, 0.8]) * (self.config.avail_h - self.config.boss_h)
            self.direct = -1 if self.boss.rect[1] >= self.offset else 1
            self.player_attack = Player_attack(-1.5*self.config.window_w, self.offset,
                                            self.image.play_att_set, self.config)
        
        if self.boss.boss_die():
            self.attack.empty()
            self.power.rect[1] = self.config.window_h
            self.state = 5
         
        if self.hurt:
            self.boss.fly()
            self.boss.boss_run(self.offset, self.direct)  
            if self.pipe.sprites()[0].out_the_window():
                self.pipe.sprites()[0].reposi(self.offset + self.boss.rect[3], 0)  
            if boss_pipe:
                self.hurt = False
                self.boss.land()
            else:
                self.pipe.sprites()[0].pipe_run()

        if self.boss.phase_2():
            self.water.update()

        if self.water_last % 4 == 0:
            self.de_level = random_water(self.water.level, self.config) 
        
        if self.water.changing():
            self.water_last = 1
        
    def power_cycle(self):
        if self.power_wait == 3:
            self.power = Power_up(random_power_up(), self.image.power_up_set, self.config)
            self.power_wait += 1
        if self.power_wait <= 6:
            if self.bird.power_up(self.power.use(self.bird)):
                self.power_last = 0
                self.power_wait = 7
        else:
            self.power_wait = 0
        if self.power_last >= 3:
            self.bird.reset()
            self.power_wait = 0
            self.power_last = -1

    def game_over(self):
        self.button.stat()
        self.bird.update(self.water.level)

    def win(self):  
        self.bg = 0
        self.boss.fly()
        self.bird.reset()
        self.attack.add(self.boss)
        self.water.fluctuate(self.config.window_h)
        self.water.update()
        self.bird.update(self.water.level)
        if self.boss.die(self.bird.rect[0], self.bird.rect[1]):
            self.pipe.update()
            Pipe.direct = 1
        if self.pipe.sprites()[0].out_the_window():
            self.pipe.empty()
        if len(self.pipe) == 0:
            self.config.victory_count += 1
            self.state = 6

    def win_message(self):
        pass # play thank message

    def tap_event(self, event):
        x,y,key = -1,-1,K_SPACE
        valid = False
        if event.type == QUIT:
            self.config.save()
            sys.exit()
            self.quit = True
        elif event.type == KEYDOWN:
            key = event.key
            x = 0
            valid = key in self.valid_key
        elif event.type == FINGERDOWN:
                x,y =  event.x, event.y
                valid = True
        elif event.type == MOUSEBUTTONDOWN:
            x,y = event.pos[0], event.pos[1]
            valid = True
        if valid:
            self.state, self.endless, self.pause = self.button.check_button_tap(
                                    self.state, self.endless, self.pause, x,y, key)
            if self.state in [2,3,5] and not self.button.pause and (
            (event.type == KEYDOWN and event.key == K_SPACE) or event.type != KEYDOWN):
                self.bird.fly()                   

    def reset(self):
        self.bg = 0
        self.power_wait = 0
        self.power_last = -1
        self.water_last = 1
        self.offset = 0
        self.direct = 1
        self.de_level = 0.25 * self.config.avail_h
        self.hurt = False 
        self.score.set(0)
        self.bird.reposition()
        self.boss.reset()
        self.water.reset()
        self.attack.empty()
        self.base.empty()
        self.pipe.empty()
        self.power = Power_up(random_power_up(), self.image.power_up_set, self.config)

        at1 = Boss_attack(1.35 * self.config.window_w, 0, 0, 1,
                          self.image.bos_att_set, self.config, False)
        
        at2 = Boss_attack(1.35 * self.config.window_w, 
                          (self.config.avail_h - self.config.pipe_w)/2,
                           0, 1, self.image.bos_att_set, self.config, False)
        
        at3 = Boss_attack(1.35 * self.config.window_w, 
                          self.config.avail_h - 1.5*self.config.pipe_w,
                           0, 1, self.image.bos_att_set, self.config, False)
        
        self.player_attack = Player_attack(-2*self.config.window_w, 
                            (self.config.avail_h - self.config.boss_h)/2,
                            self.image.play_att_set, self.config)
        
        self.attack.add(at1, at2, at3)
        for i in range (2):
            base = Base(self.config.base_w * i, self.image.base_im, self.config)
            pipe = Pipe(i==1, self.config.window_w, 0.6 * self.config.avail_h, self.image.pipe_set, self.config) 
            self.pipe.add(pipe)
            self.base.add(base)
        self.reseted = True

    def update(self):
        self.mode[self.state]()
        if  self.state != 4 and self.bird.collided(self.pipe, self.attack):
            self.config.sound.hit.play()
            self.config.sound.die.play()
            self.config.hi_score = max(self.config.hi_score, self.score.score)
            self.config.min_boss_hp = min(self.config.min_boss_hp, self.boss.health)
            if self.endless:
                self.config.endless_play += 1
            else:
                self.config.story_play += 1
            self.state = 4
        self.draw()

    def draw(self):
        self.screen.blit(self.image.background_set[self.bg], (0, 0))
        if self.state != 0:
            if self.endless:
                self.pipe.draw(self.screen)
            else:  
                self.player_attack.draw(self.screen)
                self.power.draw(self.screen)
                self.boss.draw(self.screen)
                self.pipe.draw(self.screen)
                self.attack.draw(self.screen)
            self.bird.draw(self.screen) 
            self.score.draw2(self.screen)
            self.screen.blit(self.image.base_fill, (0, self.config.window_h - self.config.fill_1))
            self.base.draw(self.screen)
            self.water.draw(self.screen)
        self.button.draw(self.screen, self.state, self.endless)
        if self.state == 4:
            self.score.draw(0.5 * self.config.window_w + 0.436 * self.config.gover_w, 
                0.58 * self.config.window_h - 0.3 * self.config.gover_h, self.screen)
        elif self.state == 1:
            self.screen.blit(self.image.message, 
            ((self.config.window_w - self.config.mess_w)/2, self.config.avail_h - 2*self.config.mess_h))
        pygame.display.update()

    def run(self):
        while not self.quit:
            self.clock.tick(self.config.fps)
            for event in pygame.event.get():
                self.tap_event(event)
            self.update()
        pygame.quit()
