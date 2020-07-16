import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self,ai_setting,screen,ship):
        super().__init__()   #初始化继承的类
        self.screen=screen

        #创建子弹在正确位置
        self.rect=pygame.Rect(0,0,ai_setting.bullet_width,ai_setting.bullet_height)
        self.rect.centerx=ship.rect.centerx
        self.rect.top=ship.rect.top

        #一些参数设置
        self.y=float(self.rect.y)  #为了计算y值变化，变成浮点数
        self.color=ai_setting.bullet_color
        self.speed_factor=ai_setting.bullet_speed_factor

    def update(self):
        self.y-=self.speed_factor
        self.rect.y=self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen,self.color,self.rect)


