s_width = 1200
s_height = 1000
block_size = 30
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
grid_x, grid_y = 10, 20


def draw_text_middle(pygame, surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    top_left_x = (s_width - play_width) // 2
    top_left_y = (s_height - play_height) // 2
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2),
                         top_left_y + play_height / 2 - label.get_height() / 2))


def draw_next_shape(pygame, shape, surface):
    sx = 350
    sy = 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    temp_size = block_size // 2

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j * temp_size,
                                                        sy + i * temp_size, temp_size, temp_size), 0)


def draw_block(pygame, surface, grid, is_partner=False):
    sx, sy = 150, 200
    if is_partner:
        sx, sy = 2, 2

    for i in range(grid_y):
        for j in range(grid_x):
            pygame.draw.rect(surface, grid[i][j],
                             (sx + j * block_size, sy + i * block_size, block_size, block_size), 0)


def draw_grid(pygame, surface, is_partner=False):
    sx, sy = 150, 200
    if is_partner:
        sx, sy = 2, 2

    edge = 4
    ed = edge // 2

    for i in range(1, grid_y):
        pygame.draw.line(surface, (128, 128, 128),
                         (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
        for j in range(1, grid_x):
            pygame.draw.line(surface, (128, 128, 128),
                             (sx + j * block_size, sy), (sx + j * block_size, sy + play_height))

    pygame.draw.rect(surface, (196, 196, 196),
                     (sx - ed, sy - ed, play_width + edge, play_height + edge), edge)


def draw_texts(pygame, screen, my_score=0, partner_score=0):
    font1 = pygame.font.SysFont('comicsans', 40)
    font2 = pygame.font.SysFont('comicsans', 20)

    label1 = font1.render('Me', 1, (255, 255, 255))
    screen.blit(label1, (300 - label1.get_width() / 2, 850))

    label2 = font2.render('Next', 1, (255, 255, 255))
    screen.blit(label2, (400 - label2.get_width() / 2, 50))

    label3 = font2.render('Score', 1, (255, 255, 255))
    screen.blit(label3, (180, 50))

    label4 = font1.render(f'{my_score}', 1, (255, 255, 255))
    screen.blit(label4, (180, 100))

    label1_2 = font1.render(f'Partner', 1, (196, 196, 196))
    screen.blit(label1_2, (900 - label1_2.get_width() / 2, 850))

    label3_2 = font2.render('Score', 1, (196, 196, 196))
    screen.blit(label3_2, (900 - label3_2.get_width() / 2, 50))

    label4_2 = font1.render(f'{partner_score}', 1, (196, 196, 196))
    screen.blit(label4_2, (900 - label4_2.get_width() / 2, 100))
