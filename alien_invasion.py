import pygame
import sys
from setting import Setting
from ship import Ship
import game_function as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import Gamestats
from button import Button
from scoreboard import Scoreboard


def run_game():
#初始化
    pygame.init()
    ai_setting=Setting()
    screen=pygame.display.set_mode((ai_setting.screen_width,ai_setting.screen_hight))   #创建窗口
    ship=Ship(ai_setting,screen)       #实例化飞船

    stats=Gamestats(ai_setting)     #统计信息
    sb=Scoreboard(ai_setting,screen,stats)     #scoreboard记分牌

    bullets=Group()    #创建子弹的一个列表
    aliens=Group()     #同上

    gf.create_fleet(ai_setting,screen,ship,aliens)

    play_button=Button(ai_setting,screen,"Play")
# 检测操作->game_function
    while True:
        gf.check_event(ai_setting,screen,stats,sb,play_button,ship,aliens,bullets)
        if  stats.game_active:
            ship.update()
            gf.update_bullets(ai_setting,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_setting,screen,stats,sb,ship,aliens,bullets)

        gf.upgrade_screen(ai_setting,screen,stats,sb,ship,aliens,bullets,
                          play_button)     #更新屏幕函数




run_game()

