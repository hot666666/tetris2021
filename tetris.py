import time
import pygame

from draw import *
from game import *
from file import *
from network import *


def main(win):
    global grid, pgrid
    global score, pscore
    global mrun, prun
    # last_score = max_score() # load max score

    locked_positions = {}
    grid = create_grid(locked_positions)
    pgrid = create_grid(locked_positions)

    change_piece = False
    run = True  # two players running
    prun = mrun = True  # Partner,Me run state

    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()

    fall_speed = 0.27
    fall_time = 0
    level_time = 0
    score = pscore = 0

    left_surface = pygame.Surface((600, 1000))
    right_surface = pygame.Surface((600, 1000))
    right_inner_surface = pygame.Surface((304, 604))

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        if fall_time / 1000 > fall_speed:
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

        if change_piece and mrun:
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
        draw_block(pygame, right_inner_surface, pgrid, is_partner=True)
        draw_grid(pygame, right_inner_surface, is_partner=True)
        right_inner_surface.set_alpha(64)
        right_surface.blit(right_inner_surface, (150 - 2, 200 - 2))
        win.blit(right_surface, (600, 0))

        draw_texts(pygame, win, score, pscore)
        pygame.display.flip()

        if mrun and check_lost(locked_positions):
            mrun = False
        if not mrun and not prun:
            break

    msg = "You lost!" if pscore > score else "You won!"
    draw_text_middle(pygame, win, msg, 80, (255, 255, 255))
    pygame.display.update()
    time.sleep(3)

    update_score(score)


def threaded_func(conn):
    global grid, pgrid
    global score, pscore
    global mrun, prun

    while True:
        time.sleep(0.15)
        conn.send([score, grid, mrun, prun])
        received_data = conn.recv()
        pscore, pgrid, prun, _ = received_data
        if not mrun and not prun:
            break
    conn.close()


def main_menu(win):
    run = True

    pygame.display.set_caption('Tetris')
    pygame.font.init()

    # Create custom socket connection
    try:
        conn = MySocket()
    except ConnectionRefusedError as e:
        print(e)
        return

    win.fill((0, 0, 0))
    draw_text_middle(pygame, win, 'Waiting for other player...',
                     60, (255, 255, 255))
    pygame.display.update()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        data = conn.client.recv(16)  # pickle없이 그냥처리
        if not data:
            continue
        if data == b"start":
            win.fill((0, 0, 0))
            draw_text_middle(pygame, win, 'Game starts in 3secs...',
                             60, (255, 255, 255))
            pygame.display.update()
            time.sleep(3)
            start_new_thread(threaded_func, (conn,))
            main(win)
            break

    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
main_menu(win)
