from pickle import TRUE
from random import random
from enum import Enum
from collections import namedtuple
import random
from select import select
from tkinter import W, Widget
import pygame
from pygame.locals import *

pygame.init()

# * Variables
WIDTH = 500
HEIGHT = 500
BLOCK_SIZE = 20

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREEN_DARKER = (28, 199, 16)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FONT = pygame.font.Font('freesansbold.ttf', 32)

# Assets
FRUIT_IMG = pygame.image.load('./Graphics/apple.png')
FRUIT_IMG = pygame.transform.scale(FRUIT_IMG, (BLOCK_SIZE, BLOCK_SIZE))


pygame.display.set_caption("Snake Game!")
CLOCK = pygame.time.Clock()
surface = pygame.display.set_mode((WIDTH, HEIGHT))

def draw_grid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        for y in range(0, HEIGHT, BLOCK_SIZE):
            rect = Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(surface, WHITE, rect, 1)

Positions = namedtuple("Positions" , 'x, y')
class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT= 4
 
class Snake(object):
    def __init__(self):
        x = random.randrange(0, WIDTH, BLOCK_SIZE)
        y = random.randrange(0, HEIGHT, BLOCK_SIZE)

        # Snake Variables
        self.head = Positions(x, y)
        self.snake = [self.head]
        self.direction = Direction.RIGHT
        # Fruit
        self.fruit = None
        self._place_food()

        # Game Status
        self.game_over = False
        self.score = 0
    
    def _update_direction(self, key_pressed):
        if key_pressed in [K_w, K_UP] and self.direction != Direction.DOWN:
                self.direction = Direction.UP
        if key_pressed in [K_s, K_DOWN] and self.direction != Direction.UP:
            self.direction = Direction.DOWN
        if key_pressed in [K_a, K_LEFT] and self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        if key_pressed in [K_d, K_RIGHT] and self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT

    def _move(self):
        x = self.head.x
        y = self.head.y

        if self.direction == Direction.UP:
            y -= BLOCK_SIZE
        if self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        if self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        
        self.head = Positions(x, y)
    
    def _collision(self):
        #* Detects if hit the fruit
        if self.head.x == self.fruit.x and self.head.y == self.fruit.y:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        #* Collision with body 
        if self.head in self.snake[1:]:
            self.game_over = True
        
        #* Collision with wall
        if self.head.x not in range(-BLOCK_SIZE, WIDTH+BLOCK_SIZE):
            self.game_over = True
        if self.head.y not in range(-BLOCK_SIZE, HEIGHT+BLOCK_SIZE):
            self.game_over = True

    def _place_food(self):
        x = random.randrange(0, WIDTH, BLOCK_SIZE)
        y = random.randrange(0, HEIGHT, BLOCK_SIZE)
        self.fruit = Positions(x, y)
        if self.fruit in self.snake:
            self._place_food()

    def _update_ui(self):
        surface.fill(GREEN_DARKER)

        # Update Score label 
        score_label = FONT.render(f"Score: {self.score}", TRUE, WHITE)
        surface.blit(score_label, [0, 0])

        # Draw Snake
        for pt in self.snake:
            rect_snake = Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(surface, RED, rect_snake)
        
        # Draw Fruit
        rect_fruit = Rect(self.fruit.x, self.fruit.y, BLOCK_SIZE, BLOCK_SIZE)
        surface.blit(FRUIT_IMG, rect_fruit)
        #pygame.draw.rect(surface, GREEN, rect_fruit)

        CLOCK.tick(15)
        pygame.display.flip()

    def play_step(self):
        #* Get User Input.
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit()
            elif event.type == KEYDOWN:
                self._update_direction(event.key)

        #* Movement
        self._move()
        self.snake.insert(0, self.head) # Update the head position

        #* Detect Collisions
        self._collision()

        #* Update UI
        self._update_ui()

        if self.game_over:
            game_over_label = FONT.render(f"GAME OVER!! Score: {self.score}", TRUE, WHITE)
            surface.blit(game_over_label, (WIDTH/2 -game_over_label.get_width()/2,
                                           HEIGHT/2 - game_over_label.get_height()/2))
            pygame.display.update()
            pygame.time.delay(3_000)

        
        #* Return GameOver and Score
        return self.game_over, self.score
        

if __name__ == "__main__":
    snake = Snake()

    running = True
    while running:
        game_over, score = snake.play_step()
        if game_over:
            print("GAME OVER")
            snake = Snake()
    
    pygame.quit()