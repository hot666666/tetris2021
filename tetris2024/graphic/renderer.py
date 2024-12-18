import numpy as np
from PIL import Image, ImageDraw, ImageTk, ImageFont


class Renderer:
    """게임 이미지를 만들어주는 클래스"""

    PIECE_COLORS = [
        (0, 0, 0),  # Empty
        (127, 219, 255),  # O
        (255, 210, 125),  # T
        (192, 132, 151),  # S
        (168, 230, 207),  # Z
        (255, 111, 97),  # I
        (90, 125, 154),  # L
        (255, 160, 122),  # J
        (32, 32, 32)  # shadow
    ]

    HEADER_COLOR = (0, 0, 0)

    TEXT_COLOR = (255, 255, 255)

    FONT = ImageFont.truetype(
        "./tetris2024/graphic/arial.ttf", size=20)

    def __init__(self, width=10, height=20,  block_size=30, canvas=None):
        self.canvas = canvas
        self.image_id = None
        self.photo_image = None

        self.width = width
        self.height = height
        self.block_size = block_size

        self.next_piece_size = (2*block_size) // 5

        self.header_height = 2
        self.header_right_padding = 10
        self.header_left_padding = block_size // 2

    def get_scaled_piece_pos(self, piece, x, y):
        """piece의 scale된 위치를 x, y에 맞게 반환하는 메서드"""

        top = y * self.block_size
        left = x * self.block_size
        bottom = top + len(piece)
        right = left + len(piece[0])

        return top, left, bottom, right

    def get_scaled_RGB_arr(self, arr):
        scale = self.next_piece_size if len(arr) == 5 else self.block_size

        ndarr = np.array(
            [[self.PIECE_COLORS[p] for p in row] for row in arr],
            dtype=np.uint8
        )
        scaled_ndarr = np.kron(ndarr, np.ones(
            (scale, scale, 1), dtype=np.uint8))
        return scaled_ndarr

    def render(self, game_states):
        # 보드 배열을 만들고 현재 블록을 추가
        board = self.get_board_ndarray(game_states.board)

        # 현재 블록 배열과 위치를 보드에 추가
        piece = self.get_piece_ndarray(game_states.piece)
        pos = self.get_scaled_piece_pos(piece, game_states.x, game_states.y)
        self.update_board_with(board, piece, pos)

        # 다음 블록 배열
        next_piece = self.get_next_piece_ndarray(game_states.next_piece)

        # 헤더 배열
        header = self.get_header_ndarray(next_piece)

        # 전체 게임 배열(헤더 + 보드)
        game = np.vstack((header, board))

        # RGB 배열 → PIL 이미지 변환
        game_img = Image.fromarray(game, "RGB")
        # 점수 표시
        self.draw_header_score(game_img, game_states.score)

        self.photo_image = ImageTk.PhotoImage(game_img)

        # Canvas에 업데이트
        if self.image_id is None:
            # 처음 그릴 때는 이미지 ID를 저장
            self.image_id = self.canvas.create_image(
                0, 0, anchor="nw", image=self.photo_image)
        else:
            # 이후에는 이미지를 업데이트
            self.canvas.itemconfig(self.image_id, image=self.photo_image)

    def draw_header_score(self, game_img, score):
        draw = ImageDraw.Draw(game_img)
        # font를 설정하면 크기 조절 가능
        draw.text((self.header_left_padding, self.header_left_padding),
                  f"Score: {score}", fill=self.TEXT_COLOR, font=self.FONT)

    def update_board_with(self, board, piece, pos):
        # 보드에 현재 블록 추가
        top, left, bottom, right = pos
        board[top:bottom, left:right] = np.where(
            piece > 0, piece, board[top:bottom, left:right]
        )

        # 격자 추가
        board[[i * self.block_size for i in range(self.height)], :, :] = 0
        board[:, [i * self.block_size for i in range(self.width)], :] = 0

    def get_board_ndarray(self, board):
        board = self.get_scaled_RGB_arr(board)

        return board

    def get_piece_ndarray(self, piece):
        piece = self.get_scaled_RGB_arr(piece)

        return piece

    def get_header_ndarray(self, next_piece):
        # 헤더 영역 배열 생성
        header = np.full(
            (self.block_size * 2, self.width * self.block_size, 3),
            fill_value=self.HEADER_COLOR,
            dtype=np.uint8)

        # 다음 블록 이미지 추가
        next_piece_x = (self.width-self.header_height) * self.block_size
        header[0:next_piece.shape[0],
               next_piece_x:next_piece_x+next_piece.shape[1]] = next_piece

        # 밑줄 추가
        header[-1:] = 128

        return header

    def get_next_piece_ndarray(self, next_piece):
        # 5x5로 패딩
        padded_piece = np.zeros((5, 5), dtype=int)
        piece_h, piece_w = len(next_piece), len(next_piece[0])
        if piece_w == 4:
            padded_piece[1:1+piece_h, 0:piece_w] = next_piece
        elif piece_w == 2:
            padded_piece[1:1+piece_h, 2:2+piece_w] = next_piece
        else:
            padded_piece[1:1+piece_h, 1:1+piece_w] = next_piece

        next_piece = self.get_scaled_RGB_arr(padded_piece)
        return next_piece
