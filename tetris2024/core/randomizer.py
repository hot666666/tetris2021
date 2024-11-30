from abc import ABC, abstractmethod
import random


class Randomizer(ABC):
    @abstractmethod
    def get_random(self) -> int:
        pass

    @abstractmethod
    def reset(self):
        pass


class BagRandomizer(Randomizer):
    """테트로미노를 랜덤하게 뽑지만, 한 번씩 다 뽑기전에 뽑은 테트로미노를 다시 뽑지 않는 클래스"""

    def __init__(self, num_pieces=7):
        self.num_pieces = num_pieces
        self.bag = list(range(self.num_pieces))
        random.shuffle(self.bag)

    def get_random(self):
        if len(self.bag) <= 0:
            self.bag = list(range(self.num_pieces))
            random.shuffle(self.bag)
        return self.bag.pop()

    def reset(self):
        self.bag = list(range(self.num_pieces))
        random.shuffle(self.bag)


class RandRandomizer(Randomizer):
    """테트로미노를 랜덤하게 뽑는 클래스"""

    def __init__(self, num_pieces=7):
        self.num_pieces = num_pieces

    def get_random(self):
        return random.randint(0, self.num_pieces - 1)

    def reset(self):
        pass
