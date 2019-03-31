import pygame

#initialize pygame to actually use the library
pygame.init


#dimensions of the game (width, height and color)
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SCREEN_TITLE = 'Crossy RPG'
WHITE_COLOR = (255,255,255)
BLACK_COLOR = (0,0,0)

#set FPS clock
clock=pygame.time.Clock()
#how many iterations of the clock; typical = 60
TICK_RATE = 60
#determine if game is still running
is_game_over = False

#creates screen of that width and height
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#sets game window color to white 
game_screen.fill(WHITE_COLOR)
#set game window title
pygame.display.set_caption(SCREEN_TITLE)

#load an image 
player_image = pygame.image.load('player.png')
#transform the image to a different dimension
player_image = pygame.transform.scale(player_image, (50, 50))


#loop to constantly update game (movement, graphics, collision checks)
#runs until is_game_over is T
while not is_game_over:

    #check if the events that can occur cause game to quit
    for event in pygame.event.get():
        #if there's a quit type event, then exit out of loop
        if event.type == pygame.QUIT:
            is_game_over = True
        #print the events
        #events can be key/mouse pressing 
        print(event)

    #create a rectangle; param = x,y pos and then width/height
    #note: that if you try to center, the top L corner is the start of the rectangle
    #so make sure you adjust (250 -> 200). also remember that coordinate systems
    # for graphs = increase x >> move down; increase y >> move down 
 #   pygame.draw.rect(game_screen, BLACK_COLOR, [200, 200, 100, 100])

    #create a circle; param = pos, radius, width = 0. should put circle on top of square
 #   pygame.draw.circle(game_screen, BLACK_COLOR, (250, 150), 50)


    game_screen.blit(player_image, (225, 225))
    
    #display screen;update graphics 
    pygame.display.update()

    #clock ticks to render next frame; runs at FPS of 60
    clock.tick(TICK_RATE)

#exits out of program and pygame
pygame.quit()
quit()
