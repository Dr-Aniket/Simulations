import pygame
pg = pygame
import pygame.display as display
import pygame.draw as draw
from color import color
from math import *

################################################################################
fullscreen = False
fullscreen = True
bgColor = color(0)
fgColor = color(350)
################################################################################

def newWindow(name="Space"):
    global dimx, dimy, stimulate
    pg.init()
    if fullscreen:
        space = display.set_mode((0,0),pg.FULLSCREEN)
    else:
        space = display.set_mode((500,500),pygame.SRCALPHA)
    dimx,dimy = display.get_window_size()
    display.set_caption(name)
    stimulate = True
    return space
space = newWindow()    
################################################################################
Clock = pg.time.Clock()
x = dimx//2
y = dimy//2
pathAngle = 0
paths = []
radius = min(dimx,dimy)*0.48
################################################################################
radiusVal = lambda a,b,t: (a * b) / ( (a * sin(t))**2 + (b * cos(t))**2 )**0.5
################################################################################
class Ellipse:
    def __init__(self, Color, x,y, angle):
        self.radius = radius
        self.a = self.radius
        self.b = self.a//3
        self.theta = radians(angle)
        self.border = 1
        self.color = Color
        self.x = x
        self.y = y
        self.points = []
        for t in range(0,360*5):
            t = radians(t/5)
            x = self.x + self.radius * cos(t+self.theta)
            y = self.y - self.radius * sin(t+self.theta)
            self.points.append((x,y))
            self.radius = radiusVal(self.a,self.b,t)
            t = degrees(t)

    def draw(self):
        draw.polygon(space,self.color,self.points,self.border)    
        
    def __eq__(self,other):
        if round(tan(self.theta),2) == round(tan(other.theta),2) and self.a == other.a and self.b == other.b:
            return True
        return False
    
    def __del__(self):
        pass
        # self.color = color(100+len(paths))
        # paths.append(Ellipse(self.color,self.x,self.y,self.theta))
################################################################################

################################################################################
def displayTxt(txt,x=dimx//2,y=20,c = fgColor):
    # pg.draw.rect(space,bgColor,(0,y-20,dimx,30))
    draw.circle(space,bgColor,(x,y),radius//3.1)
    font = pygame.font.Font('freesansbold.ttf', 20)
    txt = font.render(txt,True,c)
    textRect = txt.get_rect()
    textRect.center = (x,y)
    space.blit(txt,textRect)
################################################################################

################################################################################
class Point:
    def __init__(self,space,theta) -> None:
        self.space = space
        self.theta = theta
        self.alpha = 0
        self.a = radius
        self.b = self.a / 3
        self.radius = radiusVal(self.a,self.b,self.alpha)
        self.color = color(100 + self.theta)
        self.size = 5

    def update(self):
        x = self.x + self.radius * cos(self.alpha + self.theta)
        y = self.y - self.radius * sin(self.alpha + self.theta)

        draw.circle(self.space,self.color,(x,y),self.size)

        self.radius = radiusVal(self.a,self.b,self.alpha)
        self.alpha += (180/pi)
################################################################################

################################################################################
theta = 0
i = dimx//2
j = dimy//2
################################################################################

################################################################################
while stimulate:
    key = pygame.key.get_pressed()

    for event in pg.event.get():
        if event.type == pg.QUIT or key[pg.K_RETURN] or key[pg.K_ESCAPE]:
            stimulate = False
            break
        
        if key[pg.K_DELETE]:
            del paths
            space.fill(bgColor)
            theta = 0
            paths = []

    # if key[pg.K_SPACE] :
    newEllipse = Ellipse(fgColor,i,j,theta)
    
    if newEllipse not in paths and len(paths) < 200:
        paths.append(newEllipse)
    else:
        del newEllipse
    theta += 35
    if theta > 180:
        theta += 183

    for path in paths:
        path.draw()

    txt = f'Rings : {len(paths)}'
    displayTxt(txt,dimx//2,dimy//2)
    display.flip()

    Clock.tick(60*1)
    
