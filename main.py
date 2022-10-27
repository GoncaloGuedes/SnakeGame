from random import random
import random
import pygame
from pygame.locals import *

pygame.init()

# * Variables
WIDTH = 500
HEIGHT = 500
BLOCK_SIZE = 20
RED = (255, 0, 0)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.display.set_caption("Snake Game!")
surface = pygame.display.set_mode((WIDTH, HEIGHT))
surface.fill(BLACK)


def draw_grid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        for y in range(0, HEIGHT, BLOCK_SIZE):
            rect = Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(surface, WHITE, rect, 1)

def spawn_fruit():
    x = random.randrange(0, WIDTH, BLOCK_SIZE)
    y = random.randrange(0, HEIGHT, BLOCK_SIZE)
    fruit = Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(surface, RED, fruit) 
 
class Snake(object):
    def __init__(self):
        x = random.randrange(0, WIDTH, BLOCK_SIZE)
        y = random.randrange(0, HEIGHT, BLOCK_SIZE)
        self.rect = pygame.rect.Rect((x, y, BLOCK_SIZE, BLOCK_SIZE))
        self.direction = "UP"

    def handle_keys(self, event):
        if event.key == K_w:
            self.direction = "UP"
        elif event.key == K_s:
            self.direction = "DOWN"
        elif event.key == K_a: 
            self.direction = "LEFT"
        elif event.key == K_d: 
            self.direction = "RIGHT"
    
    def movement(self):
        if self.direction == "UP":
            self.rect.move_ip(0, -BLOCK_SIZE)
        elif self.direction == "DOWN":
            self.rect.move_ip(0, BLOCK_SIZE)
        elif self.direction == "LEFT":
            self.rect.move_ip(-BLOCK_SIZE, 0)
        elif self.direction == "RIGHT":
            self.rect.move_ip(BLOCK_SIZE, 0)
            
    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 128), self.rect)

if __name__ == "__main__":
    snake = Snake()
    CLOCK = pygame.time.Clock()

    running = True
    while running:
        snake.movement()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                break
            elif event.type == KEYDOWN:
                snake.handle_keys(event)

        surface.fill(GRAY)
        draw_grid()
        snake.draw(surface)
        pygame.display.update()

        CLOCK.tick(10)
    pygame.quit()