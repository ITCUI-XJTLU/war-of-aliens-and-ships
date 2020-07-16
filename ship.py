import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_setting,screen):
        super(Ship,self).__init__()
        self.screen=screen
        self.image=pygame.image.load('D:/program_learning/python/spaceshipe_game/image/ship.bmp')
        self.rect=self.image.get_rect()     #图像的矩形属性
        self.screen_rect=screen.get_rect()   #窗口矩形属性

        #飞船位置参数
        self.rect.centerx=self.screen_rect.centerx
        self.rect.bottom=self.screen_rect.bottom
        self.center=float(self.rect.centerx)        # 浮点化，进行后期运算

        self.moving_right=False         #实现持续移动
        self.moving_left=False

        self.ai_setting=ai_setting

    def blitme(self):        #显示飞船
        self.screen.blit(self.image,self.rect)

    def update(self): #更新位置参数
        #使用float类型的self.center进行计算
        if self.moving_right==True:
            if self.center < self.screen_rect.right:
                self.center +=self.ai_setting.ship_speed_factor

        if self.moving_left==True:
            if self.center>self.screen_rect.left:
                self.center -=self.ai_setting.ship_speed_factor
        self.rect.centerx=self.center  #只会保留self.center的整数部分

    def center_ship(self):
        self.center=self.screen_rect.centerx





