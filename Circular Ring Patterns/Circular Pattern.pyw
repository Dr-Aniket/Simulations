##########################################################################################
import pygame
pg = pygame
import pygame.display as display
import pygame.draw as draw
from vector import *
from color import *
from math import *
##########################################################################################

##########################################################################################
radius = 150
dimx = dimy = 500
fullscreen = False
fullscreen = True
bgColor = color(0)
fgColor = color(-1) + (1,)
fps = 60
speed = 1
##########################################################################################

##########################################################################################
def newSpace(name = 'Space',fullscreen = fullscreen):
    global dimx, dimy, simulate, space
    pg.init()
    if fullscreen:
        space = display.set_mode((0,0),pg.FULLSCREEN)
        dimx, dimy = display.get_window_size()
    else:
        space = display.set_mode((dimx,dimy))
        display.set_caption(name)
    simulate = True
##########################################################################################

##########################################################################################
class Ring:
    def __init__(self,center,theta):
        self.radius = radius
        self.color = 100
        self.theta = theta
        self.center = center

    def show(self):
        draw.circle(space,fgColor,(self.center.x,self.center.y),radius,1)
    
    def __eq__(self, o: object) -> bool:
        return self.theta == o[0].theta
    def __ne__(self, o: object) -> bool:
        return self.theta != o[0].theta
##########################################################################################
##########################################################################################
class Marker:
    def __init__(self,center,theta):
        self.radius = radius
        self.color = 100
        self.theta = theta
        self.center = center
        self.thickness = 10

    def update(self):
        self.theta += radians(1)
        self.color += 1
        pos = vector(cos(self.theta),-sin(self.theta)) * self.radius + self.center
        # draw.circle(space,fgColor,(self.center.x,self.center.y),radius,1)   # RING
        draw.circle(space,color(self.color),(pos.x,pos.y),self.thickness)   # MARKER
        self.y = (sin(self.theta) * self.theta + self.center.y)//10 * 10
##########################################################################################

##########################################################################################
def main():
    global simulate, space
    rings = []
    # newSpace(fullscreen= False)
    newSpace()
    clock = pg.time.Clock()
    theta = 0
    spaceCenter = vector(dimx//2,dimy//2)
    new = False
    while simulate:
        key = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT or key[pg.K_ESCAPE]:
                simulate = False
                break

            if key[pg.K_DELETE]:
                del rings
                rings = []
                theta = 0

        if key[pg.K_SPACE] or new and len(rings) < 20 :
            rad = radius//2
            c = vector( cos( theta ) , sin( theta ) ) * rad + spaceCenter
            rings.append( (Ring( c , theta ) , Marker( c , theta )))
            if rings[-1][0] in rings[:-1]:
                del rings[-1]
            theta += radians(30)

        space.fill(bgColor)
        
        for ring in rings:
            ring[0].show()
        for ring in rings:
            ring[1].update()

        display.flip()

        if len(rings) :
            try:
                y = rings[0][1].y
                new = (y == dimy//2)
                # print(y,new)
            except:
                pass
        clock.tick(fps*speed)
##########################################################################################
main()