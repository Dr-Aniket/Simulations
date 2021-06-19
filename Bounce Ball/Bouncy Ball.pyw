import colorama
import pygame
from color import color
from vector import vector
from pyfiglet import Figlet
from math import *
import os
import colorama
import winsound 
from time import time
colorama.init()
colour = colorama.Fore

#######################################################
font = 'banner3-d'
pg = pygame
colorama.init()
COLOR = colorama.Fore
txt = Figlet(font=font,width=500)
fullscreen = False
fullscreen = True
bgColor = color(-1)
fgColor = color(350)
radius = 10
showPath = True
ke = vector(0)
momentum = vector(0)
#######################################################

#######################################################
def Print(text,Color='',end='\n'):
    
    text = txt.renderText(text.title())
    print(Color+text+COLOR.RESET,end=end)
#######################################################

#######################################################
def newSpace(name='Space'):
    global dimx,dimy
    pygame.init()
    if fullscreen:
        space = pygame.display.set_mode((0,0),pg.FULLSCREEN)
    else:
        space = pygame.display.set_mode((500,500))
    dimx = pg.display.Info().current_w
    dimy = pg.display.Info().current_h
    pygame.display.set_caption(name.title())
    global clock
    clock = pygame.time.Clock()
    return space
#######################################################

#######################################################
space = newSpace()
gravity = vector(0,1)
resistanceFactor =  0.0001
damping = 0.05
#######################################################

#######################################################
def displayTxt(txt,x=dimx//2,y=20,c = fgColor):
    pg.draw.rect(space,bgColor,(0,y-20,dimx,30))
    font = pygame.font.Font('freesansbold.ttf', 20)
    txt = font.render(txt,True,c)
    textRect = txt.get_rect()
    textRect.center = (x,y)
    space.blit(txt,textRect)
#######################################################

#######################################################
class wall:
    def __init__(self,ip,fp):
        self.ipos = ip
        self.fpos = fp
        self.r = self.fpos-self.ipos
        self.theta = (self.fpos-self.ipos).theta()
        self.l = self.r.mag()
        self.color = color(350)
        self.thickness = 1
        self.mass = inf
        self.velocity = vector(0)

    def __repr__(self):
        return f'IPos : {self.ipos} | FPos : {self.fpos} | Color : {self.color} | Angle : {self.theta}' #str(self.r)
#######################################################

#######################################################
def click():
    frequency = 5000
    duration = 50
    winsound.Beep(frequency, duration)
#######################################################

#######################################################
def vel(o1,o2):
    m1 = o1.mass
    m2 = o2.mass
    v1 = o1.velocity
    v2 = o2.velocity
    x1 = o1.pos
    x2 = o2.pos
    
    try:
        return v1 - (x1-x2) * (2*m2/(m1+m2))*(((v1-v2)*(x1-x2))/(x1-x2).mag()**2)
    except:
        return v1
#######################################################

#######################################################
class ball:
    global showPath
    def __init__(self,*pos,vel = vector(2,2)):
        self.pos = vector(pos)
        self.radius = radius
        self.velocity = vel
        self.color = color(100 + 10000 * self.velocity.mag()*2/10000)
        self.collide = 0
        self.mass = self.radius*10
        self.path = []
        self.pathThicknes = 2
        self.pathColor = color(self.pos.mag() * time()%int(time()) + 100)
        self.dist = 0
        self.ke = 0
        self.momentum = 0

    def overlaps(self,other):
        seperation= self.pos | other.pos
        if  seperation <= self.radius + other.radius:
            return True
        return False
                

    def update(self):
        # self.radius = radius
        # self.mass = self.radius*10
        prePos = self.pos
        if self.pos[0] > dimx-self.radius:                    # Right Wall
            self.velocity[0] *= -1
            self.pos[0] = dimx - self.radius
            self.collide = 1
            
        if self.pos[0] < self.radius:                       # Left Wall
            self.velocity[0] *= -1
            self.pos[0] = self.radius
            self.collide = 1

        if self.pos[1] > dimy-self.radius:                    # Floor
            self.velocity[1] *= -1 
            self.pos[1] = dimy - self.radius
            self.collide = 1

        if self.pos[1] < top + self.radius:                       # Roof
            self.velocity[1] *= -1 
            self.pos[1] = top + self.radius
            self.collide = 1

        if self.collide:                                  # Collision Damping
            self.velocity *= (1 - damping)
            self.collide = 0

        airResistance = -(self.velocity.unit())* resistanceFactor
        acc = gravity + airResistance
        self.velocity +=  acc
        self.pos += self.velocity
        if self.radius>9 and showPath:
            for point in self.path[-100:]:
                pg.draw.rect(space,self.pathColor,(point[0],point[1],self.pathThicknes ,self.pathThicknes))
            self.path.append(self.pos)
        else:
            self.path = []

        self.dist += prePos | self.pos
        self.ke = ((self.velocity*self.velocity) * self.mass ) / 2
        self.momentum = self.velocity * self.mass
        
    def __eq__(self,other):
        if self.pos == other.pos and self.color == other.color and self.velocity == other.velocity:
            return True
        return False

    def __ne__(self,other):
        return not self.__eq__(other)

#######################################################

#######################################################
def bounce(o1:ball ,o2:ball ):
    theta = radians((o2.pos - o1.pos).theta() + 90)
    tangent = vector(round(cos(theta),34),round(sin(theta),3))
    alpha1 = o1.velocity.theta()
    alpha2 = o2.velocity.theta()

    v1 = vel(o1,o2)
    v2 = vel(o2,o1)

    o1.velocity = v1
    o2.velocity = v2

    click()

    return o1,o2
#######################################################

#######################################################
top = 60
stimulate = True
pause = -1
maxBalls = 100
speed = 1
balls=[]
distance = 0
walls=[wall(vector(0,top),vector(dimx,top)),
       wall(vector(dimx,top),vector(dimx,dimy)),
       wall(vector(dimx,dimy),vector(0,dimy)),
       wall(vector(0,dimy),vector(0,top))]
#######################################################

#######################################################
while stimulate:
    key = pygame.key.get_pressed()
    showTxt = ''
    for event in pygame.event.get():
        if event.type == pygame.QUIT or key[pygame.K_ESCAPE] or key[pygame.K_RETURN]:
            stimulate=False
            break
        
        if pause < 1:
            if event.type==pygame.KEYDOWN:
                if event.key == pg.K_DELETE:
                    del balls
                    balls = []
                    # os.system('cls')

            if  pg.mouse.get_pressed()[0]:
                x = pg.mouse.get_pos()[0]
                y = pg.mouse.get_pos()[1]
                finalPos = vector(x,y)
                for Ball in balls:
                    if Ball.pos|finalPos <= radius*2:
                        finalPos = 0
                        break
                if type(finalPos) == vector and len(balls)<maxBalls:
                    v = (finalPos-initialPos)
                    balls.append(ball(x,y,vel=v))
            initialPos = vector(pg.mouse.get_pos())
        
        if key[pg.K_p]:
            showPath = not showPath

        if key[pg.K_SPACE]:
            pause *= -1
        if key[pg.K_s]:
            showTxt += ' | Momentum Loss | '
            for b in balls:
                b.velocity *= 0
        if key[pg.K_g]:
            if gravity.mag() > 0:
                gravity *= 0
            else:
                gravity = vector(0,1)
        if key[pg.K_a]:
            if resistanceFactor > 0:
                resistanceFactor *= 0
            else:
                resistanceFactor = 0.0001
        if key[pg.K_d]:
            if damping > 0:
                damping = 0
            else:
                damping = 0.05
        if key[pg.K_KP_MULTIPLY]:
            # for Ball in balls:
            #     Ball.velocity *= 2
            speed *= 1.25
        if key[pg.K_KP_DIVIDE]:
            # for Ball in balls:
            #     Ball.velocity //= 2
            speed /= 1.25
    if key[pg.K_KP_PLUS]:
        radius += 1
    if key[pg.K_KP_MINUS]:
        radius -= 1
        if radius < 1:
            radius = 1

    if key[pg.K_UP]:
        maxBalls += 1
    if key[pg.K_DOWN]:
        maxBalls -= 1
        if maxBalls < 0:
            maxBalls = 0
        balls = balls[:maxBalls]

    if pause < 1:

        checked = []
        for b1 in balls:
            for b2 in balls:
                if b1 != b2 and b2 not in checked:
                    if b1.overlaps(b2):
                        b1,b2 = bounce(b1,b2)
            checked.append(b1)

        space.fill(bgColor)
        for Wall in walls:
            pg.draw.line(space,Wall.color,(Wall.ipos[0],Wall.ipos[1]),(Wall.fpos[0],Wall.fpos[1]),Wall.thickness*5)
        for Ball in balls:
            x = Ball.pos.v[0]
            y = Ball.pos.v[1]
            pg.draw.circle(space,Ball.color,(x,y),Ball.radius)
            Ball.update()
##            ke += Ball.ke
##            momentum += Ball.momentum
            if 30 < Ball.radius < 35:
                distance = Ball.dist
                distance *= 0.2645833333
                distance *= 0.001
                distance = round(distance,2)

##        if len(balls):
##            ke = ke//len(balls)
##            momentum = momentum//len(balls)
    else:
        showTxt += "Paused"
    showTxt += f' | Balls : {len(balls)}/{maxBalls} | Radius : {radius} | Speed : {speed} | Distance : {distance}m | Kinetic E. : {ke} | Momentum : {momentum} | ' 
    displayTxt(showTxt,c=fgColor)
    showTxt = f'| Gravity : {gravity.mag()>0} | AirResistance : {resistanceFactor>0} | Damping : {damping>0} | Path : {showPath} | '
    displayTxt(showTxt,y=50)
    pg.display.flip()
    clock.tick(60*speed)
#######################################################
