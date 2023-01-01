import pygame

from draw import *
from game import *
from file import *


def main(win):
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    left_surface = pygame.Surface((600, 1000))
    right_surface = pygame.Surface((600, 1000))
    right_inner_surface = pygame.Surface((304, 604))

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        left_surface.fill((0, 0, 0))
        draw_next_shape(pygame, next_piece, left_surface)
        draw_block(pygame, left_surface, grid)
        draw_grid(pygame, left_surface)
        left_surface.set_alpha(255)
        win.blit(left_surface, (0, 0))

        right_surface.fill((0, 0, 0))
        draw_block(pygame, right_inner_surface, grid, is_partner=True)
        draw_grid(pygame, right_inner_surface, is_partner=True)
        right_inner_surface.set_alpha(64)
        right_surface.blit(right_inner_surface, (150-2, 200-2))
        win.blit(right_surface, (600, 0))

        draw_texts(pygame, win, score, last_score)
        pygame.display.flip()

        if check_lost(locked_positions):
            draw_text_middle(pygame, win, "YOU LOST!", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)


def main_menu(win):
    run = True

    pygame.display.set_caption('Tetris')
    pygame.font.init()

    while run:
        win.fill((0, 0, 0))
        draw_text_middle(pygame, win, 'Press Any Key To Play',
                         60, (255, 255, 255))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()


# wndow size
s_width = 1200
s_height = 1000

win = pygame.display.set_mode((s_width, s_height))
main_menu(win)
