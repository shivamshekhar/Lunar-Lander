import os
import random
import pygame
from pygame.locals import *

pygame.init()

scr_size = (width, height) = (900, 600)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(scr_size)
pygame.display.set_caption('Lunar Lander')

FPS = 25
black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)
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

def displaytext(
    text,
    fontsize,
    x,
    y,
    color,
    font = 'sawasdee'
    ):

    font = pygame.font.SysFont(font, fontsize, True)
    text = font.render(text, 1, color)
    textpos = text.get_rect(centerx=x, centery=y)
    screen.blit(text, textpos)

def displayfuelbar(fuel,maxfuel,x,y):
    if fuel <= maxfuel/2:
        r = 255
        g = 255*2*fuel/maxfuel
    else:
        g = 255
        r = 255*2 - 255*2*fuel/maxfuel

    color = [r,g,0]
    color = tuple(color)
    image = pygame.Surface(((fuel*width)/(2*maxfuel),height/40))
    image.fill(color)
    rect = image.get_rect()
    rect.left = x
    rect.top = y
    screen.blit(image,rect)

def displayvelocitybar(maxvelocity,limitvelocity,currentvelocity):
    barheight = height/60 * maxvelocity * 2
    barwidth = width/90
    image = pygame.Surface((barwidth,barheight))
    imagerect = image.get_rect()
    imagerect.left = width/90
    imagerect.top = height/60
    image.fill(white)

    limitzone = pygame.Surface((barwidth,height/60 * limitvelocity * 2))
    limitzone.fill(green)
    limitzonerect = limitzone.get_rect()
    limitzonerect.centery = barheight/2
    image.blit(limitzone,limitzonerect)

    currentvelocitybar = pygame.Surface((barwidth,2))
    currentvelocitybar.fill(red)
    currentvelocitybarrect = currentvelocitybar.get_rect()
    currentvelocitybarrect.centery = barheight/2 + currentvelocity*10
    image.blit(currentvelocitybar,currentvelocitybarrect)

    screen.blit(image,imagerect)



class Lander(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images = []
        for i in range(0,2400,400):
            self.image,self.rect = load_sprite_sheet('lander.png',i,0,400,400,width/16,width/16,-1)
            self.images.append(self.image)
        self.index = 0
        self.movement = [0,0]
        self.acceleration = [0,0]
        self.maxacceleration = [2,2]
        self.maxspeed = [width*4/600,height*5/400]
        self.rect.left = x
        self.rect.top = y
        self.fuel = 150
        self.maxfuel = 150
        self.engineOn = False
        self.isLanded = False
        self.score = 0

    def draw(self):
        screen.blit(self.images[self.index],self.rect)

    def checkbounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.top < -3*self.rect.height/2:
            self.kill()
            #self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height

    def update(self):
        if self.engineOn == True and self.fuel > 0:
            self.fuel -= 1

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

        if self.rect.bottom == height:
            self.movement[0] = 0

        self.image = self.images[self.index]
        self.rect = self.rect.move(self.movement)
        self.checkbounds()


class Explosion(pygame.sprite.Sprite):

    def __init__(self, x, y,radius=-1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        sheet = pygame.image.load('sprites/enemy_explode.png')
        self.images = []
        for i in range(0, 768, 48):
            rect = pygame.Rect((i, 0, 48, 48))
            image = pygame.Surface(rect.size)
            image = image.convert()
            colorkey = -1
            colorkey = image.get_at((10, 10))
            image.set_colorkey(colorkey, RLEACCEL)

            image.blit(sheet, (0, 0), rect)
            if radius != -1:
                image = pygame.transform.scale(image,(radius,radius))
            self.images.append(image)

        self.image = self.images[0]
        self.index = 0
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.image = self.images[self.index]
        self.index += 1
        if self.index >= len(self.images):
            self.kill()


class Terrain(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.scroll = 0
        self.scrollspeed = [3,3]
        self.rightedge = width
        self.bottomedge = height
        self.fullterrain,self.fullterrainrect = load_image('terrain1 (1).png',int(width),int(height),-1)
        self.fullterrainrect.left = 0
        self.fullterrainrect.top = 0
        self.fullterrainrect.width = width
        self.fullterrainrect.height = height
        self.image = pygame.Surface((width,height))
        self.rect = pygame.Rect((0, 0, width, height))

        self.image.blit(self.fullterrain,self.rect,self.fullterrainrect)
        colorkey = self.image.get_at((0,0))
        self.image.set_colorkey(colorkey,RLEACCEL)
        self.image = self.image.convert_alpha()

    def update(self):
        if self.scroll == 1 and self.rightedge <= 2*width - self.scrollspeed[0]:
            self.rightedge += self.scrollspeed[0]
            self.fullterrainrect.left += self.scrollspeed[0]

        elif self.scroll == -1 and self.rightedge >= width + self.scrollspeed[0]:
            self.rightedge -= self.scrollspeed[0]
            self.fullterrainrect.left -= self.scrollspeed[0]

        elif self.scroll == 2 and self.bottomedge <= int(1.5*height) - self.scrollspeed[1]:
            self.bottomedge += self.scrollspeed[1]
            self.fullterrainrect.top += self.scrollspeed[1]

        elif self.scroll == -2 and self.bottomedge >= height + self.scrollspeed[1]:
            self.bottomedge -= self.scrollspeed[1]
            self.fullterrainrect.top -= self.scrollspeed[1]

        self.image = pygame.Surface((width,height))
        self.rect = pygame.Rect((0, 0, width, height))
        self.image.blit(self.fullterrain,self.rect,self.fullterrainrect)
        colorkey = self.image.get_at((0,0))
        self.image.set_colorkey(colorkey,RLEACCEL)
        self.image = self.image.convert_alpha()

    def draw(self):
        screen.blit(self.image,self.rect)


class LandingPad(pygame.sprite.Sprite):
    def __init__(self,x,y,sizex,sizey,score_multiplier):
        pygame.sprite.Sprite.__init__(self)
        self.score_multiplier = score_multiplier
        self.image,self.rect = load_image('mul' + str(score_multiplier) + '.png',sizex,sizey)
        self.rect.left = x
        self.rect.top = y

    def draw(self):
        screen.blit(self.image,self.rect)


def main():
    gameOver = False
    gameStart = False
    menuDisplay = True
    gameEnd = False

    explosions = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()

    Explosion.containers = explosions,all
    Lander.containers = all

    introimg,introimgrect = load_image('Intro.png',-1,-1,-1)
    introlanderbot = Lander(width/3,0)

    terrain = Terrain()

    while not gameEnd:
        while menuDisplay:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    gameStart = True
                    menuDisplay = False
                    lander = Lander(width / 2, 0)
                    landingpadx2 = LandingPad(int(0.08 * width), int(0.52 * height), width / 13, height / 40, 2)
                    landingpadx5 = LandingPad(int(0.69 * width), int(0.93 * height), width / 9, height / 35, 5)
                    landingpadx10 = LandingPad(int(0.108 * width), int(0.966 * height), width / 12, height / 35, 10)
                    introlanderbot.kill()

            screen.fill(black)
            screen.blit(introimg,introimgrect)
            introlanderbot.draw()

            displaytext('Lunar Lander',width/9,width/2,height/3,white)
            displaytext('Press any key to continue....', width / 45, width / 2, height / 2, white)
            displaytext('Written by : Shivam Shekhar', width/45,width/6,height - height/50,black)

            rnd = random.randrange(0,5)

            if rnd == 0:
                introlanderbot.acceleration[1] = introlanderbot.acceleration[1] + (-1)  # -2
            else:
                introlanderbot.acceleration = [0,0]

            if introlanderbot.rect.left < width/5:
                introlanderbot.acceleration[0] = introlanderbot.acceleration[0] + 0.5
            elif introlanderbot.rect.right > width - width/5:
                introlanderbot.acceleration[0] = introlanderbot.acceleration[0] - 0.5
            else:
                if introlanderbot.movement[0] > 0:
                    introlanderbot.acceleration[0] = introlanderbot.acceleration[0] + 0.5
                else:
                    introlanderbot.acceleration[0] = introlanderbot.acceleration[0] - 0.5

            if introlanderbot.rect.top < 0:
                introlanderbot.rect.top = 0

            if introlanderbot.rect.bottom > height/2:
                introlanderbot.acceleration[1] = introlanderbot.acceleration[1] - 1

            introlanderbot.update()
            pygame.display.update()

            clock.tick(FPS)

        while gameStart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and lander.fuel > 0:
                    lander.engineOn = True
                    if event.key == pygame.K_UP:
                        lander.acceleration[1] = lander.acceleration[1] + (-1) #-2
                    if event.key == pygame.K_LEFT:
                        lander.acceleration[0] = lander.acceleration[0] + (0.5) #-2
                    if event.key == pygame.K_RIGHT:
                        lander.acceleration[0] = lander.acceleration[0] + (-0.5) #2

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        lander.acceleration[1] = 0
                    if event.key == pygame.K_LEFT:
                        lander.acceleration[0] = 0
                    if event.key == pygame.K_RIGHT:
                        lander.acceleration[0] = 0

            if lander.acceleration[0] == 0 and lander.acceleration[1] == 0:
                lander.engineOn = False

            if lander.fuel == 0:
                lander.acceleration = [0,0]

            """
            #uncomment this part to enable scrolling of the image/terrain
            if lander.movement[0] > 1 and lander.rect.left > width*9/10:
                terrain.scroll = 1
            elif lander.movement[0] < -1 and lander.rect.left < width*1/10:
                terrain.scroll = -1
            else:
                terrain.scroll = 0

            elif lander.movement[1] > 1 and lander.rect.top > height*7/10:
                terrain.scroll = 2
            elif lander.movement[1] < -1 and lander.rect.top < height*3/10:
                terrain.scroll = -2"""

            screen.fill(black)
            terrain.draw()
            landingpadx2.draw()
            landingpadx5.draw()
            landingpadx10.draw()
            displayfuelbar(lander.fuel,lander.maxfuel,width*2/5,height/30)
            displayvelocitybar(lander.maxspeed[1],int(4*lander.maxspeed[1]/7),lander.movement[1])

            all.draw(screen)


            if pygame.sprite.collide_rect(lander,landingpadx2) and \
            lander.rect.left >= landingpadx2.rect.left - landingpadx2.rect.width/5 and \
            lander.rect.right <= landingpadx2.rect.right + landingpadx2.rect.width/5 and \
            lander.movement[1] < 4*lander.maxspeed[1]/7:
                lander.movement=[0,0]
                lander.isLanded = True
                lander.score = lander.fuel * landingpadx2.score_multiplier

            if pygame.sprite.collide_rect(lander,landingpadx5) and \
            lander.rect.left >= landingpadx5.rect.left - landingpadx5.rect.width/5 and \
            lander.rect.right <= landingpadx5.rect.right + landingpadx5.rect.width/5 and \
            lander.movement[1] < 4*lander.maxspeed[1]/7:
                lander.movement=[0,0]
                lander.isLanded = True
                lander.score = lander.fuel * landingpadx5.score_multiplier

            if pygame.sprite.collide_rect(lander,landingpadx10) and \
            lander.rect.left >= landingpadx10.rect.left - landingpadx10.rect.width/5 and \
            lander.rect.right <= landingpadx10.rect.right + landingpadx10.rect.width/5 and \
            lander.movement[1] < 4*lander.maxspeed[1]/7:
                lander.movement=[0,0]
                lander.isLanded = True
                lander.score = lander.fuel * landingpadx10.score_multiplier


            if pygame.sprite.collide_mask(lander,terrain) and lander.alive():
                (x,y) = lander.rect.center
                Explosion(x,y,lander.rect.width)
                lander.kill()


            if lander.alive() == False and len(explosions) == 0:
                gameEnd = True
                gameStart = False


            all.update()
            terrain.update()

            pygame.display.update()

            #print (lander.fuel, lander.isLanded, lander.movement[1])
            clock.tick(FPS)

        while gameOver:
            pass

    pygame.quit()
    quit()

main()
