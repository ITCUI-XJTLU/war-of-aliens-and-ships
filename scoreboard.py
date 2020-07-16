import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    def __init__(self,ai_setting,screen,stats):
        self.screen=screen
        self.screen_rect=screen.get_rect()
        self.ai_setting=ai_setting
        self.stats=stats

        self.text_color=(30,30,30)
        self.font=pygame.font.SysFont(None,48)
        self.alien_points=50

        self.prep_score()      #实时分数的渲染函数
        self.prep_high_score()   #最高分数的渲染函数
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        round_score=int(round(self.stats.score,-1))
        score_str="{:,}".format(round_score)      # 不是很明白格式
        self.score_image=self.font.render(score_str,True,self.text_color,
                                          self.ai_setting.color)

        self.score_rect=self.score_image.get_rect()
        self.score_rect.right=self.screen_rect.right-20
        self.score_rect.top=20

    def prep_high_score(self):
        high_score=int(round(self.stats.high_score,-1))
        high_score_str="{:,}".format(high_score)
        high_textscore_str="Highest Score:"+str(high_score_str)
        self.high_score_imag=self.font.render(high_textscore_str,True,self.text_color,
                                              self.ai_setting.color)

        self.high_score_rect=self.high_score_imag.get_rect()
        self.high_score_rect.centerx=self.screen_rect.centerx
        self.high_score_rect.top=self.score_rect.top

    def prep_level(self):
        self.stats.text_level="Level: "+str(self.stats.level)
        self.level_image=self.font.render(str(self.stats.text_level),True,
                                          self.text_color,self.ai_setting.color)

        self.level_rect=self.level_image.get_rect()
        self.level_rect.right=self.score_rect.right
        self.level_rect.top=self.screen_rect.bottom-40


    def prep_ships(self):
        self.ships=Group()

        for ship_number in range(self.stats.ship_left):
            ship=Ship(self.ai_setting,self.screen)
            ship.rect.x=10+ship_number*ship.rect.width
            ship.rect.y=10
            self.ships.add(ship)


    def show_score(self):
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_imag,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.ships.draw(self.screen)








