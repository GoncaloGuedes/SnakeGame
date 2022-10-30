from calendar import leapdays
from email.quoprimime import body_check
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
GREEN_DARKER = (175, 215, 70)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FONT = pygame.font.Font('freesansbold.ttf', 32)

# Assets
FRUIT_IMG = pygame.image.load('./Graphics/apple.png')
FRUIT_IMG = pygame.transform.scale(FRUIT_IMG, (BLOCK_SIZE, BLOCK_SIZE))

# Heads
HEAD_RIGHT = pygame.image.load('./Graphics/head_right.png')
HEAD_RIGHT = pygame.transform.scale(HEAD_RIGHT, (BLOCK_SIZE, BLOCK_SIZE))
HEAD_LEFT = pygame.image.load('./Graphics/head_left.png')
HEAD_LEFT= pygame.transform.scale(HEAD_LEFT, (BLOCK_SIZE, BLOCK_SIZE))
HEAD_UP = pygame.image.load('./Graphics/head_up.png')
HEAD_UP= pygame.transform.scale(HEAD_UP, (BLOCK_SIZE, BLOCK_SIZE))
HEAD_DOWN = pygame.image.load('./Graphics/head_down.png')
HEAD_DOWN= pygame.transform.scale(HEAD_DOWN, (BLOCK_SIZE, BLOCK_SIZE))

# Bodies 
BODY_BOTTOM_LEFT = pygame.image.load('./Graphics/body_bottomleft.png')
BODY_BOTTOM_LEFT = pygame.transform.scale(BODY_BOTTOM_LEFT, (BLOCK_SIZE, BLOCK_SIZE))
BODY_BOTTOM_RIGHT = pygame.image.load('./Graphics/body_bottomright.png')
BODY_BOTTOM_RIGHT = pygame.transform.scale(BODY_BOTTOM_RIGHT, (BLOCK_SIZE, BLOCK_SIZE))

BODY_TOP_LEFT = pygame.image.load('./Graphics/body_topleft.png')
BODY_TOP_LEFT = pygame.transform.scale(BODY_TOP_LEFT, (BLOCK_SIZE, BLOCK_SIZE))
BODY_TOP_RIGHT = pygame.image.load('./Graphics/body_topright.png')
BODY_TOP_RIGHT = pygame.transform.scale(BODY_TOP_RIGHT, (BLOCK_SIZE, BLOCK_SIZE))

BODY_HORIZONTAL = pygame.image.load('./Graphics/body_horizontal.png')
BODY_HORIZONTAL = pygame.transform.scale(BODY_HORIZONTAL, (BLOCK_SIZE, BLOCK_SIZE))
BODY_VERTICAL = pygame.image.load('./Graphics/body_vertical.png')
BODY_VERTICAL = pygame.transform.scale(BODY_VERTICAL, (BLOCK_SIZE, BLOCK_SIZE))

# Tails
TAIL_RIGHT = pygame.image.load('./Graphics/tail_right.png')
TAIL_RIGHT = pygame.transform.scale(TAIL_RIGHT, (BLOCK_SIZE, BLOCK_SIZE))
TAIL_LEFT = pygame.image.load('./Graphics/tail_left.png')
TAIL_LEFT= pygame.transform.scale(TAIL_LEFT, (BLOCK_SIZE, BLOCK_SIZE))
TAIL_UP = pygame.image.load('./Graphics/tail_up.png')
TAIL_UP= pygame.transform.scale(TAIL_UP, (BLOCK_SIZE, BLOCK_SIZE))
TAIL_DOWN = pygame.image.load('./Graphics/tail_down.png')
TAIL_DOWN= pygame.transform.scale(TAIL_DOWN, (BLOCK_SIZE, BLOCK_SIZE))


pygame.display.set_caption("Snake Game!")
CLOCK = pygame.time.Clock()
surface = pygame.display.set_mode((WIDTH, HEIGHT))

def draw_grid():
    for i_x, x in enumerate(range(0, WIDTH, BLOCK_SIZE)):
        if i_x%2 ==0:
            for i_y, y in enumerate(range(0, HEIGHT, BLOCK_SIZE)):
                if i_y%2 ==0:
                    rect = Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(surface, (167, 209, 61), rect)

Positions = namedtuple("Positions" , 'x, y')
BodyOrientation = namedtuple("BodyOrientation", 'x, y')
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
        self.fruit = Positions(0, 0)
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
        if self.head.x > WIDTH or self.head.x <0:
            self.game_over = True
        if self.head.y > WIDTH or self.head.y <0:
            self.game_over = True

    def _place_food(self):
        x = random.randrange(0, WIDTH, BLOCK_SIZE)
        y = random.randrange(0, HEIGHT, BLOCK_SIZE)
        self.fruit = Positions(x, y)
        if self.fruit in self.snake:
            self._place_food()

    def _draw_snake(self):
        
        HEAD_IMAGES = {
            Direction.RIGHT: HEAD_RIGHT,
            Direction.LEFT: HEAD_LEFT,
            Direction.UP: HEAD_UP,
            Direction.DOWN: HEAD_DOWN
        }

        TAIL_IMAGES = {
            (0, -1): TAIL_UP,
            (0, 1): TAIL_DOWN,
            (-1, 0): TAIL_LEFT,
            (1, 0): TAIL_RIGHT
        }


        for index, pt in enumerate(self.snake):
            rect_snake = Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE)
            if index == 0: # Add Head
                surface.blit(HEAD_IMAGES[self.direction], rect_snake)

            elif index == len(self.snake)-1: # Add tail
                vector = ((pt.x-self.snake[index-1].x)// BLOCK_SIZE,
                          (pt.y-self.snake[index-1].y)//BLOCK_SIZE)
                surface.blit(TAIL_IMAGES[vector], rect_snake)
            else: # add Body
                previous_block = self.snake[index+1]
                previous_block_x  = (previous_block.x - pt.x)// BLOCK_SIZE
                previous_block_y = (previous_block.y - pt.y) // BLOCK_SIZE
                
                next_block = self.snake[index -1]
                next_block_x = (next_block.x - pt.x) // BLOCK_SIZE
                next_block_y = (next_block.y - pt.y) // BLOCK_SIZE

                if previous_block.x == next_block.x:
                    surface.blit(BODY_VERTICAL, rect_snake)

                elif previous_block.y == next_block.y:
                    surface.blit(BODY_HORIZONTAL, rect_snake)

                else: 
                    body_part = BODY_TOP_LEFT
                    if previous_block_x == -1 and next_block_y == -1 or previous_block_y == -1 and next_block_x == -1:
                        body_part = BODY_TOP_LEFT
                    if previous_block_x == -1 and next_block_y == 1 or previous_block_y == 1 and next_block_x == -1:
                        body_part = BODY_BOTTOM_LEFT
                    if previous_block_x == 1 and next_block_y == -1 or previous_block_y == -1 and next_block_x == 1:
                        body_part = BODY_TOP_RIGHT
                    if previous_block_x == 1 and next_block_y == 1 or previous_block_y == 1 and next_block_x == 1:
                        body_part = BODY_BOTTOM_RIGHT
                
                    surface.blit(body_part, rect_snake)

    def _update_ui(self):
        surface.fill(GREEN_DARKER)
        draw_grid()

        # Update Score label 
        score_label = FONT.render(f"Score: {self.score}", True, WHITE)
        surface.blit(score_label, [0, 0])

        # Draw Snake
        self._draw_snake()
        
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
            game_over_label = FONT.render(f"GAME OVER!! Score: {self.score}", True, WHITE)
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