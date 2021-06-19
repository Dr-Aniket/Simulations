# Importing the libraries

import os
import time

# input(os.system(f'start "" "{os.getcwd()}"'))

from pyfiglet import Figlet
import colorama
import pygame
os.system('cls')

# Data file loading
data_file = os.path.join(os.getcwd(),'data.txt')
saved_file = os.path.join(os.getcwd(),'Saved Files')+'/'
while True:
    try:
        file = open(data_file,'r',encoding='utf-8')
        data = file.readlines()
        file.close()
        if len(data) == 0:
            raise 'Empty file'
        for line in data:
            line = line.lower()
            if 'time of life' in line:
                done = line.split('>')[-1].strip()
                done = float(done.strip())
                break
        Data = {}
        try:
            for line in data:
                line = line.strip().split('>')
                Data[line[0].strip().lower()] = line[-1].strip().lower()
        except Exception as e:
            print(e)
        break
    except:
        data = open(data_file,'w',encoding='utf-8')
        cmds = ['name','factor','edge','font face','delay','starts in','time of life']
        Data = {}
        for cmd in cmds:
            answer = input(f'{cmd.title()} : ').lower()
            Data[cmd] = answer

        for cmd in Data:
            data.write(f'{cmd.title()} > {Data[cmd].title()}\n')
        data.close()

# Setting up the Values
name_of_universe = Data['name'].title()
factor = int(Data['factor'])
# factor = int(input("Enter the factor  :".title()))
edge = int(Data['edge'])
edge = edge + (edge%factor)
size = edge//factor
fontFace = Data['font face']
active_cells = []
dead = (0,0,0)
alive = (255,255,255)
grid_color = (255,0,0)
grid_thickness = 1
starts_in = float(Data['starts in'])
delay = int(Data['delay'])
time_of_life = float(Data['time of life'])

# Initilising the Engine
os.system('cls')
colorama.init()
color = colorama.Fore
display = Figlet(font = fontFace,width = 300)
displayEnd = Figlet(font = 'slant',width = 300)

def head():
    print(color.MAGENTA+display.renderText(name_of_universe)+color.RESET)
head()

def point_coordinate(point):
    x = 1+ (size*(abs((point-1)%factor)))
    y = 1 + (((point-1)//factor)*size)
    # print(f'size =   {size} : point%factor =  {abs(point%factor)}',end=' ')
    return x,y
    

def show_matrix(active):
    os.system('cls')
    head()
    
    see = True
    # see = False
    if see:
        for point in range(1,factor**2+1):
            if point_coordinate(point) in active:
                print(color.GREEN+str(point)+color.RESET,end='\t')
            else:
                print(color.RED+str(point)+color.RESET,end='\t') # '██'
            if point % factor ==0:
                print('\n')
def get_cell(x,y):
    x = 1 + ((x//size)*size)
    y = 1 + ((y//size)*size)
    return x,y

def activating_cells():
    active_cell = False
    alive = (0,255,0)
    dead = (255,0,0)
    active_cells = []
    pygame.init()
    activator = pygame.display.set_mode((edge,edge))
    pygame.display.set_caption('Activator')
    activator.fill(dead)
    run = True
    while run:
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    run = False
                    break

            if pygame.mouse.get_pressed()[0]:
                coordinate = pygame.mouse.get_pos()
                break
            else:
                coordinate = False
        if coordinate:
            x,y = coordinate
            active_cell = get_cell(x,y)
            if active_cell in active_cells:
                pass
                # pygame.draw.rect(activator,dead,(active_cell[0],active_cell[1],size,size))
                # active_cells.remove(active_cell)
            else:                
                pygame.draw.rect(activator,alive,(active_cell[0],active_cell[1],size,size))
                active_cells.append(active_cell)
                active_cells = list(set(active_cells))
        else:
            active_cell = False
    pygame.quit()
    return active_cells


'''
Set the active Cells
'''
# while True:
try:
    # active_cells.sort()
    # show_matrix(active_cells)
    cell = input("File to Open : ".title()).strip()

    if len(cell) == 0:
        cell = '''GUI Activator'''
            
    if cell[0].lower() == 'r':
        cell = cell.split(' ' ,1)[-1].lower().strip()
        file = 'memory.txt'
        if cell != 'r':
            for path,folder,files in os.walk(saved_file):
                for f in files:
                    # print(cell.lower().strip(),f.lower().strip())
                    if cell.lower().strip() in f.lower().strip():
                        file = f
                        break
                        
        print(color.YELLOW + f'Opening File : {file}' + color.RESET)
        memory = open(saved_file+file,'r').readlines()
        time.sleep(1)
        for point in memory:
            point = point.strip().split()
            x = int(point[0].strip())
            y = int(point[1].strip())
            active_cells.append((x,y))
    else:
        active_cells = activating_cells()    
    #     break
    # elif cell.strip() == '':
    #     continue
    # elif cell == '/':
    #     break
    # try:
    #     cell = int(cell)
    #     if cell > (edge//size)**2 or cell < 1:
    #         continue
    # except:
    #     continue
    # point = cell 
    # if point <= factor**2 or point >0: 
    #     active_cells.append(point_coordinate(point))
    #     active_cells = list(set(active_cells))

except Exception as e:
    input(e)
    pass

# show_matrix(active_cells)

# Saving the data in the Memory
memory = open(saved_file+'memory.txt','w')
for active_cell in active_cells:
    active_cell = str(active_cell).replace('(','').replace(')','').replace(',',' ').strip()
    memory.write(f'{active_cell}\n')
memory.close()
print(color.RESET,end='')
print(f'Starting the Stimulation in  {starts_in} Secs')
time.sleep(starts_in)
# setting up the universe

# Make the Grid    
def show_grid():
    for x in range(1,edge):
        for y in range(1,edge):
            if x%size == 0 and y%size == 0:
                pygame.draw.rect(universe,alive,(x,y,grid_thickness,grid_thickness))

pygame.init()
universe = pygame.display.set_mode((edge,edge))
pygame.display.set_caption(name_of_universe)

online = True
end_msg = None
os.system('cls')
head()
birth = time.time()
clock = pygame.time.Clock()
while online:
    new_active_cells = []
    for y in range(1,edge,size):
        for x in range(1,edge,size):
            alive_neighbours = 0
            
            coordinate = x,y 

            ## COUNTING THE NEIGHBOURS

            # (1,1) Neighbour
            i = x-size
            j = y-size
            if x == 1:
                i = size * (factor-1) + 1
            if y == 1:
                j = size * (factor-1) + 1
            if (i,j) in active_cells:
                alive_neighbours += 1

            # (1,2) Neighbour
            i = x
            j = y-size
            if y == 1:
                j = size * (factor-1) + 1
            if (i,j) in active_cells:
                alive_neighbours += 1

             # (1,3) Neighbour
            i = x+size
            j = y-size
            if x == size * (factor-1) + 1:
                i = 1
            if y == 1:
                j = size * (factor-1) + 1
            if (i,j) in active_cells:
                alive_neighbours += 1

             # (2,1) Neighbour
            i = x-size
            j = y
            if x == 1:
                i = size * (factor-1) + 1
            if (i,j) in active_cells:
                alive_neighbours += 1

             # (2,3) Neighbour
            i = x+size
            j = y
            if x == size * (factor-1) + 1:
                i = 1
            if (i,j) in active_cells:
                alive_neighbours += 1

             # (3,1) Neighbour
            i = x-size
            j = y+size
            if x == 1:
                i = size * (factor-1) + 1
            if y == size * (factor-1) + 1:
                j = 1
            if (i,j) in active_cells:
                alive_neighbours += 1

             # (3,2) Neighbour
            i = x
            j = y+size
            if y == size * (factor-1) + 1:
                j = 1
            if (i,j) in active_cells:
                alive_neighbours += 1

             # (3,3) Neighbour
            i = x+size
            j = y+size
            if x == size * (factor-1) + 1:
                i = 1
            if y == size * (factor-1) + 1:
                j = 1
            if (i,j) in active_cells:
                alive_neighbours += 1

            ## APPLYING THE LAWS TO THE UNIVERSE
             
            if alive_neighbours == 3:       # If Exactly 3 neighbours are alive the cell is born at the coordinate
                 new_active_cells.append(coordinate)
            elif alive_neighbours == 2 and coordinate in active_cells:  # if the alive cell have 2 or 3 alive neighbours than it will remain alive
                new_active_cells.append(coordinate)
                                                                       # Else the cell will die
    active_cells.sort()
    new_active_cells.sort()
    if active_cells == new_active_cells:
        online = False
        end_msg = 'stable'
    else:
        active_cells = new_active_cells
    
    if len(active_cells) == 0:
        online = False
        end_msg = 'extinct'
    else:
        active_cells = list(set(active_cells))
    universe.fill(dead)
    for active_cell in active_cells:
        x = active_cell[0]
        y = active_cell[1]
##        pygame.draw.circle(universe,alive,(x,y),size,size)
        pygame.draw.rect(universe,alive,(x,y,size,size))
        

    # show_grid()
    # show_matrix(active_cells)
    # pygame.display.update()
    pygame.display.flip()
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or key[pygame.K_RETURN] or key[pygame.K_ESCAPE]:
            online = False
            end_msg = 'killed'
            break
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            active_cells.append(get_cell(pos[0],pos[1]))
        
    ''' Showing the Age of our Virtual Universe '''
    os.system('cls')
    head()
    age = round(time.time() - birth,1)
    print(color.YELLOW+f'Age of the Universe : {age} Million Years'+color.RESET,end = '\r')
    if age >= (60*time_of_life):
        online = False
        end_msg = 'dead'
    if end_msg != None:
        os.system('cls')
        head()
        end_msg = end_msg.lower()
        if 'ext' in end_msg:
            colour = color.LIGHTYELLOW_EX
        elif 'dead' in end_msg:
            colour = color.LIGHTRED_EX
        elif 'kill' in end_msg:
            colour = color.RED
        elif 'stable' in end_msg:
            colour = color.GREEN
        else:
            colour = color.WHITE
        print(colour + displayEnd.renderText(f'{end_msg}'.title()))
        print(f'Age of the Universe : {age} Million Years\n')
        pygame.quit()
        break
##    pygame.time.delay(delay)
    clock.tick(delay)
save_name = input(color.CYAN + '\nEnter the Name With Which You want to save the Memory File : ').split('.')[0].strip().lower()
if save_name != '':
    if os.path.exists(saved_file+f'{factor} {save_name} [{end_msg}].txt'):
        save_name += f' {age} '
    os.rename(saved_file+'memory.txt',saved_file+f'{factor} {save_name} [{end_msg}].txt')
