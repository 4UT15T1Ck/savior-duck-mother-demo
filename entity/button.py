import pygame
from pygame.locals import *
from .base_score import Score

class Button (pygame.sprite.Sprite):
    def __init__(self, config, button_set, num_set):
        pygame.time.Clock().tick(config.fps)
        self.button_set = button_set
        self.config = config
        self.background = button_set[14]
        self.clarity = 0
        self.boss_unlock = 0 if self.config.hi_score >= 30 else 1
        self.pause = False
        self.in_setting = False
        self.read_wiki = False
        self.read_stat = False
        self.mode_x_posi = (config.window_w - config.button_w)/2
        self.first_row = 0.6 * config.window_h
        self.right_corner = (config.window_w - config.button_h - 1,2)
        self.butt_dic = {
            0: [self.boss_unlock, (self.mode_x_posi, self.first_row + 1.2 * config.button_h),
                 2, (self.mode_x_posi, self.first_row),
                 4, self.right_corner],
            2: [ 5, self.right_corner],
            4: [12, ((config.window_w - config.gover_w)/2, 0.58 * config.window_h - config.gover_h),
                 9, (self.mode_x_posi, self.first_row),
                13, (self.mode_x_posi + 1.32 * config.button_h, self.first_row),
                 1, (self.mode_x_posi, self.first_row + 1.2 * config.button_h)] 
        }
        self.pause_dic = [9, ((config.window_w - config.button_h)/2, self.first_row),
                          6, (self.mode_x_posi, self.first_row - 1.2 * config.button_h), 
                         13, (self.mode_x_posi + 1.32 * config.button_h, self.first_row - 1.2 * config.button_h)]
        
        self.setting_dic = [11, self.right_corner,
                            3, (self.mode_x_posi, self.first_row),
                            8, (self.mode_x_posi, self.first_row - 1.2 * config.button_h),
                           10, (self.mode_x_posi + 1.32 * config.button_h, self.first_row - 1.2 * config.button_h)] 

        self.stat_dic = [Score(0, num_set, config) for i in range(5)]

        self.stat()

    def wiki(self, screen):
        known = 1
        if 10 < self.config.min_boss_hp < 20:
            known = 5
        elif self.config.min_boss_hp <= 10:
            known = 7
        for i in range(1,known):
            screen.blit(self.button_set[-1][i], 
            ((self.config.window_w - self.config.wiki_w)/2,
            0.15 * self.config.window_h + (i-1)*1.15*self.config.wiki_h))
        if known < 7:
            screen.blit(self.button_set[-1][0],
            ((self.config.window_w - self.config.wiki_w)/2,
            0.15 * self.config.window_h + (known-1)*1.15*self.config.wiki_h))

    def stat(self):
        self.stat_dic[1].set(self.config.hi_score)
        self.stat_dic[3].set(self.config.min_boss_hp)
        if self.read_stat:
            self.stat_dic[0].set(self.config.endless_play)
            self.stat_dic[2].set(self.config.story_play)
            self.stat_dic[4].set(self.config.victory_count)

    def setting(self, x, y, key):
        if key == K_RIGHT or( 0 < x - self.right_corner[0] < self.config.button_h and 
               0 < y - self.right_corner[1] < self.config.button_h):
            self.config.sound.click.play()
            if self.read_stat:
                self.read_stat = False
            elif self.read_wiki:
                self.read_wiki = False
            else:
                self.in_setting = False
        elif not (self.read_stat or self.read_wiki) and (
            key == K_s or ( 0 < x - self.setting_dic[3][0] < self.config.button_w and 
            0 < y - self.setting_dic[3][1] < self.config.button_h)):
            self.config.sound.click.play()
            self.read_stat = True
            self.stat()
        elif not (self.read_stat or self.read_wiki) and (
            key == K_m or ( 0 < x - self.setting_dic[5][0] < self.config.button_h and 
             0 < y - self.setting_dic[5][1] < self.config.button_h)):  
            self.config.sound.click.play()
            self.config.mute()
            self.setting_dic[4] = 15 - self.setting_dic[4]
        elif not (self.read_stat or self.read_wiki) and (
            key == K_w or ( 0 < x - self.setting_dic[7][0] < self.config.button_h and 
             0 < y - self.setting_dic[7][1] < self.config.button_h)):
            self.config.sound.click.play()
            self.read_wiki = True

    def check_button_tap(self,state, endless, pause, x, y, key):
        if state == 1 and key == K_SPACE:
            return 2, endless, pause
        elif state == 4:
            other_key = K_t if endless else K_p
            # menu
            if key == K_m or (0 < x - self.mode_x_posi < self.config.button_h 
                            and 0 < y - self.first_row < self.config.button_h):
                self.config.sound.click.play()
                return 0, endless, pause
            # restart
            elif key == K_r or (0 < x - self.mode_x_posi - 1.32 * self.config.button_h 
                < self.config.button_h and 0 < y - self.first_row < self.config.button_h):
                self.config.sound.click.play()
                return 1, endless, pause
            # other mode
            elif (not endless or (endless and self.boss_unlock == 0)) and(
                key == other_key or (0 < x - self.mode_x_posi < self.config.button_w and 
                 0 < y - self.first_row - 1.2 * self.config.button_h < self.config.button_h)):
                self.config.sound.click.play()
                return 1, not endless, pause
            else:
                return state, endless, pause
        elif state == 2:
            #menu
            if self.pause and (key == K_m or (0 < x - self.pause_dic[1][0] <
            self.config.button_h and 0 < y - self.pause_dic[1][1] < self.config.button_h)):
                    self.config.sound.click.play()
                    self.pause = False
                    return 0, endless, False
            #resume
            elif self.pause and ((key == K_SPACE and x == 0) or (x > 0 and 
                0 < x - self.pause_dic[3][0] < self.config.button_h and 
                 0 < y - self.pause_dic[3][1] < self.config.button_h)):
                    self.pause = False
                    return state, endless, False
            #restart
            elif self.pause and (key == K_r or (0 < x - self.pause_dic[5][0] 
            < self.config.button_h and 0 < y - self.pause_dic[5][1] < self.config.button_h)):
                self.config.sound.click.play()
                self.pause = False
                return 1, endless, False
            # pause
            elif not self.pause and ( key == K_p or (0 < x - self.right_corner[0] < self.config.button_h and 
               0 < y - self.right_corner[1] < self.config.button_h)):
                self.config.sound.click.play()
                self.pause = True
                return state, endless, True
            else:
                return state, endless, pause
        elif state == 0:
            #in_setting
            if self.in_setting:
                self.setting(x,y, key)
                return state, endless, pause 
            #setting
            elif key == K_s or 0 < x - self.right_corner[0] < self.config.button_h and (
               0 < y - self.right_corner[1] < self.config.button_h):
                self.config.sound.click.play()
                self.in_setting = True
                return state, endless, pause     
            # endless
            elif key == K_p or 0 < x - self.mode_x_posi < self.config.button_w and (
                 0 < y - self.first_row < self.config.button_h):
                self.config.sound.click.play()
                return 1, True, pause
            # story
            elif key == K_t or 0 < x - self.mode_x_posi < self.config.button_w and self.boss_unlock == 0 and (
                 0 < y - self.first_row - 1.2 * self.config.button_h < self.config.button_h):
                self.config.sound.click.play()
                return 1, False, pause
            else:
                return state, endless, pause
        else:
            return state, endless, pause

    def draw(self, screen, mode, endless):
        if endless:
            self.butt_dic[4][6] = self.boss_unlock
        else:
            self.butt_dic[4][6] = 2
        if self.pause:
            pygame.Surface.set_alpha(self.background, 100)
            screen.blit(self.background, (0,0))
            for i in range(0, len(self.pause_dic), 2):
                screen.blit(self.button_set[self.pause_dic[i]], self.pause_dic[i+1])
        elif self.in_setting:
            pygame.Surface.set_alpha(self.background, 255)
            screen.blit(self.background, (0,0))
            screen.blit(self.button_set[self.setting_dic[0]], self.setting_dic[1])
            if self.read_wiki:
                self.wiki(screen)
            elif self.read_stat:
                screen.blit(self.button_set[15], 
                ((self.config.window_w - self.config.statboard_w)/2,0.3*self.config.window_h))
                for i in range(5):
                    self.stat_dic[i].draw(self.config.window_w/2 + 0.4 * self.config.statboard_w, 
                    0.3 * self.config.window_h + 0.32 * self.config.statboard_h + i * 1.56 * self.config.num_h, screen)
            else:
                for i in range(2, len(self.setting_dic), 2):
                    screen.blit(self.button_set[self.setting_dic[i]], self.setting_dic[i+1])
        elif self.butt_dic.get(mode) != None:
            for index in range(0,len(self.butt_dic[mode]),2):
                screen.blit(self.button_set[self.butt_dic[mode][index]], self.butt_dic[mode][index+1])
            if mode == 4:
                self.boss_unlock = 0 if self.config.hi_score >= 30 else 1
                self.butt_dic[0][0] = self.boss_unlock
                self.stat_dic[1 if endless else 3].draw(0.5 * self.config.window_w 
                + 0.436 * self.config.gover_w, 0.58 * self.config.window_h - 0.55 * self.config.gover_h, screen)


