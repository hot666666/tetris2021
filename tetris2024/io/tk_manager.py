import tkinter as tk
from PIL import ImageTk

from tetris2024.core.game import GameActions


class TKManager:
    """tkinter를 이용한 UI 관리(+ 키 입력 바인딩) 클래스"""

    key_mapping = {
        "Up": GameActions.rotate,
        "Down": GameActions.move_down,
        "Left": GameActions.move_left,
        "Right": GameActions.move_right,
        "space": GameActions.hard_drop,
    }

    def __init__(self, width, height, block_size, input_event_queue):
        self.root = tk.Tk()
        self.root.title("Tetris2024")
        self.input_event_queue = input_event_queue
        self.canvas = tk.Canvas(
            self.root,
            width=width * block_size,
            height=(2 + height) * block_size,  # (헤더 + 게임보드)
            bg="black"
        )
        self.canvas.pack()
        self.root.bind(
            "<KeyPress>", lambda e: input_event_queue.push(e.keysym))

    def start_ui_loop(self, update_callback):
        """UI 루프를 시작하는 메서드"""
        self.root.after(0, update_callback)
        self.root.mainloop()

    def update_canvas(self, image):
        """이미지 배열을 캔버스에 그리는 메서드"""

        tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        self.canvas.image = tk_image

    def display_game_over(self):
        """게임 오버 메시지를 캔버스에 표시하는 메서드"""

        self.canvas.create_text(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2,
            text="Game Over",
            fill="red",
            font=("Helvetica", 24, "bold")
        )

    def close_window(self):
        """윈도우를 닫는 메서드"""
        self.root.destroy()
