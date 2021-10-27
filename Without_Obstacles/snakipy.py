#snake game

import random
import cv2
from PIL import Image
import numpy as np
import keyboard
import time
import copy
import math
from tkinter import Tk,Label,Button,Toplevel

#Dimension of the game area
SIZE =30

class Snake:
    body = {}
    snake = [0,0,255]
    food = [255,0,0]
    end=False
    def __init__(self):
        self.snake_pos = [SIZE//2,SIZE//2,0]
        self.body={}
        self.food_pos = random.sample(range(SIZE),2)
        self.snake_len = 0
        self.velo = 100
        self.refer = self.snake_pos
        self.game = np.zeros((SIZE,SIZE,3))
        self.refer = copy.deepcopy(self.snake_pos)
        self.body[self.snake_len] = self.snake_pos
        self.end = False

    def play(self,ch):
        self.snake_pos[2] = ch
        self.move()
        
        
    def point_val(self):
        if self.snake_pos[:-1] == self.food_pos:
            self.snake_len += 1
            self.body[self.snake_len] = self.refer
            self.refer = copy.deepcopy(self.body[self.snake_len])
            self.food_pos = random.sample(range(SIZE),2)
            ref_lis = self.body.values()
            ref_lis = [i[:-1] for i in ref_lis]
            while self.food_pos in ref_lis:
                self.food_pos = random.sample(range(SIZE),2)

    def end_val1(self):
        if (self.snake_pos[0]<=0 and self.snake_pos[2]==0):
            return True
        elif (self.snake_pos[1]>=SIZE-1 and self.snake_pos[2]==1):
            return True
        elif (self.snake_pos[0]>=SIZE-1 and self.snake_pos[2]==2):
            return True
        elif (self.snake_pos[1]<=0 and self.snake_pos[2]==3):
            return True
        else:
            return False

    def end_val2(self):
        ref_dic = {}
        for i in self.body:
            if i==0:
                continue
            ref_dic[i]=self.body[i][:-1]
        if self.snake_pos[:-1] in ref_dic.values():
            return True
        else:
            return False


    def move(self):
        if self.end_val1():
            cv2.destroyWindow('snake')
            self.end=True

        if not(self.end):
            self.refer = copy.deepcopy(self.body[self.snake_len])

            if self.snake_pos[2]==0:                 #up
                self.snake_pos[0] = self.snake_pos[0]-1

            elif self.snake_pos[2]==1:              #right
                self.snake_pos[1] = self.snake_pos[1]+1

            elif self.snake_pos[2]==2:                #down
                self.snake_pos[0] = self.snake_pos[0]+1

            elif self.snake_pos[2]==3:                 #left
                self.snake_pos[1] = self.snake_pos[1]-1

            ref_dic = copy.deepcopy(self.body)
            self.body[0] = copy.deepcopy(self.snake_pos)
            for i in self.body:
                if i==0:
                    continue
                self.body[i] = ref_dic[i-1]


            self.point_val()
            if self.end_val2():
                cv2.destroyWindow('snake')
                self.end=True

            self.display()

    def display(self):
        self.game = np.zeros((SIZE,SIZE,3), dtype=np.uint8)
        if len(self.body)>1:
            for i in self.body.values():
                self.game[i[0]][i[1]] = self.snake
        else:
            self.game[self.snake_pos[0]][self.snake_pos[1]] = self.snake
        self.game[self.food_pos[0]][self.food_pos[1]] = self.food

        img = Image.fromarray(self.game, 'RGB')
        img = img.resize((600,600), resample=Image.BOX)
        cv2.imshow('snake',np.array(img))
        cv2.waitKey(int(self.velo))
        key = cv2.waitKey(20) & 0xFF
        if key==27:
            cv2.destroyWindow('snake')
            self.end=True
        self.velo = 100/math.sqrt((self.snake_len+1))


######main#######

score = 0
sc_txt = "Your Score : {}"
hsc_txt = "High Score : {}"
def game():
    global score
    Game = Snake()
    m=0
    while True:
        if keyboard.is_pressed('w'):
            if Game.snake_pos[2]!=2:
                Game.play(0)
                m=0
            else:
                Game.play(m)

        elif keyboard.is_pressed('d'):
            if Game.snake_pos[2]!=3:
                Game.play(1)
                m=1
            else:
                Game.play(m)

        elif keyboard.is_pressed('s'):
            if Game.snake_pos[2]!=0:
                Game.play(2)
                m=2
            else:
                Game.play(m)
        elif keyboard.is_pressed('a'):
            if Game.snake_pos[2]!=1:
                Game.play(3)
                m=3
            else:
                Game.play(m)
        else:
            Game.play(m)

        if Game.end:
            cv2.destroyAllWindows()
            break

    score2 = Game.snake_len
    if score2>score:
        score=score2
    sc.config(text = sc_txt.format(score2))
    hsc.config(text = hsc_txt.format(score))

def exit():
    box.destroy()

box = Tk()
box.title("SnakeGame")
box.geometry('200x150')
header = Label(box, text="Snake", font=("arial",30,"bold"), fg="steelblue").pack()

button_1 = Button(box, text="Play", fg='gray26', command=game)
button_1.pack()

button_2 = Button(box,text= "Exit", fg='gray26', command=exit)
button_2.pack()

sc = Label(box, text=sc_txt.format(score),font=("arial",10,"bold"),fg="red")
sc.pack()

hsc = Label(box, text=hsc_txt.format(score),font=("arial",10,"bold"),fg="red")
hsc.pack()

box.mainloop()
