import pygame
import random   # For random food generation
import os       # For ensuring if highscore file is created or not 
pygame.init()   # Initializing default modules
pygame.mixer.init()   # Initialising music module

# Display Specific variables
screen_width=700
screen_height=600
display=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Snake Game")

# Defining clock for the velocity of the snake
clock=pygame.time.Clock()
fps=60

def show_text(text,color,x,y,font_size=27):
    font=pygame.font.SysFont(None,font_size)  # Font
    output_text=font.render(text,True,color)
    display.blit(output_text,(x,y))

def draw_snake(display,color,snake_width,snake_height,travelled_points):
    for x,y in travelled_points:
        pygame.draw.rect(display,color,(x,y,snake_width,snake_height),border_radius=2)

# Background images
bg_home=pygame.image.load("image/homescreen.jpg")
bg_home=pygame.transform.scale(bg_home,(700,600)).convert_alpha()

bg_base=pygame.image.load("image/gamebase.jpg")
bg_base=pygame.transform.scale(bg_base,(700,600)).convert_alpha()

bg_over=pygame.image.load("image/gameover.jpg")
bg_over=pygame.transform.scale(bg_over,(700,600)).convert_alpha()

sound=True
# HomeScreen Loop
def homescreen():
    # Rendering background images
    display.blit(bg_home,(0,0))

    # Initial music
    global sound
    if sound:
        pygame.mixer.music.load("music/snake_effect.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

    exit_homescreen=False
    while exit_homescreen==False:
        show_text("Welcome to Snake's Zone!!","#2B8CD4",130,90,50)
        show_text("Press Enter to start","#37D42B",235,290,35)
        show_text("Press Spacebar to On/off the sound","#D4732B",200,430,28)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit_homescreen=True
                           
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    exit_homescreen=True
                    gameLoop()
                
                elif event.key==pygame.K_SPACE:
                    sound=not(sound)
                    if not(sound):
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.play()
            
        

        pygame.display.update()
        clock.tick(fps)

# GameLoop
def gameLoop():
    # Adding nagin music
    global sound
    if sound:
        pygame.mixer.music.load("music/nagin.mp3")
        pygame.mixer.music.set_volume(0.15)
        pygame.mixer.music.play(-1)
    # game variable
    exit_game=False
    game_over=False
    score=0

    # Snake specific variables
    snake_x=60
    snake_y=40
    snake_width=20
    snake_height=20
    velocity_x=0
    velocity_y=0
    previous_key="null"
    
    travelled_points=[]  # Snake travelled points list
    snake_length=1

    # Food for snake
    food_x=random.randint(10,screen_width-10)
    food_y=random.randint(10,screen_height-10) 
    food_width=20

    # Checking whether the file exists or not
    if (not os.path.exists("highscore.txt")):
        with open("highscore.txt",'w') as file:   #Creating New file if not exists
            file.write("0")    

    # Reading highscore from a file
    with open("highscore.txt","r") as file:
        highscore=file.read()

    # Loop starting
    while exit_game==False:
        # Game Over handling
        if game_over==True:
            display.blit(bg_over,(0,0))

            show_text("Game Over!! , Press Enter to replay","#E3E20C",100,230,45)
            show_text("Your Score : "+str(score),"#E9530C",240,310,40)
            
            for event in pygame.event.get():
                # exit event handling
                if event.type==pygame.QUIT:
                    exit_game=True

                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        gameLoop()
                        exit_game=True
     
        else:
            display.blit(bg_base,(0,0))
            for event in pygame.event.get():
                # exit event handling
                if event.type==pygame.QUIT:
                    exit_game=True
                
                # Game controls
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_LEFT and previous_key!="right" and previous_key!="left":
                        velocity_x-=3
                        velocity_y=0
                        previous_key="left"
                    if event.key==pygame.K_RIGHT and previous_key!="left" and previous_key!="right":
                        velocity_x+=3
                        velocity_y=0
                        previous_key="right"
                    if event.key==pygame.K_UP and previous_key!="down" and previous_key!="up":
                        velocity_y-=3
                        velocity_x=0
                        previous_key="up"
                    if event.key==pygame.K_DOWN and previous_key!="up" and previous_key!="down":
                        velocity_y+=3
                        velocity_x=0
                        previous_key="down"

            # Score Handling
            show_text("Score : "+str(score)+"   High Score : "+str(highscore),"green",200,3)

            # Making snake
            snake_head=[]
            snake_head.append(snake_x)
            snake_head.append(snake_y)
            travelled_points.append(snake_head)

            draw_snake(display,"black",snake_width,snake_height,travelled_points)

            # Snake travelling handling
            snake_x+=velocity_x
            snake_y+=velocity_y

            if len(travelled_points)>snake_length:
                travelled_points.pop(0)

            # Snake's collision handling
            if snake_x<=0 or snake_x>=screen_width or snake_y<=20 or snake_y>=screen_height:
                if sound:
                    pygame.mixer.music.load("music/collision.mp3")
                    pygame.mixer.music.set_volume(0.15)
                    pygame.mixer.music.play()
                game_over=True

            if snake_head in travelled_points[:-1]:
                if sound:
                    pygame.mixer.music.load("music/collision.mp3")
                    pygame.mixer.music.set_volume(0.15)
                    pygame.mixer.music.play()
                game_over=True
    
            # Food Handling
            food=pygame.draw.rect(display,"red",(food_x,food_y,food_width,snake_height),border_radius=4)
            if abs(snake_x-food_x)<10 and abs(food_y-snake_y)<10:
                food_x=random.randint(20,screen_width-20)
                food_y=random.randint(40,screen_height-20)
                score+=10
                snake_length+=5
            
            if int(highscore)<score:
                highscore=score

        # Writing highscore in the file
        with open("highscore.txt","w") as file:
            file.write(str(highscore))

        pygame.display.update()
        clock.tick(fps)

homescreen()