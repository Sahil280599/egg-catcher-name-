from itertools import cycle
from random import randrange
from tkinter import Tk , Canvas , messagebox , font

# Design frame

canvas_width = 900
canvas_height = 500


win = Tk()
win.title('Egg Catcher')
c = Canvas(win , width = canvas_width ,  height = canvas_height , background = 'black')
c.create_rectangle(-5, canvas_height - 100 , canvas_width + 5 , canvas_height + 5 , fill='dark green', width=0)
c.create_oval(-80,-80,120,120,fill='white' , width=0)
c.pack()

color_cycle = cycle(['light blue' , 'light pink' , 'light yellow','light green' , 'red', 'blue' , 'white','yellow'])
egg_width = 45
egg_height = 55
egg_score = 10
egg_speed = 500
egg_interval = 4000                                                             #appearing every 4 sec of falling egg
difficulty_factor = 0.95

catcher_color = 'white'
catcher_width = 100
catcher_height = 100
catcher_start_x = canvas_width / 2 - catcher_width / 2
catcher_start_y = canvas_height -catcher_height - 20
catcher_start_x2 = catcher_start_x + catcher_width
catcher_start_y2 = catcher_start_y + catcher_height

catcher = c.create_arc(catcher_start_x ,catcher_start_y ,catcher_start_x2,catcher_start_y2 , start=200 , extent = 140 , style='arc' , outline=catcher_color , width=3)


# other interface item
score = 0                                                                                #initial score
# north west direction of score text
score_text = c.create_text(10,10,anchor='nw' , font=('Arial',18,'bold'),fill='darkblue',text='Score : ' + str(score))

#lives remaining
lives_remaning = 5
lives_text = c.create_text(canvas_width-10,10,anchor='ne' , font=('Arial',18,'bold'),fill='yellow',text='life : ' + str(lives_remaning))

# creating an egg and motion of the egg
eggs = []  # creating list

def create_eggs():
    x = randrange(10,740)                                                  #selecting random position for eggs axis 10-740
    y = 40
    new_egg = c.create_oval(x,y,x+egg_width,y+egg_height,fill=next(color_cycle),width=0)
    eggs.append(new_egg)
    win.after(egg_interval,create_eggs) # passing individual at every 4 second

def move_eggs():
    for egg in eggs:
        (egg_x,egg_y,egg_x2,egg_y2) = c.coords(egg)      #provide coordinates of each eggs
        c.move(egg,0,10)                                 # move eggs with coordinate with 0 with distance 10
        if egg_y2 > canvas_height:
            egg_dropped(egg)
    win.after(egg_speed,move_eggs)

def egg_dropped(egg):
    eggs.remove(egg)
    c.delete(egg)
    lose_a_life()
    if lives_remaning == 0:
        messagebox.showinfo('GAME OVER!' , 'FINAL SCORE : ' + str(score))
        win.destroy()

def lose_a_life():
    global lives_remaning
    lives_remaning -= 1    # life decreased by 1
    c.itemconfigure(lives_text , text='LIVES : ' + str(lives_remaning))

def catch_check():
    (catcher_x,catcher_y,catcher_x2,catcher_y2) = c.coords(catcher)
    for egg in eggs:
        (egg_x,egg_y,egg_x2,egg_y2) = c.coords(egg)
        if catcher_x < egg_x and egg_x2  < catcher_x2 and catcher_y2 - egg_y2 < 40: #using logic of which side is greater to catch up egg
            eggs.remove(egg)               # when catched it will remove the egg
            c.delete(egg)
            increase_score(egg_score)       # gained score

# this is for one instance so we called it again and again
    win.after(100,catch_check) # 100miliseconds time

def increase_score(points):
    global score , egg_speed , egg_interval
    score += points
    egg_speed = int(egg_speed * difficulty_factor)
    egg_interval = int(egg_interval * difficulty_factor)
    c.itemconfigure(score_text , text='Score : ' + str(score)) # configure the new score

def move_left(event):
    (x1,y1,x2,y2) = c.coords(catcher)
    if x1 > 0:
        c.move(catcher,-20,0) # by this we can move our catcher for left direction


def move_right(event):
    (x1,y1,x2,y2) = c.coords(catcher)
    if x2 < canvas_width:
        c.move(catcher,20,0) # for right

c.bind('<Left>' , move_left)    #bind keys with function in <>
c.bind('<Right>' , move_right)
c.focus_set()  #to check whether keys are pressed

win.after(1000,create_eggs)
win.after(1000,move_eggs)
win.after(1000,catch_check)

win.mainloop()
