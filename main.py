import argparse

from tetris2024.game_loop import GameLoop
from tetris2024.core.game import Game
from tetris2024.graphic.renderer import TKRenderer
from tetris2024.io.input_event_queue import InputEventQueue
from tetris2024.io.tk_manager import TKManager


def main(w, h, bs):
    game = Game(width=w, height=h, block_size=bs)
    renderer = TKRenderer(
        width=w, height=h, block_size=bs)
    input_event_queue = InputEventQueue()
    tk_manager = TKManager(
        width=w, height=h, block_size=bs, input_event_queue=input_event_queue
    )

    game_loop = GameLoop(
        game=game,
        renderer=renderer,
        input_event_queue=input_event_queue,
        tk_manager=tk_manager,
        drop_interval=1.0
    )

    tk_manager.start_ui_loop(game_loop.update)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type=int, default=10)
    parser.add_argument('--height', type=int, default=20)
    parser.add_argument('--block_size', type=int, default=30)
    args = parser.parse_args()

    main(args.width, args.height, args.block_size)
