import pygame

from tetris.shapes import *
import random

block_size = 30
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
grid_x, grid_y = 10, 20

grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]  # RGB row col
grid[10][5] = (0, 255, 0)
grid[11][5] = (0, 255, 0)
grid[12][5] = (0, 255, 0)
grid[13][5] = (0, 255, 0)


shape = Piece(5, 0, random.choice(shapes))


def draw_next_shape(surface):
    sx = 350
    sy = 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    temp_size = block_size//2

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*temp_size,
                                 sy + i*temp_size, temp_size, temp_size), 0)


def draw_block(surface, is_partner=False):
    sx, sy = 150, 200
    if is_partner:
        sx, sy = 2, 2

    for i in range(grid_y):
        for j in range(grid_x):
            pygame.draw.rect(surface, grid[i][j],
                             (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)


def draw_grid(surface, is_partner=False):
    sx, sy = 150, 200
    if is_partner:
        sx, sy = 2, 2

    edge = 4
    ed = edge//2

    for i in range(1, grid_y):
        pygame.draw.line(surface, (128, 128, 128),
                         (sx, sy + i*block_size), (sx+play_width, sy + i*block_size))
        for j in range(1, grid_x):
            pygame.draw.line(surface, (128, 128, 128),
                             (sx + j * block_size, sy), (sx + j*block_size, sy + play_height))

    pygame.draw.rect(surface, (196, 196, 196),
                     (sx-ed, sy-ed, play_width+edge, play_height+edge), edge)


def draw_texts(screen, my_score=0, partner_score=0):
    font1 = pygame.font.SysFont('comicsans', 40)
    font2 = pygame.font.SysFont('comicsans', 20)

    label1 = font1.render('Me', 1, (255, 255, 255))
    screen.blit(label1, (300-label1.get_width() / 2, 850))

    label2 = font2.render('Next', 1, (255, 255, 255))
    screen.blit(label2, (400-label2.get_width()/2, 50))

    label3 = font2.render('Score', 1, (255, 255, 255))
    screen.blit(label3, (180, 50))

    label4 = font1.render(f'{my_score}', 1, (255, 255, 255))
    screen.blit(label4, (180, 100))

    label1_2 = font1.render(f'Partner', 1, (196, 196, 196))
    screen.blit(label1_2, (900-label1_2.get_width()/2, 850))

    label3_2 = font2.render('Score', 1, (196, 196, 196))
    screen.blit(label3_2, (900-label3_2.get_width()/2, 50))

    label4_2 = font1.render(f'{partner_score}', 1, (196, 196, 196))
    screen.blit(label4_2, (900-label4_2.get_width()/2, 100))


# Initialize Pygame
pygame.init()
pygame.font.init()

# Set the window size and title
screen = pygame.display.set_mode((1200, 1000))
pygame.display.set_caption("TEST")

# Set the background color to white
screen.fill((0, 0, 0))

# Create a surface for the left rectangle
left_rect_surface = pygame.Surface((600, 1000))


draw_next_shape(left_rect_surface)
draw_block(left_rect_surface)
draw_grid(left_rect_surface)

left_rect_surface.set_alpha(255)
screen.blit(left_rect_surface, (0, 0))

# Create a surface for the right rectangle
right_rect_surface = pygame.Surface((600, 1000))

# Fill the right rectangle surface with a solid color
right_rect_surface.fill((0, 0, 0))

right_rect_inner_surface = pygame.Surface((304, 604))
draw_block(right_rect_inner_surface, is_partner=True)
draw_grid(right_rect_inner_surface, is_partner=True)
right_rect_inner_surface.set_alpha(64)
right_rect_surface.blit(right_rect_inner_surface, (150-2, 200-2))

# Draw the right rectangle on the screen
screen.blit(right_rect_surface, (600, 0))

draw_texts(screen)

# Update the display
pygame.display.flip()

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()
