import pygame
import math
import random
import tkinter as tk
from tkinter import messagebox
from collections import deque

#Cosas que necesitamos para la ia
    #reset function
    #reward system
    #play(action) -> direction
    #game_iteration
    #cambiar is_colission

class cube(object):
    def __init__(self,start,dirx=1,diry=0,color=(0,255,0)):
        self.pos = start
        self.dirx=dirx
        self.diry=diry
        self.color = color

    def draw(self,surface):
        pygame.draw.rect(surface,self.color,(self.pos[0]*25+1,self.pos[1]*25+1,23,23))

class snake(object):
    body = deque()
    turns = {}
    def __init__(self,color,pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirx = 1
        self.diry = 0

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.dirx != 1:
                    self.dirx, self.diry = -1 , 0
                elif event.key == pygame.K_RIGHT and self.dirx != -1:
                    self.dirx, self.diry = 1 , 0
                elif event.key == pygame.K_UP and self.diry != 1:
                    self.dirx, self.diry = 0 , -1
                elif event.key == pygame.K_DOWN and self.diry != -1:
                    self.dirx, self.diry = 0 , 1

    #    if self.head.pos[0] <= 0 and self.dirx == -1: new_head_pos = (ROWS-1,self.head.pos[1])
    #    elif self.head.pos[0] >= ROWS-1 and self.dirx == 1: new_head_pos = (0,self.head.pos[1])
    #    elif self.head.pos[1] >= ROWS-1 and self.diry == 1: new_head_pos = (self.head.pos[0],0)   esto es para jugar sin paredes
    #    elif self.head.pos[1] <= 0 and self.diry == -1: new_head_pos = (self.head.pos[0],ROWS-1)
    #    else: new_head_pos = (self.head.pos[0] + self.dirx, self.head.pos[1] + self.diry)
        new_head_pos = (self.head.pos[0] + self.dirx, self.head.pos[1] + self.diry)

        new_head = cube(new_head_pos)
        self.body.appendleft(new_head)
        self.head = new_head
        self.body.pop()
    
    def choque(self):                                                          #para jugar con paredes
        return (self.head.pos[0] < 0 or self.head.pos[0] > ROWS-1 or
        self.head.pos[1] > ROWS-1 or self.head.pos[1] < 0)

    def reset(self,pos):
        self.head = cube(pos)
        self.body = deque()
        self.body.append(self.head)
        self.dirx = 1
        self.diry = 0

    def addCube(self):
        tail = self.body[-1]
        self.body.append(tail)

    def draw(self,surface):
        for c in self.body:
            c.draw(surface)

def drawGrid(w,rows,surface):
    sizeBtwn = w // rows
    for i in range(rows):
        pygame.draw.line(surface,(30,30,30),(0,sizeBtwn*i),(500,sizeBtwn*i))
        pygame.draw.line(surface,(30,30,30),(sizeBtwn*i,0),(sizeBtwn*i,500))

def redrawWindow(surface):
    global ROWS, WIDTH, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(WIDTH,ROWS,surface)
    pygame.display.update()

def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if not any(z.pos == (x, y) for z in positions):
            break

    return (x,y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost",True)
    root.withdraw()
    messagebox.showinfo(subject,content)
    try:
        root.destroy()
    except:
        pass

def main():
    global WIDTH, ROWS, s, snack
    WIDTH = 500
    ROWS = 20
    win = pygame.display.set_mode((WIDTH,WIDTH))
    s = snake((0,255,0),pos=(10,10))
    snack= cube(randomSnack(ROWS,s),color=(255,0,0))
    clock = pygame.time.Clock()
    flag = True
    while flag:
        pygame.time.delay(80)  #pausa la ejecucion durante 80ms
        clock.tick(40)         #40FPS
        s.move()
        if s.head.pos == snack.pos:
            s.addCube()
            snack= cube(randomSnack(ROWS,s),color=(255,0,0))
        
        if s.choque() == True:
            puntuacion =(len(s.body)-1)
            mensaje = "Puntuacion: {}. \n Nueva Partida".format(puntuacion)
            message_box("Perdiste",mensaje)
            s.reset((5,10))
            
        for cubo in range(1,len(s.body)):
            if (s.head.pos == s.body[cubo].pos and len(s.body)> 2):
                puntuacion =(len(s.body)-1)
                mensaje = "Puntuacion: {}. \n Nueva Partida".format(puntuacion)
                message_box("Perdiste",mensaje)
                s.reset((5,10))
        redrawWindow(win)      #actualiza la pantalla

main()