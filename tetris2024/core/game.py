from dataclasses import dataclass

from tetris2024.core.randomizer import BagRandomizer
from tetris2024.core.tetromino_queue import TetrominoQueue
from tetris2024.graphic.renderer import Renderer


@dataclass(frozen=True)
class GameActions:
    """게임에서 사용되는 액션"""
    move_left: int = 0
    move_right: int = 1
    move_down: int = 2
    rotate: int = 3
    hard_drop: int = 4


@dataclass(frozen=True)
class GameStates:
    """랜더링을 위한 게임 상태 데이터"""
    board: list
    piece: list
    x: int
    y: int
    score: int
    next_piece: list


class Game:
    # 테트로미노 종류
    PIECES = [
        # O
        [[1, 1],
         [1, 1]],

        # T
        [[0, 2, 0],
         [2, 2, 2]],

        # S
        [[0, 3, 3],
         [3, 3, 0]],

        # Z
        [[4, 4, 0],
         [0, 4, 4]],

        # I
        [[5, 5, 5, 5]],

        # L
        [[0, 0, 6],
         [6, 6, 6]],

        # J
        [[7, 0, 0],
         [7, 7, 7]]
    ]
    # 드랍 조각을 표시할 값
    DROP_INDICATOR = 8

    def __init__(self, width=10, height=20, canvas=None, randomizer=BagRandomizer()):
        self.width = width
        self.height = height
        self.queue = TetrominoQueue(randomizer=randomizer)
        self.renderer = Renderer(
            width=width, height=height, block_size=30, canvas=canvas)

        self.reset()

        """
        게임 상태관련 변수
        - board : 현재 보드 상태
        - piece : 현재 블록(2차원 배열)
        - x, y : 현재 블록의 좌표
        - score : 현재 점수
        - idx: 현재 종류 블록 인덱스
        - cleared_lines : 지워진 줄 수
        - gameover : 게임 종료 여부
        """

    def reset(self):
        """게임 상태 초기화 후, 초기 상태 특징을 반환하는 메서드"""

        self.board = [[0]*self.width for _ in range(self.height)]

        self.score = 0
        self.cleared_lines = 0

        self.queue.reset()

        self.idx = self.queue.pop()
        self.piece = [r[:] for r in self.PIECES[self.idx]]
        self.x = self.width // 2 - len(self.piece[0]) // 2
        self.y = 0

        self.gameover = False

    def step(self, action: GameActions):
        """action에 따라 게임을 진행하고, (게임 종료, 안착 여부)를 반환하는 메서드"""

        is_landed = False

        # piece에 이동방향을 미리 적용하여 check_collision 메서드를 통해 충돌을 확인한 후 이동방향 적용
        if action == GameActions.move_left:
            if not self.check_collision(self.piece, self.x - 1, self.y):
                self.x -= 1
        elif action == GameActions.move_right:
            if not self.check_collision(self.piece, self.x + 1, self.y):
                self.x += 1
        elif action == GameActions.move_down:
            if not self.check_collision(self.piece, self.x, self.y + 1):
                self.y += 1
        elif action == GameActions.rotate:
            rotated_piece = self.get_rotated_piece(self.piece)
            if not self.check_collision(rotated_piece, self.x, self.y):
                self.piece = rotated_piece
        elif action == GameActions.hard_drop:
            self.animate_hard_drop()  # 애니메이션 루프 호출
            is_landed = True
            return self.gameover, is_landed

        # 현재 piece가 보드 상단을 벗어나는 경우 = 게임오버
        if self.truncate_overflow_piece(self.piece, self.x, self.y):
            self.gameover = True
            is_landed = True

            self.board = self.get_board_with_piece(self.piece, self.x, self.y)
            lines_cleared, self.board = self.clear_full_rows(self.board)
            self.cleared_lines += lines_cleared
            self.score += self.get_reward(lines_cleared)

            return self.gameover, is_landed

        # 게임오버가 아니지만 움직일 수 없는 경우, 다음 테트로미노를 뽑아서 현재 테트로미노로 설정
        if self.check_collision(self.piece, self.x, self.y + 1):
            self.board = self.get_board_with_piece(self.piece, self.x, self.y)
            lines_cleared, self.board = self.clear_full_rows(self.board)
            self.cleared_lines += lines_cleared
            self.score += self.get_reward(lines_cleared)

            self.spawn_next_piece()
            is_landed = True

        return self.gameover, is_landed

    def get_hard_dropped_y(self):
        """현재 piece를 hard drop 했을 때의 y 좌표를 반환하는 메서드"""

        dropped_y = self.y
        while not self.check_collision(self.piece, self.x, dropped_y + 1):
            dropped_y += 1
        return dropped_y

    def animate_hard_drop(self):
        def drop_step():
            if not self.check_collision(self.piece, self.x, self.y + 1):
                self.y += 1
                self.renderer.render(self.get_game_states())
                self.renderer.canvas.after(16, drop_step)
            else:
                # 블록이 바닥에 도달했을 때
                self.board = self.get_board_with_piece(
                    self.piece, self.x, self.y)
                lines_cleared, self.board = self.clear_full_rows(self.board)
                self.cleared_lines += lines_cleared
                self.score += self.get_reward(lines_cleared)
                self.spawn_next_piece()

        drop_step()

    def get_game_states(self) -> GameStates:
        """랜더링에 필요한 게임 상태를 반환하는 메서드, board, piece는 복사본을 반환"""

        dropped_piece = [[self.DROP_INDICATOR if v else 0 for v in r]
                         for r in self.piece]
        dropped_y = self.get_hard_dropped_y()
        board = self.get_board_with_piece(
            piece=dropped_piece, x=self.x, y=dropped_y)
        piece = [r[:] for r in self.piece]
        next_piece = self.PIECES[self.queue.peek()]
        return GameStates(board, piece, self.x, self.y, self.score, next_piece)

    def get_board_with_piece(self, piece=None, x=None, y=None):
        """현재 보드의 복사본을 만들어서, piece를 추가한 보드를 반환하는 메서드"""

        # 명시하지 않은 경우 현재 상태를 그대로 사용
        piece = piece or self.piece
        x = x or self.x
        y = y or self.y

        board = [r[:] for r in self.board]
        for _y in range(len(piece)):
            for _x in range(len(piece[_y])):
                if piece[_y][_x] == 0:
                    continue
                if board[y+_y][x+_x] == 0:
                    board[y+_y][x+_x] = piece[_y][_x]

        return board

    def check_collision(self, piece, x, y):
        """현재 보드 상태에서, piece가 pos에 추가될 때 충돌이 발생하는지 여부를 반환하는 메서드"""

        for _y in range(len(piece)):
            for _x in range(len(piece[_y])):
                if y+_y > self.height-1 or y+_y < 0 or x+_x > self.width-1 or x+_x < 0:
                    return True
                if piece[_y][_x] == 0:
                    continue
                if self.board[y+_y][x+_x] > 0:
                    return True
        return False

    def truncate_overflow_piece(self, piece, x, y) -> bool:
        """piece가 보드 상단 밖으로 나가는 경우, piece를 잘라내고 True를 반환하는 메서드"""

        is_truncated = False
        last_collision_row = -1
        for _y in range(len(piece)):
            for _x in range(len(piece[_y])):
                if piece[_y][_x] == 0:
                    continue
                if self.board[y+_y][x+_x] > 0:
                    if _y > last_collision_row:
                        last_collision_row = _y
                        break

        if y - (len(piece) - last_collision_row) < 0 and last_collision_row > -1:
            while last_collision_row >= 0 and len(piece) > 1:
                is_truncated = True
                last_collision_row = -1
                del piece[0]
                for y in range(len(piece)):
                    for x in range(len(piece[y])):
                        if piece[_y][_x] == 0:
                            continue
                        if self.board[y + _y][x + _x] > 0 and _y > last_collision_row:
                            last_collision_row = _y

        return is_truncated

    def spawn_next_piece(self):
        """다음 테트로미노를 뽑아서 현재 테트로미노로 설정하는 메서드"""

        self.idx = self.queue.pop()
        self.piece = [r[:] for r in self.PIECES[self.idx]]
        self.x = self.width // 2 - len(self.piece[0]) // 2
        self.y = 0

        if self.check_collision(self.piece, self.x, self.y):
            self.gameover = True

    def get_rotated_piece(self, piece):
        """현재 테트로미노를 시계방향으로 90도 회전한 결과를 반환하는 메서드"""

        rotated_array = []
        new_len_col, new_len_row = len(piece), len(piece[0])
        old_len_row = new_len_col

        for i in range(new_len_row):
            new_row = [0] * new_len_col
            for j in range(new_len_col):
                new_row[j] = piece[(old_len_row-1)-j][i]
            rotated_array.append(new_row)
        return rotated_array

    def clear_full_rows(self, board):
        """보드에서 꽉 찬 줄을 in-place 연산으로 지우고, 지워진 줄 수와 보드를 반환하는 메서드"""

        to_delete = []
        for i, row in enumerate(board[::-1]):
            if 0 not in row:
                to_delete.append(len(board) - 1 - i)
        if len(to_delete) > 0:
            board = self._remove_rows(board, to_delete)
        return len(to_delete), board

    def _remove_rows(self, board, indices):
        # 보드에서 indices에 해당하는 행을 in-place 삭제하고, 위에 빈 행을 추가하는 메서드
        for i in indices[::-1]:
            del board[i]
            board = [[0]*self.width] + board
        return board

    def get_reward(self, lines_cleared):
        """지워진 줄 수에 대한 보상을 반환하는 메서드"""

        return 1 + (lines_cleared ** 2) * self.width
