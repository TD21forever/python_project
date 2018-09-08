import pygame
from plane_sprites import *

class PlaneGame(object):
    '''飞机主程序'''
    def __init__(self):
        print("游戏初始化")
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self._create_sprites()
        pygame.time.set_timer(CREATE_ENEMY_EVENT,1000)
        pygame.time.set_timer(HERO_FIRE_EVENT,500)


        #开始游戏
    def start_game(self):
        print("游戏开始")

        while True:
            self.clock.tick(FRAME_PER_SEC)
            self.__event_handler()
            self.__update_sprites()
            self.__check_collide()
            pygame.display.update()

    #监听事件
    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                self.enemy_1  = Enemy("./images/1.jpg")
                self.enemy_2  = Enemy("./images/2.jpg")
                self.enemy_3  = Enemy("./images/3.jpg")
                self.enemy_4  = Enemy("./images/4.jpg")
                self.enemy_5  = Enemy("./images/5.jpg")


                self.enemy_group.add(self.enemy_1,self.enemy_2,self.enemy_3,self.enemy_4,self.enemy_5)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT] ==  1:
            self.hero.speed =2
        elif key_pressed[pygame.K_LEFT] ==1:
            self.hero.speed = -2
        else:
            self.hero.speed =0
        if key_pressed[pygame.K_UP] ==1:
            self.hero.y_speed= -2
        elif key_pressed[pygame.K_DOWN] ==1:
                self.hero.y_speed = 2
        else :
            self.hero.y_speed = 0


    #创建精灵
    def _create_sprites(self):
        #创建背景精灵和背景精灵组
        self.bg_1 = BackGround()
        self.bg_2 = BackGround(True)
        self.bg_group = pygame.sprite.Group(self.bg_1,self.bg_2)
        #创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()
        #创建英雄精灵和精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    #碰撞检测
    def __check_collide(self):
        pygame.sprite.groupcollide(self.enemy_group,self.hero.bullets,True,True)
        enemy_list = pygame.sprite.spritecollide(self.hero,self.enemy_group,True)
        if len(enemy_list)>0:
            self.__game_over()

    #更新精灵组
    def __update_sprites(self):
        #更新背景
        self.bg_group.update()
        self.bg_group.draw(self.screen)
        #更新敌机
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        #更新英雄
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        #更新子弹
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)
    @staticmethod
    def __game_over():
        print("游戏结束")
        pygame.quit()
        exit()

if __name__ == '__main__':
    game = PlaneGame()
    game.start_game()
