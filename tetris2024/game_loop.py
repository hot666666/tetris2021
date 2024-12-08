import time


class GameLoop:
    def __init__(self, game, input_event_queue, tk_manager, drop_interval=1.0):
        self.game = game
        self.input_event_queue = input_event_queue
        self.tk_manager = tk_manager
        self.drop_interval = drop_interval
        self.last_drop_time = time.time()

    def update(self):
        current_time = time.time()
        delta_time = current_time - self.last_drop_time
        gameover = False
        is_landed = False

        # 1. 입력 처리
        user_input = self.input_event_queue.pop()

        if user_input not in self.tk_manager.key_mapping:
            user_input = None

        if user_input:
            action = self.tk_manager.key_mapping[user_input]

            gameover, is_landed = self.game.step(action)

        # 자동 드랍 처리
        if delta_time > self.drop_interval:
            action = self.tk_manager.key_mapping["Down"]
            gameover, _ = self.game.step(action)

            # 최근 자동 드랍 시간 업데이트
            self.last_drop_time = current_time

        # 2. 렌더링 (render 함수가 Canvas를 바로 업데이트)
        self.game.renderer.render(self.game.get_game_states())

        # 3. UI(canvas) 업데이트
        if not gameover:
            if not is_landed:
                self.tk_manager.canvas.after(16, self.update)
            else:
                self.tk_manager.canvas.after(800, self.update)
                self.input_event_queue.clear()
        else:
            self.tk_manager.display_game_over()
            self.tk_manager.root.after(2000, self.tk_manager.close_window)
