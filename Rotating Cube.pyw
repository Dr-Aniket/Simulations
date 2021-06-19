########################### IMPORTS ###########################
import pygame
pg = pygame
import pygame.display as display
import pygame.draw as draw
from vector import vector
from matrix import *
from color import color
from itertools import  combinations as combi
from math import radians, cos, sin
#############################################################################################################

############################ INIT #############################
fullscreen = True 
# fullscreen = False
vec = vector
mat = matrix
clock = pg.time.Clock()
fps = 60
speed = 1
bgColor = color(0)
fgColor = color(350)
dimx = 500
dimy = 500
simulate = False
rmx = lambda theta: matrix(1,0,0,0,cos(theta),-sin(theta),0,sin(theta),cos(theta),r=3)
rmy = lambda theta: matrix(cos(theta),0,-sin(theta),0,1,0,sin(theta),0,cos(theta),r=3)
rmz = lambda theta: matrix(cos(theta),-sin(theta),0,sin(theta),cos(theta),0,0,0,1,r=3)
#############################################################################################################

############################# BG ##############################
def newSpace(name = 'CUBE'):
    global dimx, dimy, simulate
    pg.init()
    if fullscreen:
        space = display.set_mode((0,0),pg.FULLSCREEN)
        dimx, dimy = display.get_window_size()
    else:
        space = display.set_mode((dimx,dimy))
        display.set_caption(name)
    
    return space, True
#############################################################################################################

############################# BG ##############################
def fillBg(space):
    space.fill(bgColor)
    # draw.circle(space,color(350),(dimx//2,dimy//2),1)  # Center
    # for i in range((dimx+dimy) //100):
    #     x = randint(0,dimx)
    #     y = randint(0,dimy)
    #     radius = 1 #randint(1,2)
    #     draw.circle( space, color(i*time.time())+(10,), (x, y) , radius )
#############################################################################################################

############################ CUBE #############################
class cube:
    def __init__(self,space = False,center = (0,0),size = 100, dim = 3) -> None:
        self.space = space
        self.size = size
        self.center = vec(center)
        self.vertxes = []
        self.pointStroke = size//15
        self.lineStroke = int(1 + size//40)
        self.theta = 0
        self.color = (100 + self.theta)
        self.sides = 4
        self.corners = 0
        self.dim = dim
        self.clockwise = True
        self.init()

    def init(self):
        pts = [1,-1]
        def func(lst):
            pass
        for z in pts:
            for y in pts:
                for x in pts:
                    self.setPoint(x,y,z)
                    
        self.corners = 2** self.dim

    def setPoint(self,*point):
        point = vec(point) * self.size
        self.vertxes.append(point)

    def update(self,axis = [0,1],colour = False):
        self.theta = radians(1)
        if not self.clockwise:
            self.theta *= -1
        if not colour:
            self.color += 1
        else:
            self.color = colour
        
        newPoints = []
        for vertex in self.vertxes:
            if 0 in axis:
                vertex = vertex.vecMatMul(rmx(self.theta))
            if 1 in axis:
                vertex = vertex.vecMatMul(rmy(self.theta))
            if 2 in axis:
                vertex = vertex.vecMatMul(rmz(self.theta))
            newPoints.append(vertex)
        self.vertxes = newPoints

    def showPoints(self):
        for point in self.vertxes:
            point += self.center
            draw.circle(self.space,color(self.color),(point.x,point.y),self.pointStroke)
    
    def showPoint(self,point):
        point += self.center
        draw.circle(self.space,color(self.color),(point.x,point.y),self.pointStroke)
        
    def showLine(self,p1,p2):
        p1 += self.center
        p2 += self.center
        draw.line(self.space,color(self.color),(p1.x,p1.y),(p2.x,p2.y),self.lineStroke)
    
    def show(self):
        self.showPoint(self.vertxes[0])
        for i,j in combi(range(self.corners),2):
            self.showPoint(self.vertxes[j])
            Draw = (i + 1 == j and j % 2 != 0) or (i + 2 == j and j % self.sides != 0 and (j-1) % self.sides != 0 ) or (i +4 == j)
            # Draw = True
            if Draw :
                self.showLine(self.vertxes[i],self.vertxes[j])
#############################################################################################################

############################ MAIN #############################
def main():
    space, simulate = newSpace()
    cubes = []
    size = (dimy/3**0.5)//2 - 10
    colour = 0
    while simulate:
        key = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT or key[pg.K_RETURN] or key[pg.K_ESCAPE]:
                simulate = False
                break
            if pg.mouse.get_pressed()[0]:
                center = pg.mouse.get_pos()
                cubes.append(cube(space,center,size))
            if key[pg.K_BACKSPACE]:
                cubes = cubes[:-1]
            if key[pg.K_DELETE]:
                del cubes
                cubes = []
            if key[pg.K_LSHIFT]:
                cubes[-1].clockwise = False
            elif key[pg.K_RSHIFT]:
                cubes[-1].clockwise = True

        if key[pg.K_UP]:
            size += 1
            Max = dimy//3**0.5
            if size > Max:
                size = Max
        elif key[pg.K_DOWN]:
            size -= 1
            if size < 2:
                size = 2
    
        fillBg(space)
        for Cube in cubes:
            Cube.update(axis = [1,2])
            Cube.show()

        display.flip()
        clock.tick(fps*speed)
#############################################################################################################

main()