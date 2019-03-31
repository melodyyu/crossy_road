import pygame


#convert everything into one class

#global variables (dimensions)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Crossy RPG Kai'
#global variables (color)
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

#FPS clock
clock = pygame.time.Clock()

#initialize font 
pygame.font.init()
font = pygame.font.SysFont('comicsans', 75)


class Game:

    #set FPS of clock; typical=60
    TICK_RATE = 60

    #turn into constructor for width(screen_width) height and title (game_screen)
    def __init__ (self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height

        #create window of specified size to display game 
        self.game_screen = pygame.display.set_mode((width,height))
        #set window color to white 
        self.game_screen.fill(WHITE_COLOR)
        #name the window 
        pygame.display.set_caption(title)

        #load background image
        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))

    #Note: every function needs self
    #loop to constantly update game (movement, graphics, collision 
    def run_game_loop(self, level_speed):
        is_game_over = False
        #boolean to check if we won or not 
        did_win = False 
        direction = 0

        #create player character
        player_char = PlayerChar('player.png', 375, 700, 50, 50)
        enemy_0 = NonPlayerChar('enemy.png', 20, 600, 50, 50)
        treasure = GameObject('treasure.png', 375, 50, 50, 50)
        #create more enemies w/ diff starting points 
        enemy_1 = NonPlayerChar('enemy.png', 40, 400, 50, 50)
        enemy_2 = NonPlayerChar('enemy.png', 60, 200, 50, 50)

        #multiply enemy speed with each level
        enemy_0.SPEED *= level_speed 

        #runs until is_game_over = True
        while not is_game_over:
            #if there's a quit type event, exit out of loop
            #events that can cause game to quit are key/mouse pressing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_game_over = True

                #if a key is being pressed down and *held down*, moves 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        #if up key is pressed, we move up
                        direction = 1
                    elif event.key == pygame.K_DOWN:
                        #if down key is pressed, we move down
                        direction = -1

                #if key is pressed up, prevent movement 
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0 
                    
                print(event)

            #redraw screen; then redraw everything on top of it after a loop 
            self.game_screen.fill(WHITE_COLOR)
            #render the game screen
            self.game_screen.blit(self.image, (0,0)) 

            #treasure appears on screen too
            treasure.draw(self.game_screen)
            
            #move player in whatever direction and amount they chose
            player_char.move(direction, self.height)
            #everytime we move player, must redraw it
            player_char.draw(self.game_screen) 

            #do the same as above, but for the enemy
            enemy_0.move(self.width)
            enemy_0.draw(self.game_screen)


            #spawn more enemies at certain levels
            if level_speed > 3:
                enemy_1.move(self.width)
                enemy_1.draw(self.game_screen)
                #print levels
                #text=font.render('Level', level_speed, True, BLACK_COLOR)
            if level_speed > 5:
                enemy_2.move(self.width)
                enemy_2.draw(self.game_screen)
            
            #figure out when game is over 
            if player_char.detect_collision(enemy_0):
                is_game_over = True
                did_win = False
                text = font.render(':( Try again!', True, BLACK_COLOR)
                self.game_screen.blit(text, (275, 350))
                pygame.display.update()
                clock.tick(1)
                break
            elif player_char.detect_collision(treasure):
                is_game_over = True
                did_win = True

                #render the text 
                text = font.render('You won! :)', True, BLACK_COLOR)
                #put text on screen
                self.game_screen.blit(text, (275, 350))
                #update the display
                pygame.display.update()
                #wait for game to tick once
                clock.tick(1)
                #break out of it to start the game again 
                break
            
        
        

            #update all game graphics
            pygame.display.update()
            #tick clock to update everything in game
            clock.tick(self.TICK_RATE)

        if did_win:
            #recursive function; we won, be able to play game again
            #increase game by 0.5 everytime you win 
            self.run_game_loop(level_speed + 0.5)
        else:
            #we lost, break out of the game and quit t 
            return 
# class used to create enemy, play char and treasure
class GameObject:

    #take x,y,width,height as parameters bc need to transform image anyways
    def __init__ (self, image_path, x, y, width, height):

        #take image, load it and display it
        object_image = pygame.image.load(image_path)
        #scale image up
        self.image = pygame.transform.scale(object_image, (width,height))
        
        self.x_pos= x
        self.y_pos = y

        self.width = width
        self.height = height 


    #draw objects on top of the background
    def draw(self, background):
        #blit = takes image and places it on top of another image at the specified location
        background.blit(self.image, (self.x_pos, self.y_pos))
        

class PlayerChar(GameObject):

    #add in speed to determine FPS of character
    #how many tiles the character moves at once 
    SPEED = 10

    #default initializer
    def __init__ (self, image_path, x, y, width, height):
        super().__init__ (image_path, x, y, width, height)

    #movement differs. don't need to take in a specific amt cuz we have global var speed
    #can also prevent the character from moving past the top 
    def move(self, direction, max_height):

        #move by static amount each time 
        if direction > 0:
            #y up in neg direction = moves up
            self.y_pos -= self.SPEED

            #move down 
        elif direction < 0:
            self.y_pos += self.SPEED

        #prevent from moving to max height
        if self.y_pos >= max_height - 40:
            #bounces character back from top mark if it reaches there 
            self.y_pos = max_height -40

    #if we're on overlap with enemy's y-pos, return True = we've collided 
    def detect_collision(self, other_body):
        #if the lowest part of our body is lower than the lowest part of their body,
        #then we're safe 
        if self.y_pos > other_body.y_pos + other_body.height:
            return False
        #if we're above the enemy, there's no collision
        elif self.y_pos + self.height < other_body.y_pos:
            return False

        #do the same for the x_pos; if our x_pos > other_body's x_pos, return F
        if self.x_pos > other_body.x_pos + other_body.width:
            return False
        #we know we're not occupying the same x_pos 
        elif self.x_pos + self.width < other_body.x_pos:
            return False 

        #if all of these fail, then that means there's collision, so return True
        return True

        


#class for enemies moving L <-> R 
class NonPlayerChar(GameObject):

    #add in speed to determine FPS of character
    #how many tiles the character moves at once 
    SPEED = 10

    #default initializer
    def __init__ (self, image_path, x, y, width, height):
        super().__init__ (image_path, x, y, width, height)

    #method for movement. turns around once it reaches close to the end. 
    def move(self, max_width):
        #if char at 20 tiles from L side of screen, turn around 
        if self.x_pos <= 20:
            self.SPEED = abs(self.SPEED)
        #if char at 20 tiles from R side of screen, turn around
        elif self.x_pos >= max_width - 40:
            self.SPEED = -abs(self.SPEED)

        self.x_pos += self.SPEED 
            

            
#initialize pygame
pygame.init

new_game = Game('background.png',SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
#start game at speed 1 
new_game.run_game_loop(1)


pygame.quit()
quit()

   
