from collections import deque

from tetris2024.core.randomizer import BagRandomizer


class TetrominoQueue:
    """테트로미노를 미리 정해진 크기만큼 랜덤하게 뽑아서 저장하는 클래스

        Args:
            randomizer(Randomizer): 테트로미노를 랜덤하게 뽑는 객체
            size(int): 미리 뽑아 저장할 테트로미노 크기
    """

    def __init__(self, randomizer=BagRandomizer(), size=1):
        self.size = size
        self.randomizer = randomizer
        self.queue = deque([], maxlen=size)

    def pop(self) -> int:
        next_piece = self.queue.popleft()
        self.queue.append(self.randomizer.get_random())
        return next_piece

    def peek(self) -> int:
        return self.queue[0]

    def reset(self):
        self.queue.clear()
        for _ in range(self.size):
            self.queue.append(self.randomizer.get_random())
