import pygame
# pygame.init()
pygame.display.set_mode((1000,800))
pygame.display.set_caption("Gangster")
    
exit_game=False
while exit_game==False:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit_game=True
        if event.type==pygame.KEYDOWN and event.key==pygame.K_RIGHT:
            print("hello")