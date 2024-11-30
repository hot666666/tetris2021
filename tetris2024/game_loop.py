import time


class GameLoop:
    def __init__(self, game, renderer, input_event_queue, ui_manager, drop_interval=1.0):
        self.game = game
        self.renderer = renderer
        self.input_event_queue = input_event_queue
        self.ui_manager = ui_manager
        self.drop_interval = drop_interval
        self.last_drop_time = time.time()

        self.key_mapping = {
            "Up": self.game.actions.rotate,
            "Down": self.game.actions.move_down,
            "Left": self.game.actions.move_left,
            "Right": self.game.actions.move_right,
            "space": self.game.actions.hard_drop,
        }

    def update(self):
        current_time = time.time()
        delta_time = current_time - self.last_drop_time
        gameover = False

        # 1. 입력 처리
        user_input = self.input_event_queue.pop()

        if user_input not in self.key_mapping:
            user_input = None

        if user_input:
            action = self.key_mapping[user_input]

            gameover, block_respawned = self.game.step(action)

            # 새로 블록이 생성되었다면, 입력 버퍼를 비움
            if block_respawned:
                self.input_event_queue.clear()

        if delta_time > self.drop_interval:
            action = self.key_mapping["Down"]
            gameover, block_respawned = self.game.step(action)

            # 최근 자동 드랍 시간 업데이트
            self.last_drop_time = current_time

        # 3. 렌더링
        tk_game_img = self.renderer.render(
            self.game.get_game_states()
        )

        # 4. UI(canvas) 업데이트
        if not gameover:
            self.ui_manager.update_canvas(tk_game_img)
            self.ui_manager.canvas.after(16, self.update)
        else:
            self.ui_manager.display_game_over()
            self.ui_manager.root.after(2000, self.ui_manager.close_window)
