try:
    import pygame 
except:
    import os
    path = os.getcwd()
    file = os.path.basename(__file__)
    file = f'{path}\{file}'
    os.system("pip install pygame")
    os.system(f'start "" "{file}"')
    exit()
pg = pygame
from random import randint as rand
import pygame.display as display
import pygame.draw as draw
import time


######################################################################
def color(number : int):
    ''' Color on a Circular Scale ''' 
    if int(number) == -1:
        return (255,255,255)        
    number = abs(int(number))
    if number >= 400:
        number = number - ( 300 * ((number-100)//300))
    r = 0
    g = 0
    b = 0
    if number <= 100:
        percent = number/100
        r = int(percent * 255)
    elif number > 100 and number <= 200:
        number = number - 100
        percent = number/100
        g = int(percent * 255)
        r = 255 - g

    elif number >200 and number <= 300:
        number = number - 200
        percent = number/100
        b = int(percent * 255)
        g = 255 - b
    elif number > 300 and number <= 400:
        number = number - 300
        percent = number/100
        r = int(percent * 255)
        b = 255 - r
    else:
        r = g = b = 255
    return (r,g,b)
######################################################################

######################################################################
dimx = 800
dimy = 610
fullScreen = False
fps = 60
speed = 0
######################################################################

def newSpace(name = "Probability"):
    global dimx,dimy,simulate
    pg.init()
    if fullScreen:
        space = display.set_mode((0,0),pg.FULLSCREEN)
        dimx,dimy = display.get_window_size()
    else:
        space = display.set_mode((dimx,dimy))
        display.set_caption(name)
    simulate = True
    return space

#######################################################
def displayTxt(txt,x=dimx//2,y=20,c = (20,200,255)):
    font = pygame.font.Font('freesansbold.ttf', 20)
    txt = font.render(txt,True,c)
    textRect = txt.get_rect()
    textRect.center = (x,y)
    space.blit(txt,textRect)
#######################################################

class Bar:
    def __init__(self,x,y):
        self.per = 0
        self.len = 0
        self.width = 40
        self.x = x
        self.y = y
        self.color = color(100 + self.len)
        self.count = 0
        self.set(self.per)
        
    def update(self):
        self.count += 1

    def set(self,tot):
        try:
            self.per = round((self.count/tot)*100,1)
        except:
            self.per = 0
        self.len = self.per * 5
        if self.len<1:
            self.len=1
        self.color = color(100+self.len*2)
        
    
    def draw(self):
        x = self.x
        y = self.y - self.len 
        draw.rect(space,self.color,(x,y,self.width,self.len))
        displayTxt(f'{self.per}%',self.x+20,dimy-80)

def run():
    clock = pg.time.Clock()
    global dimx,dimy,simulate,space,speed
    space = newSpace()
    startHeight = dimy-100
    dis = 70
    noOfBars = 4
    bars = []
    for i in range(noOfBars):
        bars.append(Bar(dimx//3+dis*i,startHeight))
    total = 0
    pause = True
    while simulate:
        key = pg.key.get_pressed()
        while pause:
            displayTxt('Paused : {Press Space to Start}',y=dimy//2)
            display.flip()
            for event in pg.event.get():
                if key[pg.K_SPACE]:
                    pause = False
                    time.sleep(1)
                    break
            key = pg.key.get_pressed()
            space.fill((0,0,0))
            
        for event in pg.event.get():
            if event.type == pg.QUIT or key[pg.K_ESCAPE] or key[pg.K_RETURN]:
                simulate = False
                break
        space.fill((0,0,0))
        draw.line(space,color(350),(dimx//2-dimx//(8-noOfBars),startHeight+1),(dimx//2+dimx//(8-noOfBars),startHeight+1),2)
        
        for i in range(int(speed)+1):
            v = rand(1,noOfBars)
            bars[v-1].update()
            total += 1
        for bar in bars:
            bar.set(total)
            bar.draw()
        displayTxt(f'Total : {total}',y = dimy-50,c = color(-1))
        display.flip()
        speed = total/100 + 0.001
        clock.tick(fps*speed)
run()
