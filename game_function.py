import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_event(event,ai_setting,screen, ship,bullets):
    if event.key==pygame.K_RIGHT:   #左右移动
        ship.moving_right=True
    elif event.key==pygame.K_LEFT:
        ship.moving_left=True
    elif event.key==pygame.K_SPACE:   #空格键时，发子弹
       fire_bullet(ai_setting,screen,ship,bullets)
    elif event.key==pygame.K_q:
        sys.exit()

def check_keyup_event(event,ship):
    if event.key==pygame.K_RIGHT:
        ship.moving_right=False
    elif event.key==pygame.K_LEFT:
        ship.moving_left=False

#检查鼠标单击位置并重置参数
def check_play_button(ai_setting,screen,stats,sb,play_button,ship,
                      aliens,bullets,mouse_x,mouse_y):
    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        ai_setting.initialize_dynamic_setting()
        pygame.mouse.set_visible(False)          #隐藏光标

        stats.game_active=True
        stats.reset_stats()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_score()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_setting,screen,ship,aliens)
        ship.center_ship()


#检测输入，并调用上面两个函数  --做工程时，要秉持函数尽可能功能单一，多调用
def check_event(ai_setting,screen,stats,sb,play_button,ship,aliens,bullets):
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            check_keydown_event(event,ai_setting,screen,ship,bullets)
        elif event.type==pygame.KEYUP:
            check_keyup_event(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_setting,screen,stats,sb,play_button,ship,
                              aliens,bullets,mouse_x, mouse_y)


#更新屏幕
def upgrade_screen(ai_setting,screen,stats,sb,ship,aliens,bullets,play_button):
    screen.fill(ai_setting.color)
    for bullet in bullets:
        bullet.draw_bullet()
    ship.blitme()         #显示飞船
    aliens.draw(screen)
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()     #更新界面



#子弹部分函数调用
# #打出子弹
def fire_bullet(ai_setting,screen,ship,bullets):
    if len(bullets)<=ai_setting.bullets_allow:
        new_bullet=Bullet(ai_setting,screen,ship)
        bullets.add(new_bullet)

def update_bullets(ai_setting,screen,stats,sb,ship,aliens,bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom<=0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_setting,screen,stats,sb,ship,aliens,bullets)

#1.检查子弹和人是否碰撞   2.人被消灭完后，创建一组新的
def check_bullet_alien_collisions(ai_setting,screen,stats,sb,ship,aliens,bullets):
    collision=pygame.sprite.groupcollide(bullets,aliens,True,True)           #返回一个字典（人+子弹）

    if collision:        #判断是否为空
        for aliens in collision.values():
            stats.score+=ai_setting.alien_points
            sb.prep_score()
        check_high_score(stats,sb)

    if len(aliens)==0:
        bullets.empty()
        ai_setting.increase_speed()     #加速
        create_fleet(ai_setting,screen,ship,aliens)

        stats.level+=1       #更新level值
        sb.prep_level()

def check_high_score(stats,sb):
    if stats.score>stats.high_score:
        stats.high_score=stats.score
        sb.prep_high_score()



#外星人部分函数
def get_numer_aliens_x(ai_setting,alien_width):
    available_space_x=ai_setting.screen_width-2*alien_width
    number_alien_x=int(available_space_x/(2*alien_width))
    return number_alien_x

def get_number_rows(ai_setting, ship_height, alien_height):
    available_space_y=(ai_setting.screen_hight-(3*alien_height)-ship_height)
    number_rows=int(available_space_y/(2*alien_height))
    return number_rows

def create_alien(ai_setting,screen,aliens,alien_number,row_number):
    alien=Alien(ai_setting,screen)
    alien_width=alien.rect.width
    alien.x=alien_width+2*alien_width*alien_number            #  这一行创建横向的外星人，接受下面函数的for循环调用，结合下边才可以理解
    alien.rect.x=alien.x
    alien.rect.y=alien.rect.height+2*alien.rect.height*row_number     #同上
    aliens.add(alien)

def change_fleet_direction(ai_setting,aliens):
    for alien in aliens.sprites():
        alien.rect.y+=ai_setting.fleet_drop_speed
    ai_setting.fleet_direction*=-1

def check_fleet_edges(ai_setting,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_setting,aliens)
            break

def ship_hit(ai_setting,screen,stats,sb, ship,aliens,bullets):
    if  stats.ship_left>=0:
        stats.ship_left-=1

        sb.prep_ships()

        aliens.empty()       #清空现有的外星人和子弹
        bullets.empty()

        create_fleet(ai_setting,screen,ship,aliens)      #创建一群新的外星人
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active=False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_setting,screen,stats,sb,ship,aliens,bullets):    #检查外星人是否到底
    screen_rect=screen.get_rect()
    for alien in aliens:
        if alien.rect.bottom >=screen_rect.bottom:
            ship_hit(ai_setting,screen,stats,sb,ship,aliens,bullets)
            break

def update_aliens(ai_setting,screen,stats,sb,ship,aliens,bullets):
    check_fleet_edges(ai_setting,aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_setting,screen,stats,sb,ship,aliens,bullets)

    check_aliens_bottom(ai_setting,screen,stats,sb,ship,aliens,bullets)


def create_fleet(ai_setting,screen,ship,aliens):
    #获取参数
    alien=Alien(ai_setting,screen)
    number_aliens_x=get_numer_aliens_x(ai_setting,alien.rect.width)
    number_rows=get_number_rows(ai_setting,ship.rect.height,alien.rect.height)
    #向group里添加元素
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_setting,screen,aliens,alien_number,row_number)


        