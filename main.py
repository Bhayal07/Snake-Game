import pygame
from pygame import KEYDOWN
from pygame.examples.grid import Game
from pygame.locals import *
import time
import random

SIZE=40
class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 800))  # Initialize display
        self.BACKGROUND_COLOR = pygame.image.load("background.jpg").convert()  # Load background
        self.snake = Snake(self.surface, 1, self.BACKGROUND_COLOR)
        self.snake.draw()
        self.apple=Apple(self.surface)
        self.apple.draw()

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length - 1}", True, (255, 255, 255))  # Subtract initial length
        self.surface.blit(score, (500, 0))

    def play(self):
        self.surface.blit(self.BACKGROUND_COLOR, (0, 0))  # Draw background here
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        #  snake coliding with apple
        for i in range(self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
                self.snake.increase_length()
                self.apple.move()  # Move apple to a new location
                self.apple.draw()

        # snake coliding with itself
        for i in range(1,self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise Exception("Game Over!")

        # Snake colliding with the border
        if (self.snake.x[0] < 0 or self.snake.x[0] >= 1000 or self.snake.y[0] < 0 or self.snake.y[0] >= 800):
            raise Exception("Game Over!")

    def is_collision(self, x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:  # Exact match of positions
            return True
        return False

    def reset(self):
        self.snake = Snake(self.surface, 1, self.BACKGROUND_COLOR)  # Pass background
        self.apple=Apple(self.surface)

    def show_game_over(self):
        self.surface.blit(self.BACKGROUND_COLOR, (0, 0))  # Draw background
        font = pygame.font.SysFont('arial', 30)

        line1 = font.render("Game Over!", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))  # First line at y=300

        #Display Final Score
        final_score = font.render(f"Final Score: {self.snake.length - 1}", True, (255, 255, 255))
        self.surface.blit(final_score, (200, 350))

        line2 = font.render("Press Enter to continue", True, (255, 255, 255))
        self.surface.blit(line2, (200, 400))  # Second line moved to y=350

        pygame.display.flip()

    def run(self):
        running = True
        pause=False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause=False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause=True
                self.reset()

            time.sleep(0.2)

class Snake:
    def __init__(self,parent_screen,length,background):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("block.jpg").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'right'
        self.length = length
        self.background = background


    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self,):
        self.parent_screen.blit(self.background, (0, 0))  # Use stored background

        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
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
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        elif self.direction == 'right':
            self.x[0] += SIZE
        elif self.direction == 'up':
            self.y[0] -= SIZE
        elif self.direction == 'down':
            self.y[0] += SIZE
        self.draw()

class Apple:
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("apple.jpg").convert()
        self.x = SIZE*3
        self.y = SIZE*3

    def move(self):
        max_x = (500 // SIZE) - 1  # Max horizontal grid position
        max_y = (500 // SIZE) - 1  # Max vertical grid position

        self.x = random.randint(0, max_x) * SIZE
        self.y = random.randint(0, max_y) * SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()




