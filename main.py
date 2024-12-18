import argparse

from tetris2024.game_loop import GameLoop
from tetris2024.core.game import Game
from tetris2024.io.input_event_queue import InputEventQueue
from tetris2024.io.tk_manager import TKManager


def main(w, h, bs):
    tk_manager = TKManager(
        width=w, height=h, block_size=bs, input_event_queue=InputEventQueue()
    )
    game = Game(width=w, height=h, canvas=tk_manager.canvas)

    game_loop = GameLoop(
        game=game,
        tk_manager=tk_manager,
    )

    game_loop.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type=int, default=10)
    parser.add_argument('--height', type=int, default=20)
    parser.add_argument('--block_size', type=int, default=30)
    args = parser.parse_args()

    main(args.width, args.height, args.block_size)
