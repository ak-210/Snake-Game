import pygame
from pygame.locals import *
import time
import random

# reused values are written so we can easily change in future
SIZE = 40
bg_color = (70,255,70)
res = (1000, 680)

class Point:
    def __init__(self, main_screen):
        self.image = pygame.image.load('point.png').convert()
        self.image = pygame.transform.scale(self.image, (SIZE-1, SIZE-1))
        self.main_screen = main_screen
        self.x = SIZE*10
        self.y = SIZE*15

    def draw(self):
        self.main_screen.blit(self.image,(self.x, self.y))
        pygame.display.flip()

    def move(self):
        a = random.randint(0, res[0]/SIZE - 1)
        b = random.randint(0, res[1]/SIZE - 1)
        self.x = SIZE*a
        self.y = SIZE*b
        self.draw()

###########################  SNAKE CLASS  ################################

# Snake movement, growth etc.
class Snake:
    def __init__(self, main_screen, len, point):
        self.main_screen = main_screen
        self.block = pygame.image.load("block.jpg").convert()
        self.block = pygame.transform.scale(self.block, (SIZE-1, SIZE-1))
        self.length = len
        self.x = [SIZE]*self.length
        self.y = [SIZE]*self.length
        self.direction = 'right'
        self.pt = point

    def show_background(self, bg_p):
        bg = pygame.image.load(bg_p).convert()
        bg = pygame.transform.scale(bg, res)
        self.main_screen.blit(bg, (0,0))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
    
    def draw(self):
        self.show_background('game_bg.png')
        self.pt.draw()
        for i in range(self.length):
            self.main_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def walk(self):

        for j in range((self.length-1), 0, -1):
            self.x[j] = self.x[j-1]
            self.y[j] = self.y[j-1]

        if self.direction == 'up':
            self.y[0] -= SIZE

        if self.direction == 'down':
            self.y[0] += SIZE
            
        if self.direction == 'left':
            self.x[0] -= SIZE
            
        if self.direction == 'right':
            self.x[0] += SIZE
    
        self.draw()

####################   GAME CLASS   #################################

# Contains all features of the game
class Game:
    def __init__(self):
        pygame.init() # Start pygame
        pygame.mixer.init()
        
        # Game setup: background, snake, points
        self.surface = pygame.display.set_mode(res) # Resolution of screen and main surface to draw on
        self.surface.fill(bg_color)
        self.apple = Point(self.surface)
        self.snake = Snake(self.surface, 4, self.apple)

    # Starting of the game
    def start(self):
        run = True # To pause or end
        while run:
            self.show_background('start_bg.jpg') # Show the start screen ###

            # To start the game from start screen
            for event in pygame.event.get():
                if event.type == KEYDOWN: # Key is pressed
                    # Pressing 'esc' to exit
                    if event.key == K_ESCAPE:
                        run = False # Exits loop
                        
                    # START
                    if event.key == K_SPACE:
                        self.show_background('game_bg.png') #Changing Background to game
                        self.play_bg_music('bg_music_1.mp3', 1) # Start of music. 1 -> Play
                        self.run() # Running of the game
                
                # Pressing the cross mark on screen
                elif (event.type == QUIT):
                    run = False        

    def show_score(self):
        font1 = pygame.font.SysFont('ariel', 30, True, False)
        score = font1.render(f'SCORE: {self.snake.length - 4}', True, (0, 0, 0))
        self.surface.blit(score, (15, 15))
        pygame.display.flip()

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.show_score()

        if self.collide(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound('point.ogg')
            self.apple.move()
            self.snake.increase_length()

        for i in range(3, self.snake.length):
            if self.collide(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('gameover.ogg')
                raise "Game Over"

    def play_sound(self, name):
        music = pygame.mixer.Sound(name)
        pygame.mixer.Sound.play(music)

    def collide(self, x1, y1, x2, y2):
        if (x1 >= x2-5 and x1 <= x2+SIZE-5):
            if (y1 >= y2-5 and y1 <= y2+SIZE-5):
                return True

        return False

    def show_background(self, bg_p):
        bg = pygame.image.load(bg_p)
        bg = pygame.transform.scale(bg, res)
        self.surface.blit(bg, (0,0))
        pygame.display.flip()

    def gameover(self):
        self.surface.fill(bg_color)
        font1 = pygame.font.SysFont('ariel', 30,False, False)
        font2 = pygame.font.SysFont('times new roman', 70,False, False)
        line1 = font2.render('GAME OVER', True, (21, 140, 237))
        line2 = font1.render(f'SCORE: {self.snake.length - 4}', True, (21, 140, 237))
        line3 = font1.render('Press ENTER to Restart, ESCAPE to Return', True, (21, 140, 237))
        self.surface.blit(line1, (310, 200))
        self.surface.blit(line2, (460, 300))
        self.surface.blit(line3, (300, 350))
        pygame.display.flip()

    def reset(self):
        self.snake.length = 4
        self.snake.x = [SIZE]*self.snake.length
        self.snake.y = [SIZE]*self.snake.length
        self.snake.direction = 'right'
        self.snake.walk()
        self.apple.move()  

    def play_bg_music(self, name, cmd):
        music = pygame.mixer.music.load(name)
        if cmd == 1:
            pygame.mixer.music.play()
        if cmd == 0:
            pygame.mixer.music.pause()

    # Running of the game
    def run(self):
        pygame.init()
        pause = False # To pause the game
        running = True # To RUN the game

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False
                        self.reset()

                    if not pause:
                        if event.key == K_UP or event.key == K_w:
                            self.snake.move_up()

                        if event.key == K_DOWN or event.key == K_s:
                            self.snake.move_down()

                        if event.key == K_LEFT or event.key == K_a:
                            self.snake.move_left()

                        if event.key == K_RIGHT or event.key == K_d:
                            self.snake.move_right()

                elif (event.type == QUIT):
                    pygame.quit()
                    exit()
            
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.play_bg_music('bg_music_1.mp3', 0)
                self.gameover()
                pause = True
            time.sleep(0.2)

if __name__ == "__main__":
    game = Game() # Create the game
    game.start() # Start the game
