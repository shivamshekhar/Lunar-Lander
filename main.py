import os
import pygame
import sys
import time
import math
import random
from pygame.locals import *

pygame.init()

scr_size = (width, height) = (600, 400)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(scr_size)
FPS = 25
black = (0,0,0)
gravity = 0.3
air_resistance = 0.05

def load_image(
    name,
    sizex=-1,
    sizey=-1,
    colorkey=None,
    ):

    fullname = os.path.join('sprites', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))

    return (image, image.get_rect())


def load_sprite_sheet(
        sheetname,
        x = -1,
        y = -1,
        sizex = -1,
        sizey = -1,
        scalex = -1,
        scaley = -1,
        colorkey = None,
        ):
    fullname = os.path.join('sprites',sheetname)
    sheet = pygame.image.load(fullname)
    sheet = sheet.convert()

    if x!=-1 or y!=-1 or sizex!=-1 or sizey!=-1:
        rect = pygame.Rect((x,y,sizex,sizey))
        image = pygame.Surface(rect.size)
        image = image.convert()

    else:
        image = sheet

    image.blit(sheet,(0,0),rect)
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey,RLEACCEL)

    if scalex != -1 or scaley != -1:
        image = pygame.transform.scale(image,(scalex,scaley))

    return (image,image.get_rect())

class Lander(pygame.sprite.Sprite):
    def __init__(self,x,y):
        self.images = []
        for i in range(0,2400,400):
            self.image,self.rect = load_sprite_sheet('lander.png',i,0,400,400,width/10,width/10,-1)
            self.images.append(self.image)
        self.index = 0
        self.movement = [0,0]
        self.acceleration = [0,0]
        self.maxacceleration = [2,2]
        self.maxspeed = [4,5]
        self.rect.left = x
        self.rect.top = y

    def draw(self):
        screen.blit(self.images[self.index],self.rect)

    def checkbounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        #if self.rect.top < 0:
        #    self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height

    def update(self):
        if self.acceleration[0] > self.maxacceleration[0]:
            self.acceleration[0] = self.maxacceleration[0]
        elif self.acceleration[0] < -1*self.maxacceleration[0]:
            self.acceleration[0] = -1*self.maxacceleration[0]

        if self.acceleration[1] > self.maxacceleration[1]:
            self.acceleration[1] = self.maxacceleration[1]
        elif self.acceleration[1] < -1*self.maxacceleration[1]:
            self.acceleration[1] = -1*self.maxacceleration[1]

        if self.movement[0] < 0:
            self.movement[0] = self.movement[0] + self.acceleration[0] + air_resistance
        elif self.movement[0] > 0:
            self.movement[0] = self.movement[0] + self.acceleration[0] - air_resistance
        else:
            self.movement[0] = self.movement[0] + self.acceleration[0]

        self.movement[1] = self.movement[1] + self.acceleration[1] + gravity

        if self.movement[0] > self.maxspeed[0]:
            self.movement[0] = self.maxspeed[0]
        elif self.movement[0] < -1*self.maxspeed[0]:
            self.movement[0] = -1*self.maxspeed[0]

        if self.movement[1] > self.maxspeed[1]:
            self.movement[1] = self.maxspeed[1]
        elif self.movement[1] < -1*self.maxspeed[1]:
            self.movement[1] = -1*self.maxspeed[1]

        if self.acceleration[1] < 0and self.acceleration[0] == 0:
            self.index = 1
        elif self.acceleration[0] < 0 and self.acceleration[1] == 0:
            self.index = 2
        elif self.acceleration[0] > 0 and self.acceleration[1] == 0:
            self.index = 4
        elif self.acceleration[0] < 0 and self.acceleration[1] < 0:
            self.index = 3
        elif self.acceleration[0] > 0 and self.acceleration[1] < 0:
            self.index = 5
        else:
            self.index = 0

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

class Terrain(pygame.sprite.Sprite):
    def __init__(self,color):
        self.image = pygame.Surface((width,height))
        self.rect = self.image.get_rect()
        self.color = color
        self.colorkey = -1
        for i in range(0,width):
            r = random.randrange(height/4,height/4 + 10)
            point = pygame.Surface((1,r))
            point.fill(self.color)
            ptrect = point.get_rect()
            ptrect.left = i
            ptrect.bottom = height
            self.image.blit(point,ptrect)

        if self.colorkey is -1:
            self.colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(self.colorkey, RLEACCEL)

        self.image = self.image.convert_alpha()

    def draw(self):
        screen.blit(self.image,self.rect)

class LandingPad(pygame.sprite.Sprite):
    def __init__(self,multiplier):
        self.multiplier = multiplier



def main():
    gameOver = False

    lander = Lander(width/2,0)
    #lander2 = Lander(width/2,height/2)
    terrain = Terrain((255,255,255))

    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_DOWN:
                #    lander.acceleration[1] = 2
                if event.key == pygame.K_UP:
                    lander.acceleration[1] = lander.acceleration[1] + (-1) #-2
                if event.key == pygame.K_LEFT:
                    lander.acceleration[0] = lander.acceleration[0] + (-0.5) #-2
                if event.key == pygame.K_RIGHT:
                    lander.acceleration[0] = lander.acceleration[0] + (0.5) #2

            if event.type == pygame.KEYUP:
                #if event.key == pygame.K_DOWN:
                #    lander.acceleration[1] = 0
                if event.key == pygame.K_UP:
                    lander.acceleration[1] = 0
                if event.key == pygame.K_LEFT:
                    lander.acceleration[0] = 0
                if event.key == pygame.K_RIGHT:
                    lander.acceleration[0] = 0

        screen.fill(black)
        terrain.draw()

        print pygame.sprite.collide_mask(lander,terrain)

        lander.draw()
        #lander2.draw()

        lander.update()
        #lander2.update()

        pygame.display.update()

        clock.tick(FPS)
    pygame.quit()
    quit()

main()
