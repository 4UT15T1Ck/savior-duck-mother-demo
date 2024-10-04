import pygame, sys
from pygame.locals import *
from random import randint, choice
import pickle
from math import floor
from config import Config
from image import Image
from bird import Bird
from pipe import Pipe
from base_score import Base, Score
from boss import Boss
from attack import Boss_attack, Player_attack
from power_water import Power_up, Water 

def collided(bird, base, pipe, attack):
    if bird.rect[1] <= -bird.rect[3]/3:
        return True
    if pygame.sprite.spritecollide(bird, base, False, pygame.sprite.collide_mask):
        return True
    if pygame.sprite.spritecollide(bird, pipe, False, pygame.sprite.collide_mask):
            return True
    if bird.invincibility():
        if pygame.sprite.spritecollide(bird, attack, True, pygame.sprite.collide_mask):
            bird.reset()
            return False
    else:
        if pygame.sprite.spritecollide(bird, attack, False, pygame.sprite.collide_mask):
            return True
    return False

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2]) 

def boss_hit(player_attack, boss):
    if player_attack.rect.colliderect(boss.rect.scale_by(0.2,1)):
        boss.hit()
        return True
    return False

def random_power_up():
    return choice([1,1,1,-1,1,2,2,2,2,-2])

def random_pipes(x, pipe_set, config: Config):
    y = randint( int(config.avail_h*0.4), int(config.avail_h*0.8))
    pipe = Pipe(False, x, y, pipe_set, config)
    pipe_inverted = Pipe(True,x,y, pipe_set, config)
    return [pipe, pipe_inverted]

def random_attack(hp, attack_set, config: Config):
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
            pipe = Boss_attack(x, y, y_offset, (pat-1)//3, attack_set, config)
            val.append(pipe)
    elif (pat - 1) // 3 == 0:
        oui = [-2, -1, 0, 1, 2]
        for i in range(5):
            x_offset = (pat + 1) % 2 * 0.05
            x = config.window_w * (1 + i * x_offset)
            y = config.avail_h / 2 + pat // 3 * oui[i] * config.base_h
            y_offset =  (1 - pat // 3 * i%2 * 2) * oui[i] * config.ghost_vertic
            ghost = Boss_attack(x, y, int(y_offset), (pat-1)//3, attack_set, config)
            val.append(ghost)
    else:
        for i in range(4):
            y = (i + 0.5) * (config.avail_h - config.mush_h)/4
            y_offset = pat % 5 * (1 - pat // 8 * i % 2 * 2)*(1 - pat// 9 * (i + 1)%2)
            mush = Boss_attack(config.window_w, y, y_offset, (pat-1)//3, attack_set, config)
            val.append(mush)
    return val

def get_power(power, bird):
    if bird.rect.colliderect(power.rect.scale_by(1.5)):
        return power.use()
    return 0

def random_water(level, config: Config):
    if level > config.avail_h/2:
        return choice([0.1, 0.2, 0.3])*config.avail_h
    else:
        return choice([0.9, 0.7, 0.8])*config.avail_h

class Play():
    def __init__(self) -> None:
        self.clock = pygame.time.Clock()
        self.config = Config()
        self.image = Image(self.config)
        self.screen = self.config.show_window()
        pygame.event.set_blocked(MOUSEMOTION) 
        self.dir = -1
        self.state = 0
        self.endless = True
        self.quit = False
        self.attack = pygame.sprite.Group()
        self.base = pygame.sprite.Group()
        self.pipe = pygame.sprite.Group()
        self.score = Score(self.image.number_set, self.config)
        self.bird = Bird(self.image.bird_set, self.config)
        self.boss = Boss(self.image.boss_set, self.config)
        self.water = Water(self.image.water_im, self.config)
        self.mode = [self.menu,self.wait, self.play, self.boss_fight, self.game_over, self.win, self.win_message]
        self.load()
        self.reset()
        self.run()

    def load(self):
        with open('data.pkl', 'rb') as file:
            db = pickle.load(file)
            self.hi_score = db['hi_score']
            self.death_count = db['death_count']
            self.boss_challenge = db['boss_chall']
            self.victory_count = db['vic_count']

    def save(self):
        db = {'hi_score': self.hi_score, 'death_count': self.death_count,
              'boss_chall': self.boss_challenge, 'vic_count': self.victory_count}
        with open('data.pkl', 'wb') as file:
            pickle.dump(db, file)

    def menu(self):
        self.screen.blit(self.image.button_set[0], (0.3 * self.config.window_w, self.config.window_h * 0.6))
    
    def wait(self):
        self.reset()
        self.screen.blit(self.image.begin_im, (120, 150))

    def play(self):
        if is_off_screen(self.base.sprites()[0]):
            self.base.remove(self.base.sprites()[0])
            new_base = Base(self.config.window_w - 5, self.image.base_im, self.config)
            self.base.add(new_base)
        if is_off_screen(self.pipe.sprites()[0]):
            self.score.add()
            self.pipe.empty()
        if self.score.score and not self.endless:
            self.score.set(20)
            boss_pipe = Pipe(False, self.config.window_w - self.config.pipe_w, 
                             self.config.window_h, self.image.pipe_set, self.config)
            self.pipe.add(boss_pipe)
            self.state = 3
        elif len(self.pipe) == 0:
            pipes = random_pipes(self.config.window_w + 10, self.image.pipe_set, self.config) 
            self.pipe.add(pipes)
        if self.score.score > 10 and self.score.score % 3 == 0:
            for pipe in self.pipe.sprites():
                if pipe.y_move(self.dir):
                    self.dir *= -1
        if self.score.score != 0 and self.score.score % 23 == 0:
            self.water.fluctuate(0)
        elif self.score.score % 19 == 0:
            self.water.fluctuate(self.config.window_h)
        self.water.update()
        self.base.update()
        self.pipe.update()
        self.bird.update(self.water.level)

    def boss_fight(self):
        self.bg = 1
        self.pipe.sprites()[0].boss()
        self.boss.boss_fight()
        self.power_cycle()
        self.boss_control()

        if len(self.attack) and is_off_screen(self.attack.sprites()[-1]):
            self.power_wait += 1 if self.power_wait <= 6 else 0
            self.power_last += 1 if self.power_last >= 0 else 0
            self.water_last += 1 if self.water_last >= 0 else 0
            self.attack.empty()
            new_attack = random_attack(self.boss.health, self.image.bos_att_set, self.config)
            self.attack.add(new_attack)

        self.water.fluctuate(self.de_level)
        self.bird.update(self.water.level) 
        self.attack.update()
        self.power.update(self.power_wait)
        self.player_attack.update(self.bird)

    def boss_control(self):
        if boss_hit(self.player_attack, self.boss):
            self.score.sub()
            if self.boss.rect[1] >= (self.config.avail_h - self.config.boss_h)/2:
                self.offset = choice([0.25, 0.35, 0.45]) * (self.config.avail_h - self.config.boss_h)
            else: 
                self.offset = choice([0.55, 0.75, 0.65]) * (self.config.avail_h - self.config.boss_h)
            self.direct = -1 if self.boss.rect[1] >= self.offset else 1
            self.hurt = True
            self.player_attack = Player_attack(-self.config.window_w, self.offset,
                                               self.image.play_att_set, self.config)  
        
        if self.boss.boss_die():
            self.attack.empty()
            self.power.rect[1] = self.config.window_h
            self.state = 5
         
        if self.hurt:
            self.pipe.sprites()[0].pipe_run(self.offset + self.config.boss_h, self.direct)
            self.hurt = self.boss.boss_hurt(self.offset, self.direct)
    

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
            if self.bird.power_up(get_power(self.power, self.bird)):
                self.power_last = 0
                self.power_wait = 7
        else:
            self.power_wait = 0
        if self.power_last >= 3:
            self.bird.reset()
            self.power_wait = 0
            self.power_last = -1

    def game_over(self):
        pass

    def win(self):
        self.bg = 0
        self.bird.reset()
        self.water.fluctuate(self.config.window_h)
        self.water.update()
        if self.boss.die():
            self.pipe.update()
        if len(self.pipe) > 0 and is_off_screen(self.pipe.sprites()[0]):
            self.score.add()
            self.pipe.empty()
            self.mov_x = (self.config.window_w * 0.6 - self.bird.rect[0])/120
            self.mov_y = (self.config.window_h - self.config.base_h
                           - self.bird.rect[3] - self.bird.rect[1])/120
        if self.score.score == 30:
            if self.bird.settle(floor(self.mov_x), floor(self.mov_y)):
                self.victory_count += 1
                self.state = 6
        else:
            self.bird.update(self.water.level)

    def win_message(self):
        pass
    def tap_event(self, event):
        choice = -1
        if event.type == QUIT:
            self.save()
            sys.exit()
            self.quit = True
        elif event.type == FINGERDOWN or event.type == MOUSEBUTTONDOWN:
            choice = 2
            x,y = 0,0
            if event.type == FINGERDOWN and (self.state == 0 or self.state == 4):
                x,y =  event.x, event.y
            elif event.type == MOUSEBUTTONDOWN and (self.state == 0 or self.state == 4):
                x,y = event.pos[0], event.pos[1]
            if 0.3 * self.config.window_w < x < 0.7 * self.config.window_w and (
                0.6 * self.config.window_h < y < 0.7 * self.config.window_h):
                choice = 0
            elif 0.3 * self.config.window_w < x < 0.7 * self.config.window_w and (
                0.72 * self.config.window_h < y < 0.82 * self.config.window_h):
                choice = 1
        elif event.type == KEYDOWN:
            if event.key == K_p:
                choice = 0
            elif event.key == K_b:
                choice = 1
            elif event.key == K_SPACE:
                choice = 2
        if choice == 0:
            if self.state == 0 or self.state == 4:
                self.state = 1
                self.endless = True
        elif choice == 1 and self.hi_score >= 50:
            if self.state == 0 or self.state == 4:
                self.state = 1
                self.endless = False  
        elif choice == 2:
            if self.state == 1:
                self.state = 2
            self.bird.fly()            

    def reset(self):
        self.bg = 0
        self.power_wait = 0
        self.power_last = -1
        self.water_last = 1
        self.offset = 0
        self.direct = 1
        self.de_level = 0.2 * self.config.avail_h
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
                          self.image.bos_att_set, self.config)
        
        at2 = Boss_attack(1.35 * self.config.window_w, 
                          (self.config.avail_h - self.config.pipe_w)/2,
                           0, 1, self.image.bos_att_set, self.config)
        
        at3 = Boss_attack(1.35 * self.config.window_w, 
                          self.config.avail_h - 1.5*self.config.pipe_w,
                           0, 1, self.image.bos_att_set, self.config)
        
        self.player_attack = Player_attack(-2*self.config.window_w, 
                            (self.config.avail_h - self.config.boss_h)/2,
                            self.image.play_att_set, self.config)
        
        self.attack.add(at1, at2, at3)
        for i in range (2):
            base = Base(self.config.base_w * i, self.image.base_im, self.config) 
            self.base.add(base)
        pipes = random_pipes(1.2*self.config.window_w, self.image.pipe_set, self.config)
        self.pipe.add(pipes)

    def update(self):
        self.mode[self.state]()
        if  self.state != 4 and collided(self.bird, self.pipe, self.base, self.attack):
            self.hi_score = max(self.hi_score, self.score.score)
            self.death_count += 1
            self.state = 4

    def draw(self):
        self.screen.blit(self.image.background_set[self.bg], (0, 0))
        self.player_attack.draw(self.screen)
        self.boss.draw(self.screen)
        self.pipe.draw(self.screen)
        self.attack.draw(self.screen)

        if self.state != 0:
            self.bird.draw(self.screen) 
            self.score.draw(self.screen)
            self.power.draw(self.screen)
            self.base.draw(self.screen)
        self.water.draw(self.screen)
        
        if self.state == 4 or self.state == 0:
            self.screen.blit(self.image.button_set[0], (0.3 * self.config.window_w, self.config.window_h * 0.6))
            self.screen.blit(self.image.button_set[0], (0.3 * self.config.window_w, self.config.window_h * 0.72))
            if self.state == 4:
                self.screen.blit(pygame.transform.scale_by(self.image.button_set[0],(1, 3)),
                             (0.3 * self.config.window_w, self.config.window_h * 0.28))
        if self.state == 6:
            self.screen.blit(self.image.button_set[0], (0.3 * self.config.window_w, self.config.window_h * 0.6))
        pygame.display.update()

    def run(self):
        while not self.quit:
            self.clock.tick(self.config.fps)
            for event in pygame.event.get():
                self.tap_event(event)
            self.update()
            self.draw()
        pygame.quit()



