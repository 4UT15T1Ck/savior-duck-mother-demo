import pygame
from config import Config

class Image:
    def __init__(self, config: Config) -> None:
        self.number_set = [pygame.transform.scale(pygame.image.load('sprites/{}.png'.format(str(num))), (config.num_w, config.num_h))
                       if num != 1 else pygame.transform.scale(pygame.image.load('sprites/1.png'), (int(config.num_w*0.7), config.num_h))
                       for num in range(10)]
        
        self.bird_set = [pygame.transform.scale(pygame.image.load('sprites/bluebird-upflap.png'), (config.bird_w, config.bird_h)),
                     pygame.transform.scale(pygame.image.load('sprites/bluebird-downflap.png'), (config.bird_w, config.bird_h)),
                     pygame.transform.scale(pygame.image.load('sprites/bluebird-midflap.png'), (config.bird_w, config.bird_h)),
                     pygame.transform.scale(pygame.image.load('sprites/yellowbird-midflap.png'), (config.bird_w, config.bird_h)),
                     pygame.transform.scale(pygame.image.load('sprites/bluebird-midflap.png'), (int(config.bird_w*0.7), int(config.bird_h*0.7))),
                     pygame.transform.scale(pygame.image.load('sprites/bluebird-downflap.png'), (int(config.bird_w*0.7), int(config.bird_h*0.7))),
                     pygame.transform.scale(pygame.image.load('sprites/bluebird-upflap.png'), (int(config.bird_w*0.7), int(config.bird_h*0.7)))]
        
        self.pipe_set = [pygame.transform.scale(pygame.image.load('sprites/pipe-green.png'), (config.pipe_w, config.pipe_h))]
        self.pipe_set.append(pygame.transform.flip(self.pipe_set[0], False, True))
        
        self.base_im = pygame.transform.scale(pygame.image.load('sprites/base.png'), 
                    (config.base_w, config.base_h))
        
        self.boss_set = [pygame.transform.scale(pygame.image.load('sprites/stand.png'), (config.boss_w, config.boss_h)),
                         pygame.transform.scale(pygame.image.load('sprites/hurt.png'), (config.boss_w, config.boss_h))]
        
        self.bos_att_set = [pygame.transform.scale(pygame.image.load('sprites/ghost.png'), (config.ghost_w, config.ghost_h)),
                            pygame.transform.rotate(self.pipe_set[0], 90),
                            pygame.transform.scale(pygame.transform.rotate(pygame.image.load('sprites/cutemushroom.png'), 90), 
                            (config.mush_w, config.mush_h))]
        
        self.play_att_set = [pygame.transform.scale(pygame.image.load('sprites/nest.png'), (config.bird_w, config.bird_h)),
        pygame.transform.rotate(pygame.transform.scale(pygame.image.load('sprites/egg.png'), (config.patt_w, config.patt_h)), 180)]

        self.power_up_set = [None, pygame.transform.scale(pygame.image.load('sprites/golden mush.png'),(config.mush_w*1.5, config.mush_h*1.5)),
                            pygame.transform.scale(pygame.image.load('sprites/tiny mush.png'),(config.mush_w*1.5, config.mush_h*1.5))]
        
        self.water_im = pygame.transform.scale(pygame.image.load('sprites/flood.png'), (config.window_w, config.window_h))
        pygame.Surface.set_alpha(self.water_im, 100)

        self.background_set = [pygame.transform.scale(pygame.image.load('sprites/background-day.png'), (config.window_w, config.window_h)),
                               pygame.transform.scale(pygame.image.load('sprites/background-night.png'), (config.window_w, config.window_h))]
        
        self.begin_im = pygame.image.load('sprites/message.png')
        
        self.button_set = [pygame.transform.scale(pygame.image.load('sprites/background_wanabe.png'), (0.4 * config.window_w, config.window_h/10))]


con = Config()       
im = Image(con)