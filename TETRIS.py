import pygame
import random
import sys
import copy

import threading
def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0,255,0)
YELLOW = (255,255,0)

PAD_SIZE = (400, 800)
BLOCK_SIZE = 40
BOARD_ROW = 20
BOARD_COL = 10

SEC = 1

TYPES =[ # index 0~6
[[0,0],[0,1],[0,2],[0,3]], #직선
[[0,0],[0,1],[1,0],[1,1]], #정사각형
[[0,0],[0,1],[0,2],[1,0]], #3-1 왼쪽아래
[[0,0],[0,1],[1,1],[1,2]], #2-2 왼쪽위
[[0,0],[0,1],[0,2],[1,2]], #ㅗ
[[0,0],[1,0],[1,1],[1,2]], #1-3 왼쪽위
[[0,1],[0,2],[1,0],[1,1]] #2-2 오른쪽위
]

class Block:
    def __init__(self):
        self.row = 0
        self.col = int(BOARD_COL*0.5)
        self.states = TYPES[random.randint(0,6)]

    def minmaxRow(self):
        temp = [row[0]+self.row for row in self.states]
        return min(temp),max(temp)

class Board:
    def __init__(self):
        self.states =[[0 for col in range(10)] for row in range(20)]
        self.index = [False for _ in range(20)]

    def checkIndex(self):
        for idx, state in enumerate(self.index):
            if state:
                if sum(self.states[idx])==0:
                    self.index[idx]=False


    def checkIsFull(self, row):
        if self.states[row] == [1,1,1,1,1,1,1,1,1,1]:
            return True
        return False

    def checkRows(self, movingBlock):
        minRow, maxRow = movingBlock.minmaxRow()
        r = maxRow
        while r != minRow-1:
            if self.checkIsFull(r):
                self.states[r] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                self.states.insert(0, self.states.pop(r))
                minRow += 1
            else:
                r -= 1

def checkCollision(Board, movingBlock, LOWEST=None): # 행동이 취해진 후
    if LOWEST==None: LOWEST=0

    for blockRow,blockCol in movingBlock.states:
        row, col = blockRow+movingBlock.row+LOWEST, blockCol+movingBlock.col
        if not ( (-1<row and row<BOARD_ROW)and(-1<col and col<BOARD_COL) ):
            return True
        if Board.states[row][col] == 1:
            return True
    return False

def drawObject(col,row, type):
    global GamePad
    pygame.draw.rect(GamePad, type, pygame.Rect((col*BLOCK_SIZE+2,row*BLOCK_SIZE+2),(BLOCK_SIZE-2,BLOCK_SIZE-2)))

def drawBlockOnBoard(Board):
    for idx, state in enumerate(Board.index):
        if state:
            for col in range(0, BOARD_COL):
                if Board.states[idx][col] == 1:
                    drawObject(col, idx, GREEN)

def drawMovingBlock(colorType, movingBlock, LOWEST=None):
    if LOWEST==None: LOWEST=0

    for y, x in movingBlock.states:
        x, y = x+movingBlock.col, y+movingBlock.row+LOWEST
        drawObject(x,y,colorType)

def rotate(movingBlock):
    maxRow = 0
    for rc in movingBlock.states:
        if(rc[0] > maxRow):
            maxRow = rc[0]
        rc[0], rc[1] = rc[1],-rc[0]
    for rc in movingBlock.states:
        rc[1]+=maxRow

def setBoard(Board, movingBlock):
    for rc in movingBlock.states:
        Board.states[rc[0] + movingBlock.row][rc[1] + movingBlock.col] = 1
        Board.index[rc[0] + movingBlock.row] = True

def drawBoard():
    global GamePad


    for i in range(0,PAD_SIZE[0]+1,40):
        pygame.draw.line(GamePad, BLACK, (i, 0), (i, PAD_SIZE[1]), 2)
        pygame.draw.line(GamePad, BLACK, (0, i), (PAD_SIZE[0], i), 2)
        pygame.draw.line(GamePad, BLACK, (0, PAD_SIZE[0]+i), (PAD_SIZE[0], PAD_SIZE[0]+i), 2)

def makeDown():
    global movingBlock, Board, tempRow
    movingBlock.row += 1
    if checkCollision(Board, movingBlock):
        movingBlock.row -= 1
        setBoard(Board, movingBlock)
        movingBlock = Block()
        tempRow = None


def findLowest(Board, movingBlock):
    tempRow = movingBlock.row
    while not checkCollision(Board,movingBlock,tempRow):
        tempRow += 1
    return tempRow-1

def runGame():
    global GamePad, BLOCK, Clock
    global Board, movingBlock

    endFlag = False
    tempRow = None

    #GamePad.fill(WHITE)
    #drawMovingBlock(GREEN, movingBlock)
    #drawSettedBlock()
    #drawBoard()


    while not endFlag:
        GamePad.fill(WHITE)
        drawBoard()
        drawMovingBlock(GREEN, movingBlock)
        tempRow = findLowest(Board, movingBlock)
        drawMovingBlock(YELLOW, movingBlock, tempRow)
        drawBlockOnBoard(Board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # col -1
                    movingBlock.col -= 1
                    if checkCollision(Board, movingBlock):
                        movingBlock.col += 1
                if event.key == pygame.K_RIGHT:  # col +1
                    movingBlock.col += 1
                    if checkCollision(Board, movingBlock):
                        movingBlock.col -= 1
                if event.key == pygame.K_UP:  # rotate
                    temp = copy.deepcopy(movingBlock.states)
                    rotate(movingBlock)
                    if checkCollision(Board, movingBlock):
                        movingBlock.states = temp
                if event.key == pygame.K_DOWN:   #row +1
                    movingBlock.row += 1
                    if checkCollision(Board, movingBlock):
                        movingBlock.row -= 1
                if event.key == pygame.K_SPACE:
                    movingBlock.row += tempRow


        GamePad.fill(WHITE)
        drawBoard()
        drawMovingBlock(GREEN, movingBlock)
        tempRow = findLowest(Board, movingBlock)
        drawMovingBlock(YELLOW, movingBlock, tempRow)
        drawBlockOnBoard(Board)

        pygame.display.update()
        Clock.tick(60)

    pygame.quit()










def initGame():
    global GamePad, BLOCK, Clock
    global Board, movingBlock

    pygame.init()
    GamePad = pygame.display.set_mode(PAD_SIZE)
    pygame.display.set_caption('tetris_2021hs_V2')
    BLOCK = pygame.image.load('block.png')

    pygame.display.set_icon(BLOCK)
    Clock = pygame.time.Clock()
    Board = Board()
    movingBlock = Block()
    set_interval(makeDown, SEC)




initGame()
runGame()