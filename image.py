import pygame

def loadify(imgname):
    return pygame.image.load(imgname).convert_alpha()

class Image:
    def __init__(self, config) -> None:
        self.number_set = [pygame.transform.scale(loadify('sprites/{}.png'.format(str(num))), (config.num_w, config.num_h))
                       if num != 1 else pygame.transform.scale(loadify('sprites/1.png'), (int(config.num_w*0.5), config.num_h))
                       for num in range(10)]
        
        self.bird_set = [pygame.transform.scale(loadify('sprites/upflap.png'), (config.bird_w, config.bird_h)),
                     pygame.transform.scale(loadify('sprites/halfup.png'), (config.bird_w, config.bird_h)),
                     pygame.transform.scale(loadify('sprites/midflap.png'), (config.bird_w, config.bird_h)),
                     pygame.transform.scale(loadify('sprites/halfdown.png'), (config.bird_w, config.bird_h)),
                     pygame.transform.scale(loadify('sprites/downflap.png'), (config.bird_w, config.bird_h)),
                     pygame.transform.scale(loadify('sprites/golden.png'), (config.bird_w, config.bird_h)),
                     pygame.transform.scale(loadify('sprites/downflap.png'), (int(config.bird_w*0.7), int(config.bird_h*0.7))),
                     pygame.transform.scale(loadify('sprites/halfdown.png'), (int(config.bird_w*0.7), int(config.bird_h*0.7))),
                     pygame.transform.scale(loadify('sprites/midflap.png'), (int(config.bird_w*0.7), int(config.bird_h*0.7))),
                     pygame.transform.scale(loadify('sprites/halfup.png'), (int(config.bird_w*0.7), int(config.bird_h*0.7))),
                     pygame.transform.scale(loadify('sprites/upflap.png'), (int(config.bird_w*0.7), int(config.bird_h*0.7)))]
        
        self.pipe_set = [pygame.transform.scale(loadify('sprites/trunk.png'), (config.pipe_w, config.pipe_h))]
        self.pipe_set.append(pygame.transform.flip(self.pipe_set[0], False, True))
        
        self.base_im = pygame.transform.scale(loadify('sprites/base.png'), (config.base_w, config.base_h))
        self.base_fill = pygame.transform.scale(loadify('sprites/fill.png'), (config.base_w, config.fill_1))
        
        self.boss_set = [pygame.transform.scale(loadify('sprites/boss stay.png'), (config.boss_w, config.boss_h)),
                         pygame.transform.scale(loadify('sprites/boss up.png'), (config.boss_w, config.boss_h)),
                         pygame.transform.scale(loadify('sprites/boss mid.png'), (config.boss_w, config.boss_h)),
                         pygame.transform.scale(loadify('sprites/boss down.png'), (config.boss_w, config.boss_h))]
        
        self.bos_att_set = [[pygame.transform.scale(loadify('sprites/bird1.png'), (config.ghost_w, config.ghost_h)),
                             pygame.transform.scale(loadify('sprites/bird3.png'), (config.ghost_w, config.ghost_h)),
                             pygame.transform.scale(loadify('sprites/bird2.png'), (config.ghost_w, config.ghost_h))],
                            [pygame.transform.rotate(self.pipe_set[0], 90)],
                            [pygame.transform.scale(loadify('sprites/fish1.png'),(config.mush_w, config.mush_h)),
                             pygame.transform.scale(loadify('sprites/fish2.png'), (config.mush_w, config.mush_h)),
                             pygame.transform.scale(loadify('sprites/fish3.png'), (config.mush_w, config.mush_h)),
                             pygame.transform.scale(loadify('sprites/fish4.png'), (config.mush_w, config.mush_h))]]
        
        self.play_att_set = [pygame.transform.scale(loadify('sprites/nest.png'), (config.bird_w/2, config.bird_h*0.6)),
                            pygame.transform.scale(loadify('sprites/egg.png'), (config.patt_w, config.patt_h))]

        self.power_up_set = [None, pygame.transform.scale(loadify('sprites/lightmush.png'),(config.power_w, config.power_h)),
                            pygame.transform.scale(loadify('sprites/darkmush.png'),(config.power_w, config.power_h*1.3))]
        
        self.water_im = pygame.transform.scale(loadify('sprites/flood.png'), (config.window_w, config.window_h))
        pygame.Surface.set_alpha(self.water_im, 100)

        self.background_set = [pygame.transform.scale(loadify('sprites/background-day.png'), (config.window_w, config.window_h)),
                               pygame.transform.scale(loadify('sprites/background-night.png'), (config.window_w, config.window_h))]
        
        self.message = pygame.transform.scale(loadify('sprites/message.png'), (config.mess_w, config.mess_h))
        
        self.begin_im = loadify('sprites/message.png')
        
        self.button_set = [pygame.transform.scale(loadify('sprites/story.png'), (config.button_w, config.button_h)), #0
                           pygame.transform.scale(loadify('sprites/lock.png'), (config.button_w, config.button_h)), #1
                           pygame.transform.scale(loadify('sprites/endless.png'), (config.button_w, config.button_h)),#2
                           pygame.transform.scale(loadify('sprites/stat.png'), (config.button_w, config.button_h)),#3
                           pygame.transform.scale(loadify('sprites/setting.png'), (config.button_h, config.button_h)), #4
                           pygame.transform.scale(loadify('sprites/pause.png'), (config.button_h, config.button_h)), #5
                           pygame.transform.scale(loadify('sprites/resume.png'), (config.button_h, config.button_h)), #6
                           pygame.transform.scale(loadify('sprites/mute.png'), (config.button_h, config.button_h)),#7
                           pygame.transform.scale(loadify('sprites/unmute.png'), (config.button_h, config.button_h)),#8
                           pygame.transform.scale(loadify('sprites/menu.png'), (config.button_h, config.button_h)),#9
                           pygame.transform.scale(loadify('sprites/wiki.png'), (config.button_h, config.button_h)),#10
                           pygame.transform.scale(loadify('sprites/return.png'), (config.button_h, config.button_h)), #11
                           pygame.transform.scale(loadify('sprites/game over.png'), (config.gover_w, config.gover_h)), #12
                           pygame.transform.scale(loadify('sprites/restart.png'), (config.button_h, config.button_h)), #13
                           pygame.transform.scale(loadify('sprites/bback.png'), (config.window_w, config.window_h)),#14
                           pygame.transform.scale(loadify('sprites/stat board.png'), (config.statboard_w, config.statboard_h)),#15
                           [pygame.transform.scale(loadify('sprites/w unknown.png'), (config.wiki_w, config.wiki_h)),
                           pygame.transform.scale(loadify('sprites/w nest.png'), (config.wiki_w, config.wiki_h)),
                           pygame.transform.scale(loadify('sprites/w darkmush.png'), (config.wiki_w, config.wiki_h)),
                           pygame.transform.scale(loadify('sprites/w lightmush.png'), (config.wiki_w, config.wiki_h)),
                           pygame.transform.scale(loadify('sprites/w exh.png'), (config.wiki_w, config.wiki_h)),
                           pygame.transform.scale(loadify('sprites/w water.png'), (config.wiki_w, config.wiki_h)),
                           pygame.transform.scale(loadify('sprites/w fish.png'), (config.wiki_w, config.wiki_h))]] 
