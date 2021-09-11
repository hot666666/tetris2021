import pygame
import random
import sys
import copy
import threading
from collections import deque




BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

INVISABLE_BOARD = 2
DISPLAY_SIZE = (600, 800)
PAD_SIZE = (400, 800)
BLOCK_SIZE = 40
BOARD_ROW = 20 + INVISABLE_BOARD
BOARD_COL = 10

ONE_LINE_SCORE = 200
ONE_BLOCK_SCORE = 10

SEC = 1

TYPES = [  # index 0~6
    [[0, 0], [0, 1], [0, 2], [0, 3]],  # 직선
    [[0, 0], [0, 1], [1, 0], [1, 1]],  # 정사각형
    [[0, 0], [0, 1], [0, 2], [1, 0]],  # 3-1 왼쪽아래
    [[0, 0], [0, 1], [1, 1], [1, 2]],  # 2-2 왼쪽위
    [[0, 0], [0, 1], [0, 2], [1, 2]],  # ㅗ
    [[0, 0], [1, 0], [1, 1], [1, 2]],  # 1-3 왼쪽위
    [[0, 1], [0, 2], [1, 0], [1, 1]]   # 2-2 오른쪽위
]




class Blocks:
    def __init__(self):
        self.types = deque()
        for _ in range(3):
            self.types.append(copy.deepcopy(TYPES[random.randint(0, 6)]))

    def popBlock(self):
        self.types.append(copy.deepcopy(TYPES[random.randint(0, 6)]))
        return self.types.popleft()


class Block:
    def __init__(self, state):
        self.row = 0
        self.col = int(BOARD_COL * 0.5)
        self.states = state

    def minmaxRow(self):
        temp = [row[0] + self.row for row in self.states]
        return min(temp), max(temp)


class Board:
    def __init__(self):
        self.states = [[0] * 10 for _ in range(20+INVISABLE_BOARD)]
        self.index = [False] * (20 + INVISABLE_BOARD)
        self.score = 0

    def checkIsFull(self, row):
        if self.states[row] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]:
            return True
        return False

    def checkRows(self, movingBlock):
        minRow, maxRow = movingBlock.minmaxRow()
        cnt = 0
        for r in range(maxRow, minRow - 1, -1):
            if self.checkIsFull(r):
                self.states.pop(r)
                cnt += 1
        for _ in range(cnt):
            self.states.insert(0, [0] * 10)
        self.score += cnt * ONE_LINE_SCORE




def set_interval(func, sec):  # import threading
    def func_wrapper():
        set_interval(func, sec)
        func()

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def setBoard():
    for rc in movingBlock.states:
        Board.states[rc[0] + movingBlock.row][rc[1] + movingBlock.col] = 1
        Board.index[rc[0] + movingBlock.row] = True # 여기 보드에서 손봐줘야함


def drawObject(col, row, type):
    pygame.draw.rect(GamePad, type,
                     pygame.Rect((col * BLOCK_SIZE + 2, row * BLOCK_SIZE + 2), (BLOCK_SIZE - 2, BLOCK_SIZE - 2)))


def drawBlockOnBoard(color=GREEN):
    for idx, state in enumerate(Board.index):
        if state:
            for col in range(0, BOARD_COL):
                if Board.states[idx][col] == 1:
                    drawObject(col, idx - INVISABLE_BOARD, color)

def drawMovingBlock(colorType, temp=0):  # temp는 낙하지점을 더한 row값
    for y, x in movingBlock.states:
        tx, ty = x + movingBlock.col, y + movingBlock.row + temp
        drawObject(tx, ty - INVISABLE_BOARD, colorType)

def drawMessage(text, XY,size=20,color=BLACK):
    global GamePad

    textfont = pygame.font.Font('freesansbold.ttf', size)
    text = textfont.render(text, True, color)
    textpos = text.get_rect()
    textpos.center = XY
    GamePad.blit(text, textpos)
    pygame.display.update()

def drawQObject(col, row, type):
    pygame.draw.rect(GamePad, type,
                     pygame.Rect((col * 20 + 480, row * 20 + 200), (20-2 , 20-2)))

def drawQueueBlock(colorType):
    t = 0
    for q in Q.types:
        for y,x in q:
            drawQObject(x, y+t, colorType)
        t += 5

def drawBoard():
    for i in range(0, PAD_SIZE[0] + 1, 40):
        pygame.draw.line(GamePad, BLACK, (i, 0), (i, PAD_SIZE[1]), 2)
        pygame.draw.line(GamePad, BLACK, (0, i), (PAD_SIZE[0], i), 2)
        pygame.draw.line(GamePad, BLACK, (0, PAD_SIZE[0] + i), (PAD_SIZE[0], PAD_SIZE[0] + i), 2)

def checkInBoard():
    for block in movingBlock.states:
        row = block[0] + movingBlock.row
        col = block[1] + movingBlock.col
        if not (-1 < row < BOARD_ROW and -1 < col < BOARD_COL):
            return False
        if Board.states[row][col] == 1:
            return False
    return True

def checkMovable():
    for block in movingBlock.states:
        row = block[0] + movingBlock.row + 1
        col = block[1] + movingBlock.col
        if row >= BOARD_ROW or Board.states[row][col] == 1:
            return False
    return True

def checkFallable(temp):
    for block in movingBlock.states:
        row = block[0] + temp
        col = block[1] + movingBlock.col
        if row >= BOARD_ROW or Board.states[row][col] == 1:
            return False
    return True


def down():  # 현재 블럭이 착지될 것인가.
    global movingBlock, Q

    movingBlock.row += 1
    if not checkInBoard():
        Board.score += ONE_BLOCK_SCORE
        movingBlock.row -= 1
        setBoard()
        Board.checkRows(movingBlock)
        movingBlock = Block(Q.popBlock())

def fall():
    temp = movingBlock.row
    while checkFallable(temp + 1):
        temp += 1
    return temp

def rotate():
    maxRow = 0
    for rc in movingBlock.states:
        if (rc[0] > maxRow):
            maxRow = rc[0]
        rc[0], rc[1] = rc[1], -rc[0]
    for rc in movingBlock.states:
        rc[1] += maxRow




def runGame():
    global GamePad, BLOCK, Clock
    global Board, movingBlock, Q


    while True:
        maxRow = fall()
        if not maxRow:
            break

        GamePad.fill(WHITE)
        drawBoard()
        drawBlockOnBoard()
        drawMovingBlock(YELLOW, maxRow - movingBlock.row)
        drawMovingBlock(GREEN)
        drawQueueBlock(GREEN)
        drawMessage(f'SCORE: {Board.score} ',(500,100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()  # theading 종료도 해줘야 꺼질듯

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    movingBlock.col -= 1
                    if not checkInBoard():
                        movingBlock.col += 1
                if event.key == pygame.K_RIGHT:
                    movingBlock.col += 1
                    if not checkInBoard():
                        movingBlock.col -= 1
                if event.key == pygame.K_UP:
                    temp = copy.deepcopy(movingBlock.states)
                    rotate()
                    if not checkInBoard():
                        movingBlock.states = temp
                if event.key == pygame.K_DOWN:
                    movingBlock.row += 1
                    if not checkInBoard():
                        movingBlock.row -= 1
                if event.key == pygame.K_SPACE:  # 새블록처리
                    movingBlock.row = maxRow
                    setBoard()
                    Board.checkRows(movingBlock)
                    movingBlock = Block(Q.popBlock())
                    Board.score += ONE_BLOCK_SCORE


        pygame.display.update()

    pygame.quit()

def initGame():
    global GamePad, BLOCK, Clock
    global Board, movingBlock, Q

    pygame.init()
    GamePad = pygame.display.set_mode(DISPLAY_SIZE)
    pygame.display.set_caption('tetris_2021hs_V2')
    BLOCK = pygame.image.load('newblock.png')

    pygame.display.set_icon(BLOCK)
    Clock = pygame.time.Clock()
    Board = Board()
    Q = Blocks()
    movingBlock = Block(Q.popBlock())
    set_interval(down, SEC)




initGame()
runGame()