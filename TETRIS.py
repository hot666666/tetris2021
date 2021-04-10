# 시간날때 -> 맨밑칸에서의움직임,최적화,추가 게임기능
import pygame
import random
from time import sleep
import copy

WHITE = (255, 255, 255)
pad_width = 400
pad_height = 800
block_size = 40

board_row = 20
board_col = 10

TYPES =[ # index 0~6
[[0,0],[0,1],[0,2],[0,3]], #직선
[[0,0],[0,1],[1,0],[1,1]], #정사각형
[[0,0],[0,1],[0,2],[1,0]], #3-1 왼쪽아래
[[0,0],[0,1],[1,1],[1,2]], #2-2 왼쪽위
[[0,0],[0,1],[0,2],[1,2]], #ㅗ
[[0,0],[1,0],[1,1],[1,2]], #1-3 왼쪽위
[[0,1],[0,2],[1,0],[1,1]] #2-2 오른쪽위
]

class board:
    def __init__(self):
        self.states =[
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.index = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]

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

class BLOCK:
    def __init__(self):
        self.tRow = 0
        self.row = 0
        self.states = TYPES[random.randint(0,6)]
        self.col = int(board_col*0.5)

    def minmaxRow(self):
        temp = [row[0]+self.row for row in self.states]
        return min(temp),max(temp)

    def rowForPrint(self):
        self.tRow += 0.05
        if self.tRow // 1 == 1:
            self.row += 1
            self.tRow -= 1


def drawObject(obj, x, y):
    global gamepad
    gamepad.blit(obj, (x, y))

def rotate(movingBlock):
    maxRow = 0
    for rc in movingBlock.states:
        if(rc[0] > maxRow):
            maxRow = rc[0]
        rc[0], rc[1] = rc[1],-rc[0]
    for rc in movingBlock.states:
        rc[1]+=maxRow

def checkCollision(Board, movingBlock):
    for rc in movingBlock.states:
        row = rc[0]+movingBlock.row
        col = rc[1]+movingBlock.col
        try:
            if Board.states[row][col] == 1 or row<0 or col<0 or row>board_row:
                return True
        except IndexError:
            return True
    return False

def checkMovabiltiy(Board, movingBlock):
    for rc in movingBlock.states:
        if rc[0] + movingBlock.row == board_row-1: return False
        if Board.states[rc[0]+movingBlock.row+1][rc[1]+movingBlock.col] == 1: return False
    return True

def checkEndFlag(Board, movingBlock):
    for rc in movingBlock.states:
        row = rc[0]+movingBlock.row
        col = rc[1]+movingBlock.col
        if Board.states[row][col]==1:
            return True
    return False

def setBoard(Board, movingBlock):
    for rc in movingBlock.states:
        Board.states[rc[0] + movingBlock.row][rc[1] + movingBlock.col] = 1
        Board.index[rc[0] + movingBlock.row] = True

def runGame():
    global gamepad, block, clock ,grid
    global Board, movingBlock

    endFlag = False


    while not endFlag:

        movingBlock.rowForPrint()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:    #col -1
                    movingBlock.col-=1
                    if checkCollision(Board, movingBlock):
                        movingBlock.col += 1
                elif event.key == pygame.K_RIGHT: #col +1
                    movingBlock.col+=1
                    if checkCollision(Board, movingBlock):
                        movingBlock.col -= 1
                elif event.key == pygame.K_UP:    #rotate
                    temp = copy.deepcopy(movingBlock.states)
                    rotate(movingBlock)
                    if checkCollision(Board, movingBlock):
                        movingBlock.states = temp
                elif event.key == pygame.K_DOWN:   #row +1
                    movingBlock.row+=1
                    if checkCollision(Board, movingBlock):
                        movingBlock.row -= 1
                elif event.key == pygame.K_SPACE:
                    while checkMovabiltiy(Board,movingBlock):
                        movingBlock.row += 1

        if not checkMovabiltiy(Board,movingBlock):
            setBoard(Board,movingBlock)
            Board.checkRows(movingBlock)
            movingBlock = BLOCK()
            Board.checkIndex()
            if checkEndFlag(Board,movingBlock):
                endFlag=True




        gamepad.fill(WHITE)
        drawObject(grid, 0,0)
        for idx, state in enumerate(Board.index):
            if state:
                for col in range(0,10):
                    if Board.states[idx][col] == 1:
                        drawObject(block, (col) * block_size+2, (idx) * block_size+2 )
        for rc in movingBlock.states:
            drawObject(block, (movingBlock.col+rc[1])*block_size+2,(movingBlock.row+rc[0]+movingBlock.tRow)*block_size+2)



        pygame.display.update()
        clock.tick(60)

    pygame.quit()




def initGame():
    global gamepad, block, clock, grid
    global Board, movingBlock

    pygame.init()
    gamepad = pygame.display.set_mode((pad_width, pad_height))
    pygame.display.set_caption('tetris_2021hs v1')
    block = pygame.image.load('newblock.png')
    grid = pygame.image.load('board.png')
    pygame.display.set_icon(block)
    clock = pygame.time.Clock()
    Board = board()
    movingBlock = BLOCK()





initGame()
runGame()