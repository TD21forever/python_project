import random
import pygame
#屏幕窗口常量
SCREEN_RECT = pygame.Rect(0,0,480,700)
#FPS
FRAME_PER_SEC = 60
#定义两个事件
CREATE_ENEMY_EVENT=pygame.USEREVENT
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):
    ''' 游戏精灵类'''
    def __init__(self,image_name,speed=1,y_speed=None):
        # 如果父不是object 一定要调用父类的初始化方法
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.y_speed = y_speed
        #更新父类的方法 update
    def update(self):
        self.rect.y += self.speed
class BackGround(GameSprite):
    '''背景精灵'''
    def __init__(self,is_alt = False):
        super().__init__("./images/background.png")
        if is_alt:
            self.rect.y = -self.rect.height
    def update(self):
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height

class Enemy(GameSprite):
    def __init__(self,name):
        super().__init__(name)
        self.rect.bottom = 0
        self.max_x = SCREEN_RECT.width-self.rect.width
        self.rect.x = random.randint(0,self.max_x)

        self.speed = random.randint(2,5)
    def update(self):
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            print("飞机飞出屏幕请及时从精灵组删除")
            #从精灵组中消除
            self.kill()
    def __del__(self):
        print("敌机挂了%s"%self.rect)

class Hero(GameSprite):
    def __init__(self):
        super().__init__("./images/6.jpg",speed=0)
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom-120
        self.bullets = pygame.sprite.Group()
    def update(self):
        self.rect.x += self.speed
        self.rect.y += self.y_speed
        if self.rect.left <=SCREEN_RECT.left :
            self.rect.x =0
        elif self.rect.right >= SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
        if self.rect.top <= SCREEN_RECT.top:
            self.rect.top =0
        elif self.rect.bottom >= SCREEN_RECT.bottom:
            self.rect.bottom = SCREEN_RECT.bottom
    def fire(self):
        for i in (0,1,2):

            self.bullet = Bullet()
            self.bullet.rect.y = self.rect.y - i*20
            self.bullet.rect.centerx = self.rect.centerx
            self.bullets.add(self.bullet)

class Bullet(GameSprite):
    def __init__(self):
        super().__init__("./images/bullet2.png",-2)
    def update(self):
        super().update()
        if self.rect.bottom <0:
            self.kill()




