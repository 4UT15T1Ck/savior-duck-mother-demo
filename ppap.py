 
import pygame, os, sys
from pygame.locals import *
from random import randint, choice
import pickle
from math import floor

WIDTH, HEIGHT = 450, 800 # 16 : 9 WIDTH : 850
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SAVIOR DUCK MOTHER!!!')
pygame.event.set_blocked(MOUSEMOTION)

################### SIZE #########################

FPS = 60
BIRD_WIDTH, BIRD_HEIGHT     = 0.12 * WIDTH, 0.08 * WIDTH
BOX_WIDTH, BOX_HEIGHT       = 0.6 * WIDTH, 0.1 * HEIGHT
PIPE_WIDTH, PIPE_HEIGHT     = 0.18 * WIDTH, 0.6 * HEIGHT
GOV_WIDTH, GOV_HEIGHT       = 0.75 * WIDTH, 0.15 * WIDTH
NUM_WIDTH, NUM_HEIGHT       = 0.05 * WIDTH, 0.08 * WIDTH
RES_WIDTH, RES_HEIGHT       = 0.75 * WIDTH, 0.3 * WIDTH
WIN_WIDTH, WIN_HEIGHT       = 0.9 * WIDTH, 0.45 * WIDTH
HSCORE_WIDTH, HSCORE_HEIGHT = 0.4 * WIDTH, 0.1 * WIDTH
BASE_WIDTH, BASE_HEIGHT     = WIDTH, (HEIGHT - 4/3*WIDTH)/2
BOSS_WIDTH, BOSS_HEIGHT     = PIPE_WIDTH, 1.2 * PIPE_WIDTH
EGG_WIDTH, EGG_HEIGHT       = 0.064 * WIDTH, 0.048 * WIDTH
MUSH_WIDTH, MUSH_HEIGHT     = 0.08 * WIDTH, 0.064 * WIDTH
GHOST_WIDTH, GHOST_HEIGHT   = 0.128 * WIDTH, 0.112 * WIDTH
AVAIL_HEIGHT = HEIGHT - BASE_HEIGHT
GHOST_SPEED                 = WIDTH/90
GHOST_VERTICAL_SPEED        = WIDTH//180
PIPE_SPEED                  = WIDTH//20
MUSH_SPEED                  = WIDTH//90
INTRO_SPEED                 = WIDTH/450
SPEED                       = 5 
GRAVITY                     = 0.2 
GAME_SPEED                  = WIDTH//90

###########################################################

GAME_OVER = pygame.image.load(os.path.join('sprites', 'gameover.png'))
GAME_OVER_SCREEN = pygame.transform.scale(GAME_OVER, (GOV_WIDTH, GOV_HEIGHT))
BACKGROUND = pygame.image.load('sprites/background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))
NIGHTTIME = pygame.image.load(os.path.join('sprites', 'background-night.png'))
BOSS_FIGHT = pygame.transform.scale(NIGHTTIME, (WIDTH, HEIGHT))
BEGIN_IMAGE = pygame.image.load('sprites/message.png').convert_alpha()
BOS = pygame.image.load('sprites/stand.png')
HUR = pygame.image.load(os.path.join('sprites', 'hurt.png'))
MUS = pygame.image.load(os.path.join('sprites', 'cutemushroom.png'))
MUSS = pygame.transform.rotate(MUS, 90)
GO = pygame.image.load(os.path.join('sprites', 'ghost.png'))
PIP = pygame.image.load('sprites/pipe-green.png')
PIPE = pygame.transform.scale(PIP, (PIPE_WIDTH, PIPE_HEIGHT))
EG = pygame.image.load(os.path.join('sprites', 'egg.png'))
NES = pygame.image.load(os.path.join('sprites', 'nest.png'))
GOL_MUSH = pygame.image.load('sprites/golden mush.png')
SMO_MUSH = pygame.image.load('sprites/tiny mush.png')
FLOODING = pygame.image.load(os.path.join('sprites', 'flood.png'))
BB = pygame.image.load('sprites/background_wanabe.png')
BBB = pygame.transform.scale(BB, (0.6 * WIDTH, HEIGHT/10))

class Bird(pygame.sprite.Sprite):

    def __init__(self) ->None:
        pygame.sprite.Sprite.__init__(self)

        self.im =  [pygame.image.load('sprites/bluebird-upflap.png'),
                        pygame.image.load('sprites/bluebird-downflap.png'),
                        pygame.image.load('sprites/bluebird-midflap.png'),
                        pygame.image.load('sprites/yellowbird-midflap.png')]

        self.images = [pygame.transform.scale(self.im[0], (BIRD_WIDTH, BIRD_HEIGHT)),
                       pygame.transform.scale(self.im[1], (BIRD_WIDTH, BIRD_HEIGHT)),
                       pygame.transform.scale(self.im[2], (BIRD_WIDTH, BIRD_HEIGHT))]

        self.speed = SPEED
        self.max_fall_speed = SPEED
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
            self.speed += self.debuff * GRAVITY
            self.current_image = 0 if self.speed < -3 else 1 if self.speed < 0 else 2
        self.image = self.images[self.current_image]
        if self.rect[1] < AVAIL_HEIGHT - self.image.get_height() + 1:
            if abs(self.rect[1] + self.rect[3] - level) < self.speed:
                self.rect[1] = level - self.rect[3]
                self.angle = -30
            else: self.rect[1] += self.in_water * self.speed
        self.image = pygame.transform.rotozoom(self.image, self.in_water * self.angle, 1)
        if self.angle > -60 and self.speed >= 0:
            self.angle -= 0.8 * abs(self.speed)
        if self.angle < 60 and self.speed < 0:
            self.angle += abs(self.speed)
        
    def fly(self):
        self.speed = -SPEED / self.debuff
    
    def power_up(self, power):
        self.power = abs(power) if power != 0 else self.power
        if power < 0:
            self.debuff = 1.2
        if abs(power) == 1:
            self.images[2] = pygame.transform.scale(self.im[3], (BIRD_WIDTH, BIRD_HEIGHT))
            return True
        elif abs(power) == 2:
            for i in range(3):
                self.images[i] = pygame.transform.scale_by(self.images[i], 0.7)
            self.image = self.images[floor(self.current_image)]
            self.rect.scale_by_ip(0.7)
            self.rect[0] = WIDTH / 15
            return True
        return False
        
    def invincibility(self):
        if self.power == 1 and self.speed > 0:
            return True
        return False
    
    def settle(self, mov_x, mov_y):
        self.image = self.images[2]
        if HEIGHT - BASE_HEIGHT - self.rect[3] - self.rect[1] <= mov_y:
            self.rect[1] = HEIGHT - BASE_HEIGHT - self.rect[3]
            return True
        else:
            self.rect[1] += mov_y
            self.rect[0] += mov_x
            return False

    def reposition(self):
        self.image = self.images[2]
        self.rect[0] = WIDTH / 15
        self.rect[1] = AVAIL_HEIGHT /2
        self.angle = 0
        self.reset()
        self.in_water = 1

    def reset(self):
        if self.power != 0:
            for i in range(3):
                self.images[i] = pygame.transform.scale(self.im[i], (BIRD_WIDTH, BIRD_HEIGHT))
            self.image = self.images[floor(self.current_image)]
            self.rect = self.rect.scale_by(self.power)
            self.rect[0] = WIDTH / 15
            self.power = 0
            self.debuff = 1

    def draw(self):
        screen.blit(self.image, (self.rect[0], self.rect[1]))

class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.inverted = inverted
        self.image = PIPE
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.go_boss = True

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = y - 6*BIRD_HEIGHT - self.rect[3]
        else:
            self.rect[1] = y
    
    def y_move(self, dir):
        if self.inverted:
            if self.rect[1] + self.rect[3] >= 2*SPEED:
                self.rect[1] += dir * SPEED * 0.8
            else:
                self.rect[1] = 2*SPEED - self.rect[3] 
                return True
        else:
            if AVAIL_HEIGHT - self.rect[1] >= 2*SPEED:
                self.rect[1] += dir * SPEED * 0.8
            else:
                self.rect[1] = AVAIL_HEIGHT - 2*SPEED 
                return True
        return False

    def update(self):
        self.rect[0] -= GAME_SPEED
    
    def boss(self):
        if self.rect[1] > (AVAIL_HEIGHT + BOSS_HEIGHT)/2 and self.go_boss:
            self.rect[1] -= GAME_SPEED
        else:
            self.go_boss = False 
    
    def pipe_run(self, goal, direct):
        if abs(self.rect[1] - goal) > GAME_SPEED:
            self.rect[1] += direct * GAME_SPEED
        else:
            self.rect[1] = goal   

class Base(pygame.sprite.Sprite):
    
    def __init__(self, xpos) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (BASE_WIDTH, BASE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = AVAIL_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED
 
class Score(pygame.sprite.Sprite):

    def __init__(self) -> None:
        self.num = [pygame.image.load(os.path.join('sprites', '0.png')),
                        pygame.image.load(os.path.join('sprites', '1.png')),
                        pygame.image.load(os.path.join('sprites', '2.png')),
                        pygame.image.load(os.path.join('sprites', '3.png')),
                        pygame.image.load(os.path.join('sprites', '4.png')),
                        pygame.image.load(os.path.join('sprites', '5.png')),
                        pygame.image.load(os.path.join('sprites', '6.png')),
                        pygame.image.load(os.path.join('sprites', '7.png')),
                        pygame.image.load(os.path.join('sprites', '8.png')),
                        pygame.image.load(os.path.join('sprites', '9.png'))]
        self.score = 0
    
    def reset(self, stage):
        if stage == 2:
            self.score = 0
        else: self.score = 28

    def add(self):
        self.score += 1

    def boss_time(self):
        return self.score == 29

    def draw(self):
        if self.score < 10:
            screen.blit(self.num[self.score],((WIDTH - self.num[self.score].get_width())/2, AVAIL_HEIGHT *4/45))
        else:
            screen.blit(self.num[self.score%10],(WIDTH/2, AVAIL_HEIGHT *4/45))
            screen.blit(self.num[self.score//10],(WIDTH/2 - self.num[self.score//10].get_width(), AVAIL_HEIGHT *4/45))

class Boss(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.transform.scale(BOS, (BOSS_WIDTH, BOSS_HEIGHT)),
                       pygame.transform.scale(HUR, (BOSS_WIDTH, BOSS_HEIGHT))]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.image = self.images[0]
        self.rect[0] = WIDTH - self.image.get_width()
        self.rect[1] = HEIGHT  
        self.health = 20
        self.intro = True
        self.attack_choice = 0
        self.state = 0      

    def boss_fight(self):
        if self.intro:
            if abs(self.rect[1] - (AVAIL_HEIGHT - self.image.get_height())/2) > GAME_SPEED:
                self.rect[1] -= GAME_SPEED
            else:
                self.rect[1] = (AVAIL_HEIGHT - self.image.get_height())/2 - 2 * INTRO_SPEED
                self.intro = False

    def boss_hurt(self, goal, direct):
        if self.state < 1:
            self.state += 0.05
            self.image = self.images[1]
        return self.boss_run(goal, direct)

    def boss_run(self, goal, direct):
        if self.health > 0:
            if abs(self.rect[1] - goal) > GAME_SPEED:
                self.rect[1] += direct * GAME_SPEED
            else:
                self.rect[1] = goal
                self.image = self.images[0]
                self.state = 0
        else:
            if self.rect[1] < goal:
                self.rect[1] += SPEED
        return self.rect[1] != goal
    
    def hit(self):
        self.health -= 1

    def die(self):
        if self.rect[1] < HEIGHT:
            self.rect[1] += GAME_SPEED
            return False
        return True

    def boss_die(self):
        return self.health <= 0

    def phase_2(self):
        return self.health <= 10
    
    def draw(self):
        screen.blit(self.image, (self.rect[0], self.rect[1]))

class Boss_attack(pygame.sprite.Sprite):
    def __init__(self, x, y, y_offset, pat) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.transform.scale(GO, (GHOST_WIDTH,GHOST_HEIGHT)),
                       pygame.transform.rotate(PIPE, 90),
                       pygame.transform.scale(MUSS, (MUSH_WIDTH, MUSH_HEIGHT))]
        self.image = self.images[pat]
        self.rect = self.image.get_rect()
        self.rect[1] = y
        self.rect[0] = x
        self.pat = pat
        self.offset = y_offset
        self.direct = 1
        if pat == 2:
            self.up, self.down = y + WIDTH/4.5, y - WIDTH/4.5
        else:
            self.up, self.down = y + HEIGHT, y - HEIGHT

    def update(self):
        if self.rect[0] > WIDTH - PIPE_WIDTH:
            self.rect[0] -= INTRO_SPEED
        else:
            self.rect[0] -= (self.pat % 2 * 3.5 + 1) * GHOST_SPEED
            self.vertic_move()
    
    def vertic_move(self): 
        if self.rect[1] > self.up or self.rect[1] < self.down:
            self.direct *= -1
        self.rect[1] -= self.direct * self.offset

class Player_attack(pygame.sprite.Sprite):
    def __init__(self,x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.transform.scale(NES, (BIRD_WIDTH, BIRD_HEIGHT)),
                       pygame.transform.rotate(pygame.transform.scale(EG, (EGG_WIDTH, EGG_HEIGHT)), 180)]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect[1] = y
        self.rect[0] = x
        self.speed = GAME_SPEED
        self.limit = WIDTH / 15

    def update(self, bird):
        if self.rect[0] < self.limit:
            self.rect[0] += GAME_SPEED
        self.collide(bird)
    
    def collide(self, bird):
        if abs(bird.rect[1] - self.rect[1]) <= 3 and abs(bird.rect[0] - self.rect[0]) <= 3:
            self.image = self.images[1]
            self.speed *= 5
            self.limit = WIDTH
    
    def draw(self):
        screen.blit(self.image, (self.rect[0], self.rect[1]))

class Power_up(pygame.sprite.Sprite):
    def __init__(self, power) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.images = [MUS, pygame.transform.scale(GOL_MUSH,(1.5*MUSH_WIDTH, 1.5*MUSH_HEIGHT)),
                       pygame.transform.scale(SMO_MUSH,(1.5*MUSH_WIDTH, 1.5*MUSH_HEIGHT))]
        self.power = power
        self.image = self.images[abs(power)]
        self.rect  = self.image.get_rect()
        self.rect[0] = WIDTH/12 
        self.rect[1] = AVAIL_HEIGHT
        self.wait = 0

    def update(self, wait):
        if 3 <= wait < 7:
            if self.rect[1] + self.rect[3] > AVAIL_HEIGHT:
                self.rect[1] -= INTRO_SPEED
        elif wait == 7:
            self.rect[1] = AVAIL_HEIGHT 
    
    def use(self):
        return self.power
    
    def draw(self):
        screen.blit(self.image, (self.rect[0], self.rect[1]))

class Water(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image =  pygame.transform.scale(FLOODING, (WIDTH, HEIGHT))
        pygame.Surface.set_alpha(self.image, 100)
        self.level = HEIGHT
        self.desired_level = HEIGHT
        self.direction = -1 
    
    def reset(self):
        self.level = HEIGHT
    def update(self):
        if self.level > self.desired_level:
            self.direction = -1
        elif self.level < self.desired_level:
            self.direction = 1
        if abs(self.level - self.desired_level) > SPEED:
            self.level += self.direction * SPEED
        else:
            self.level = self.desired_level
        return self.level

    def fluctuate(self, level):
        self.desired_level = level   

    def changing(self):
        return self.level != self.desired_level 

    def draw(self):
        screen.blit(self.image, (0, self.level))

def collided(bird, base, pipe, attack):
    if bird.rect[1] <= -bird.rect[3]/10:
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

def random_pipes(x):
    y = randint( int(0.5*BASE_HEIGHT + 5*BIRD_HEIGHT), int(AVAIL_HEIGHT - 0.5*BASE_HEIGHT))
    pipe = Pipe(False, x, y)
    pipe_inverted = Pipe(True, x,y)
    return [pipe, pipe_inverted]

def random_attack(hp):
    a, b = (1, 6) if hp > 15 else (4, 9) if hp > 10 else (1, 9)
    pat = randint(a,b)
    val = []
    if (pat - 1) // 3 == 1:
        for i in range(1,4):
            c,d = (2,4) if i == 3 else (-4,-1) if i == 1 else (-4,4)
            x_offset = pat // 5 * i * choice([0.02, 0.03])
            x = WIDTH * (1 + i % 2 * x_offset)
            y = (3*(i - 1) + choice([-0.5, -0.25, 0, 1, 1.5])) * AVAIL_HEIGHT/8.5
            y_offset = pat // 6 * randint(c,d)
            pipe = Boss_attack(x, y, y_offset, (pat - 1) // 3)
            val.append(pipe)
    elif (pat - 1) // 3 == 0:
        oui = [-2, -1, 0, 1, 2]
        for i in range(5):
            x_offset = (pat + 1) % 2 * 0.05
            x = WIDTH * (1 + i * x_offset)
            y = AVAIL_HEIGHT / 2 + pat // 3 * oui[i] * BASE_HEIGHT
            y_offset =  (1 - pat // 3 * i%2 * 2) * oui[i] * GHOST_VERTICAL_SPEED
            ghost = Boss_attack(x, y, int(y_offset), (pat - 1) // 3)
            val.append(ghost)
    else:
        for i in range(4):
            y = (i + 0.5) * (AVAIL_HEIGHT - MUSH_HEIGHT)/4
            y_offset = pat % 5 * (1 - pat // 8 * i % 2 * 2)*(1 - pat// 9 * (i + 1)%2)
            mush = Boss_attack(WIDTH, y, y_offset, (pat - 1) // 3)
            val.append(mush)
    return val

def get_power(power, bird):
    if power.rect.colliderect(bird.rect.scale_by(1.3)):
        return power.use()
    return 0

def random_water(level):
    if level > AVAIL_HEIGHT/2:
        return choice([0.1, 0.2, 0.3])*AVAIL_HEIGHT
    else:
        return choice([0.9, 0.7, 0.8])*AVAIL_HEIGHT

class Play():
    def __init__(self) -> None:
        self.clock = pygame.time.Clock()
        self.dir = -1
        self.state = 0
        self.quit = False
        self.stage = 2
        self.attack = pygame.sprite.Group()
        self.base = pygame.sprite.Group()
        self.pipe = pygame.sprite.Group()
        self.score = Score()
        self.bird = Bird()
        self.boss = Boss()
        self.water = Water()
        self.mode = [self.menu,self.wait, self.play, self.boss_fight, self.game_over, self.win, self.win_message]
        self.load()
        self.reset()

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
        screen.blit(BACKGROUND, (0, 0))
        screen.blit(BBB, (0.2 * WIDTH, HEIGHT * 0.6))
    
    def wait(self):
        self.reset()
        screen.blit(BACKGROUND, (0, 0))
        screen.blit(BEGIN_IMAGE, (120, 150))

    def play(self):
        self.stage = self.state
        screen.blit(BACKGROUND, (0, 0))
        if is_off_screen(self.base.sprites()[0]):
            self.base.remove(self.base.sprites()[0])
            new_base = Base(BASE_WIDTH - 5)
            self.base.add(new_base)
        if is_off_screen(self.pipe.sprites()[0]):
            self.score.add()
            self.pipe.empty()
        if self.score.boss_time():
            boss_pipe = Pipe(False, WIDTH - PIPE_WIDTH, HEIGHT)
            self.pipe.add(boss_pipe)
            self.state = 3
        elif len(self.pipe) == 0:
            pipes = random_pipes(WIDTH + 10) 
            self.pipe.add(pipes)
        if self.score.score > 10 and self.score.score % 3 == 0:
            for pipe in self.pipe.sprites():
                if pipe.y_move(self.dir):
                    self.dir *= -1
        
        if self.score.score == 20:
            self.water.fluctuate(HEIGHT/2)
        elif self.score.score == 25:
            self.water.fluctuate(HEIGHT)
        self.water.update()
        self.base.update()
        self.pipe.update()
        self.bird.update(self.water.level)

    def boss_fight(self):
        self.stage = self.state
        screen.blit(BOSS_FIGHT,(0, 0))
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
            new_attack = random_attack(self.boss.health)
            self.attack.add(new_attack)

        self.water.fluctuate(self.de_level)
        self.bird.update(self.water.level) 
        self.attack.update()
        self.power.update(self.power_wait)
        self.player_attack.update(self.bird)

    def boss_control(self):
        if boss_hit(self.player_attack, self.boss):
            if self.boss.rect[1] >= (AVAIL_HEIGHT - BOSS_HEIGHT)/2:
                self.offset = choice([0.25, 0.35, 0.45]) * (AVAIL_HEIGHT - BOSS_HEIGHT)
            else: 
                self.offset = choice([0.55, 0.75, 0.65]) * (AVAIL_HEIGHT - BOSS_HEIGHT)
            self.direct = -1 if self.boss.rect[1] >= self.offset else 1
            self.hurt = True
            self.player_attack = Player_attack(-WIDTH, self.offset)  
        
        if self.boss.boss_die():
            self.attack.empty()
            self.power.rect[1] = HEIGHT
            self.state = 5
         
        if self.hurt:
            self.pipe.sprites()[0].pipe_run(self.offset + BOSS_HEIGHT, self.direct)
            self.hurt = self.boss.boss_hurt(self.offset, self.direct)
    

        if self.boss.phase_2():
            self.water.update()

        if self.water_last % 4 == 0:
            self.de_level = random_water(self.water.level) 
        
        if self.water.changing():
            self.water_last = 1
        
    def power_cycle(self):
        if self.power_wait == 3:
            self.power = Power_up(random_power_up())
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
        if self.bg:
            screen.blit(BOSS_FIGHT,(0, 0))
        else: screen.blit(BACKGROUND, (0, 0))

    def win(self):
        screen.blit(BACKGROUND, (0, 0))
        self.bg = 0
        self.bird.reset()
        self.water.fluctuate(HEIGHT)
        self.water.update()
        if self.boss.die():
            self.pipe.update()
        if len(self.pipe) > 0 and is_off_screen(self.pipe.sprites()[0]):
            self.score.add()
            self.pipe.empty()
            self.mov_x = (WIDTH * 0.6 - self.bird.rect[0])/120
            self.mov_y = (HEIGHT - BASE_HEIGHT - self.bird.rect[3] - self.bird.rect[1])/120
        if self.score.score == 30:
            if self.bird.settle(floor(self.mov_x), floor(self.mov_y)):
                self.victory_count += 1
                self.state = 6
        else:
            self.bird.update(self.water.level)

    def win_message(self):
        screen.blit(BACKGROUND, (0, 0))


    def tap_event(self, event):
        if event.type == QUIT:
            self.save()
            sys.exit()
            self.quit = True
        if event.type == KEYDOWN or event.type == FINGERDOWN or event.type == MOUSEBUTTONDOWN:
            x,y = 0,0
            if event.type == FINGERDOWN:
                x,y =  event.x, event.y
            elif event.type == MOUSEBUTTONDOWN:
                x,y = event.pos[0], event.pos[1]
            if self.state == 0:
                if (event.type == KEYDOWN and event.key == K_p) or (
                    0.2 * WIDTH < x < 0.8 * WIDTH and 0.6 * HEIGHT < y < 0.7 * HEIGHT):
                    self.reset()
                    self.state = 1
            elif self.state == 4:
                if (event.type == KEYDOWN and event.key == K_r) or (
                    0.2 * WIDTH < x < 0.8 * WIDTH and 0.6 * HEIGHT < y < 0.7 * HEIGHT):
                    self.reset()
                    self.state = 1
                elif (event.type == KEYDOWN and event.key == K_m) or (
                    0.2 * WIDTH < x < 0.8 * WIDTH and 0.72 * HEIGHT < y < 0.82 * HEIGHT):
                    self.reset()
                    self.state = 0
            elif self.state == 6:
                if (event.type == KEYDOWN and event.key == K_m) or (
                    0.2 * WIDTH < x < 0.8 * WIDTH and 0.6 * HEIGHT < y < 0.7 * HEIGHT):
                    self.reset()
                    self.state = 0                
            elif (event.type == KEYDOWN and event.key == K_SPACE) or (
                event.type == FINGERDOWN or event.type == MOUSEBUTTONDOWN):
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
        self.de_level = 0.2 * AVAIL_HEIGHT
        self.hurt = False 
        self.score.reset(self.stage)
        self.bird.reposition()
        self.boss.reset()
        self.water.reset()
        self.attack.empty()
        self.base.empty()
        self.pipe.empty()
        self.power = Power_up(random_power_up())
        at1 = Boss_attack(1.35 * WIDTH, 0, 0, 1)
        at2 = Boss_attack(1.35 * WIDTH, (AVAIL_HEIGHT - PIPE_WIDTH)/2, 0, 1)
        at3 = Boss_attack(1.35 * WIDTH, AVAIL_HEIGHT - 1.5*PIPE_WIDTH, 0, 1)
        self.player_attack = Player_attack(-2*WIDTH, (AVAIL_HEIGHT - BOSS_HEIGHT)/2)
        self.attack.add(at1, at2, at3)
        for i in range (2):
            base = Base(BASE_WIDTH * i) 
            self.base.add(base)
        pipes = random_pipes(1.2*WIDTH)
        self.pipe.add(pipes)

    def update(self):
        self.mode[self.state]()
        if self.score.score < 30 and self.state != 4 and (
            collided(self.bird, self.pipe, self.base, self.attack)):
            self.hi_score = max(self.hi_score, self.score.score)
            self.death_count += 1
            self.state = 4

    def draw(self):
        self.player_attack.draw()
        self.boss.draw()
        self.pipe.draw(screen)
        self.attack.draw(screen)
        if self.state != 0:
            self.bird.draw() 
            self.score.draw()
            self.power.draw()
            self.base.draw(screen)
        self.water.draw()
        if self.state == 4:
            screen.blit(pygame.transform.scale_by(BBB,(1, 3)), (0.2 * WIDTH, HEIGHT * 0.28))
            screen.blit(BBB, (0.2 * WIDTH, HEIGHT * 0.6))
            screen.blit(BBB, (0.2 * WIDTH, HEIGHT * 0.72))
        if self.state == 6:
            screen.blit(BBB, (0.2 * WIDTH, HEIGHT * 0.6))
        pygame.display.update()

    def run(self):
        while not self.quit:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                self.tap_event(event)
            self.update()
            self.draw()
        pygame.quit()

def main():
    play = Play()
    play.run()


if __name__ == "__main__":
    main()



