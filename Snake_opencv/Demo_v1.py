# -*- coding:utf-8 -*-

import pygame, sys, random
from pygame.locals import *
import cv2 as cv
import numpy as np
import imutils


pygame.init()
DIFFICULT = 9
ScreenX = 500
ScreenY = 500
ScreenSize = (ScreenX, ScreenY)
Screen = pygame.display.set_mode(ScreenSize, 0, 32)
#创建了一个窗口，set_mode会返回一个Surface对象，代表了在桌面上出现的那个窗口，三个参数第一个为元祖，代表分 辨率（必须）；第二个是一个标志位，如果不用什么特性，就指定0；第三个为色深。当我们把第二个参数设置为FULLSCREEN时，就能得到一个全屏窗口了
pygame.display.set_caption("Snake Game")#设置窗口的标题

# # 背景音乐

# pygame.mixer.music.load('BackgroundMusic.flac')
# pygame.mixer.music.play(-1, 0.0)
# EatFoodMusic = pygame.mixer.Sound('EatFoodMusic.wav')
# ClickMusic = pygame.mixer.Sound('ClickMusic.wav')

# 蛇
class snake():
    def __init__(self):
        self.Direction = None
        self.Body = []
        self.AddBody()
        # self.AddBody()

    def AddBody(self):
        NewAddLeft, NewAddTop = (0, 0)
        if self.Body:
            NewAddLeft, NewAddTop = (self.Body[0].left, self.Body[0].top)
        NewAddBody = pygame.Rect(NewAddLeft, NewAddTop, 20, 20)
        if self.Direction == K_LEFT:
            if NewAddBody.left <= 0:
                NewAddBody.left = 480
            else:
                NewAddBody.left -= 20
        elif self.Direction == K_RIGHT:
            if NewAddBody.left >= 480:
                NewAddBody.left = 0
            else:
                NewAddBody.left += 20
        elif self.Direction == K_UP:
            if NewAddBody.top <= 0:
                NewAddBody.top = 480
            else:
                NewAddBody.top -= 20
        elif self.Direction == K_DOWN:
            if NewAddBody.top >= 480:
                NewAddBody.top = 0
            else:
                NewAddBody.top += 20
        self.Body.insert(0, NewAddBody)

    def DelBody(self):
        self.Body.pop()

    def IsDie(self):
        if self.Body[0] in self.Body[1:]:
            return True
        return False

    def Move(self):
        self.AddBody()
        self.DelBody()

    def ChangeDirection(self, Curkey):
        LR = [pygame.K_LEFT, pygame.K_RIGHT]
        UD = [pygame.K_UP, pygame.K_DOWN]
        if Curkey in LR + UD:
            if (Curkey in LR) and (self.Direction in LR):
                return
            if (Curkey in UD) and (self.Direction in UD):
                return
            self.Direction = Curkey
    def GetX(self):
        return self.Body[0][0]

    def GetY(self):
        return self.Body[0][1]


# 食物
class food():
    def __init__(self):
        self.Obj = pygame.Rect(-20, 0, 20, 20)

    def Remove(self):
        self.Obj.x = -20

    def SendFood(self):
        if self.Obj.x == -20:
            AllPos = []
            for pos in range(20, ScreenX - 20, 20):
                AllPos.append(pos)
            self.Obj.left = random.choice(AllPos)
            self.Obj.top = random.choice(AllPos)

# 难度选择及游戏
def GameMain():
    FPSClock = pygame.time.Clock()
    Score = 0
    Snake = snake()
    Food = food()

    BackgroungImg = pygame.image.load('BackgroundImg.png').convert()

    ScoreFont = pygame.font.SysFont('arial', 30)

    cap = cv.VideoCapture(0)
    lis_x=[0,0,0,0,0,0,0,0,0,0]
    lis_y=[0,0,0,0,0,0,0,0,0,0]
    while True:     # main game loop
        if lis_x[-1] - lis_x[-5] > 40:
            Snake.ChangeDirection(K_RIGHT)
        elif lis_y[-1] - lis_y[-5] > 40:
            Snake.ChangeDirection(K_DOWN)
        elif lis_x[-1] - lis_x[-5] < -40:
            Snake.ChangeDirection(K_LEFT)
        elif lis_y[-1] - lis_y[-5] < -40:
            Snake.ChangeDirection(K_UP)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                Snake.ChangeDirection(event.key)

        Screen.blit(BackgroungImg, (0, 0))
        pygame.draw.rect(Screen, (0, 0, 0), Food.Obj, 0)
        Snake.Move()

        for rect in Snake.Body:
            pygame.draw.rect(Screen, (0, 0, 0), rect, 0)

        if Snake.IsDie():
            return Score

        if Food.Obj == Snake.Body[0]:
            Score += 1
            Food.Remove()
            Snake.AddBody()

        Food.SendFood()

        ScoreSurface = ScoreFont.render(str(Score), True, (0, 0, 0))
        Screen.blit(ScoreSurface, (0, 0))

        pygame.draw.rect(Screen, (0, 0, 0), Food.Obj, 0)

        pygame.display.update()
        FPSClock.tick(DIFFICULT) #FPS
        # 读取每一帧
        _, frame = cap.read()
        # 重设图片尺寸以提高计算速度
        frame = imutils.resize(frame, width=500,height=500)
        frame = cv.flip(frame,1,dst=None)
        # 进行高斯模糊
        blurred = cv.GaussianBlur(frame, (11, 11), 0)
        # 转换颜色空间到HSV
        hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)
        # 定义红色无图的HSV阈值
        lower_red = np.array([20, 100, 100])
        upper_red = np.array([220, 255, 255])
        # 对图片进行二值化处理
        mask = cv.inRange(hsv, lower_red, upper_red)
        # 腐蚀操作
        mask = cv.erode(mask, None, iterations=2)
        # 膨胀操作，先腐蚀后膨胀以滤除噪声
        mask = cv.dilate(mask, None, iterations=2)

        cv.imshow('mask', mask)

        # 寻找图中轮廓
        cnts = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]
        center = (0,0)
        # 如果存在至少一个轮廓则进行如下操作
        if len(cnts) > 0:
            # 找到面积最大的轮廓
            c = max(cnts, key=cv.contourArea)
            # 使用最小外接圆圈出面积最大的轮廓
            ((x, y), radius) = cv.minEnclosingCircle(c)
            # 计算轮廓的矩
            M = cv.moments(c)
            # 计算轮廓的重心
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # 只处理尺寸足够大的轮廓
            if radius > 10:
	            # 画出最小外接圆
	            cv.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), -1)
	            # 画出重心
	            cv.circle(frame, center, 5, (0, 0, 255), -1)

        cv.imshow('frame', frame)
        x,y = center
        lis_x.append(x)
        lis_y.append(y)
  

        k = cv.waitKey(5) & 0xFF
        if k == 27:
            break
    cap.release()
    cv.destroyAllWindows()

# 游戏结果
def GameResult(Score):

    GameResultBackgroundImg = pygame.image.load('GRBgImg.png').convert()
    ScoreHintFont = pygame.font.SysFont('arial', 35)
    ScoreFont = pygame.font.SysFont('arial', 180)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return True

        Screen.blit(GameResultBackgroundImg, (0, 0))
        ChoiceHintSurface = ScoreHintFont.render('Your Score is:', True, (0, 0, 0))
        Screen.blit(ChoiceHintSurface, (40, 110))
        ChoiceSurface = ScoreFont.render(str(Score), True, (0, 0, 0))
        Screen.blit(ChoiceSurface, (150, 150))
        EntranceHintSurface = ScoreHintFont.render('Press Space to restart the game', True, (0, 0, 0))
        Screen.blit(EntranceHintSurface, (50, 350))
        pygame.display.update()

if __name__ == '__main__':
    flag = True
    while flag:
        Score = GameMain()
        flag = GameResult(Score)