import pygame
import random
import os
import json

#initializing game
pygame.init()

#intializing audio mixer
pygame.mixer.init()

#game window height and width
screen_w=500
screen_h=500

#making game window
gameWindow=pygame.display.set_mode((screen_w,screen_h))
clock=pygame.time.Clock()
caption=pygame.display.set_caption("Py-Snake")

#creating score file if not created and reading its data
if not (os.path.exists("score.json")):
    with open("score.json","w") as f:
        params={"easy":0,"hard":0}
        json.dump(params,f)
    f.close()

with open("score.json","r") as c:
    data=json.load(c)

#some colors' RGB values
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)

#drawing snake
def draw_snake(gameWindow,color,snake_list,snake_size):
    for x,y in snake_list:
        pygame.draw.rect(gameWindow,color,[x,y,snake_size,snake_size])

#adding text in screen
def text_screen(text,color,x,y,f_s=30):
    font=pygame.font.SysFont(None,f_s)
    screen_text=font.render(text,True,color)
    gameWindow.blit(screen_text,[x,y])


#creating welcome window
def welcome():
    running=True
    while running:
        gameWindow.fill(white)
        text_screen("Welcome To Py-Snake",black,98,170,45)
        text_screen("Press 1 to Play Easy Mode",black,125,220)
        text_screen("Press 2 to Play Hard Mode",black,125,250)
        text_screen("(Use arrow keys to control the snake)",black,130,300,20)
        pygame.display.update()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_1:
                    running=False
                    gameloop(1,data['easy'])
                if event.key==pygame.K_2:
                    running=False
                    gameloop(2,data['hard'])


#updating high score in file
def write_file(mode,score):
    global data
    if mode==1:
        data['easy']=score
    else:
        data['hard']=score
    with open("score.json","w") as file:
        json.dump(data,file)
    file.close()


#creating the gameloop
def gameloop(mode,hiscore):

    #initializing game variables
    global white,black,red
    running=True
    snake_size=20
    snake_x=50 #snake position in x-axis
    snake_y=50 #snake position in y-axis
    velocity_x=0 #snake moving speed in x-axis
    velocity_y=0 #snake moving speed in y-axis
    snake_speed=2 #snake moving speed

    #direction checking variables
    mov_x=False 
    mov_y=False

    #snake's food variables
    food_x=random.randint(25,screen_w-25)
    food_y=random.randint(25,screen_h-25)
    food_size=20

    #setting game score
    score=0

    #controling snake length
    snake_len=1
    snake_list=[]

    #variables to control screen after user loses the game
    gameover=False
    pl=False

    while running:
        gameWindow.fill(white)

        #initializing game window controls
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RIGHT:
                    if not mov_x:
                        snake_x+=10
                        velocity_x=snake_speed
                        velocity_y=0
                        mov_x=True
                        mov_y=False
                
                if event.key==pygame.K_LEFT:
                    if not mov_x:
                        snake_x-=10
                        velocity_x=-snake_speed
                        velocity_y=0
                        mov_x=True
                        mov_y=False

                if event.key==pygame.K_UP:
                    if not mov_y:
                        snake_y-=10
                        velocity_x=0
                        velocity_y=-snake_speed
                        mov_x=False
                        mov_y=True

                if event.key==pygame.K_DOWN:
                    if not mov_y:
                        snake_y+=10
                        velocity_x=0
                        velocity_y=snake_speed
                        mov_x=False
                        mov_y=True

                if event.key==pygame.K_RETURN:
                    if gameover:
                        running=False
                        welcome()

        
        

        if not gameover:
            snake_x+=velocity_x
            snake_y+=velocity_y

            #controlling snake's length
            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)
            if len(snake_list)>snake_len:
                del snake_list[0]
            
            #checking if snake is biting itself
            if head in snake_list[:-1]:
                gameover=True

            #drawing food, snake and adding score and high score in game window
            pygame.draw.rect(gameWindow,red,[food_x,food_y,food_size,food_size])
            text_screen(f"Score: {score}",red,10,10)
            text_screen(f"High-Score:{hiscore}",red,360,10)
            draw_snake(gameWindow,black,snake_list,snake_size)

        #logic to see if snake eat the food
        if (abs(snake_x-food_x) <=10) and (abs(snake_y-food_y) <=10):
            #playing snake eating sound
            pygame.mixer.music.load('eat.mp3')
            pygame.mixer.music.play()
            food_x=random.randint(40,screen_w-40)
            food_y=random.randint(40,screen_h-40)
            #incrementing score and snake's length
            score+=1
            snake_len+=5

            #updating highscore
            if (score>int(hiscore)):
                hiscore=score

        #controlling game mode
        if mode==1:
            #easy mode -> no box limit
            if(snake_x<=0 and velocity_x<0):
                snake_x=screen_w
            if (snake_x>=screen_w and velocity_x>0):
                snake_x=0-snake_size
            if(snake_y<=0 and velocity_y<0):
                snake_y=screen_h
            if (snake_y>=screen_h and velocity_y>0):
                snake_y=0-snake_size
        else:
            #hard mode -> snake moves inside the box
            if (snake_x==12 or snake_x==470 or snake_y==30 or snake_y==470):
                gameover=True
            if running:
                pygame.draw.rect(gameWindow,red,[12,30,10,450])
                pygame.draw.rect(gameWindow,red,[480,30,10,450])
                pygame.draw.rect(gameWindow,red,[12,30,478,10])
                pygame.draw.rect(gameWindow,red,[12,480,478,10])

        #controlling game window after user loses the game
        if gameover:
            if running:
                gameWindow.fill(white)
                if not pl:
                    pl=True

                    #playing game over sound
                    pygame.mixer.music.load('over.mp3')
                    pygame.mixer.music.play()
                    #updating high score
                    write_file(mode,hiscore)
                text_screen(f"Game Over!! Your Score: {score}",red,120,200)
                text_screen(f"Press Enter To Continue",red,130,230)
        if running:
            pygame.display.update()
            clock.tick(60)
    
    #updating high score if user closes the game without losing
    write_file(mode,hiscore)
    
    pygame.quit()

welcome()
c.close()
