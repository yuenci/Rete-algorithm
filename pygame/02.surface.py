'''
Author: Innis
Description: 
Date: 2022-03-31 15:17:38
LastEditTime: 2022-03-31 18:14:12
FilePath: \0328P-rete\pygame\02.surface.py
'''
#Surface=pygame.Surface(size=(width,height),flags,depth)


import sys
from time import time
import pygame

#使用pygame之前必须初始化
pygame.init()

#设置主屏窗口 ；设置全屏格式：flags=pygame.FULLSCREEN
screen = pygame.display.set_mode((800,600))

#设置窗口标题
pygame.display.set_caption('c语言中文网')
screen.fill('white')

#创建一个 50*50 的图像,并优化显示
face = pygame.Surface((50,50),flags=pygame.HWSURFACE)
#填充颜色
face.fill(color='pink')
#http://c.biancheng.net/pygame/surface.html

#创建一个圆形
radius =50
x,y = 300,300
pygame.draw.circle(screen, (255,0,0), (x,y), radius, width = 1)
pygame.draw.circle(screen,[255,0,0],[100,100],30,0)
#https://blog.csdn.net/weixin_41810846/article/details/112071924

#画一条线
pygame.draw.aaline(screen, (0, 0, 255), (100, 200), (340, 250), 1)
#https://blog.csdn.net/FourLeafCloverLLLS/article/details/78480857

def circle():
    for i in range(10):
        print(i)
        radius =50
        y = 300
        x = i * 20 + 300
        pygame.draw.circle(screen, (255,0,0), (x,y), radius, width = 1)
        time.sleep(1)

while True:
    # 循环获取事件，监听事件
    for event in pygame.event.get():
        # 判断用户是否点了关闭按钮
        if event.type == pygame.QUIT:
            #卸载所有模块
            pygame.quit()
            #终止程序
            sys.exit()
    # 将绘制的图像添加到主屏幕上，(100,100)是位置坐标，显示屏的左上角为坐标系的(0,0)原点
    screen.blit(face, (100, 100))
    pygame.display.flip() #更新屏幕内容