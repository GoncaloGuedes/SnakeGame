from socketserver import DatagramRequestHandler
from tarfile import BLOCKSIZE
import pygame
import random

pygame.init()


# Variables 
WIDTH = 600
HEIGHT = 400
BLOCKSIZE = 20 #Set the size of the grid block
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)

# Setup Game
pygame.display.set_caption("SnakeGame!")
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))



def spawn_fruit():
    COLOR = (255, 0, 0)
    x = random.randrange(0, WIDTH, BLOCKSIZE)
    y = random.randrange(0, HEIGHT, BLOCKSIZE)

    #! Não pode dar spawn em cima do corpo da cobra

    fruit = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
    pygame.draw.rect(WINDOW, COLOR, fruit)
        

def drawGrid(): 
    for x in range(0, WIDTH, BLOCKSIZE):
        for y in range(0, HEIGHT, BLOCKSIZE):
            rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
            pygame.draw.rect(WINDOW, WHITE, rect, 1)
    

def main():
    CLOCK = pygame.time.Clock()
    running = True
    while running:
        drawGrid()
        spawn_fruit()

        # Se a cabeça da cobra está na mesma posição que a fruta, a posição da fruta atualiza
        # Se a cabeça toda na cobra, acaba
        # Se a cabeça toda na parede, acaba
        # Se come uma fruta, aumneta 1 bloco de tamanho e aumenta a velocidade
        # Atualiza o Score
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()