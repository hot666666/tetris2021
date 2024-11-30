from collections import deque


class InputEventQueue:
    """랜더링과 키입력의 동기화를 위한 입력 큐 클래스"""

    def __init__(self):
        self.input_queue = deque()

    def push(self, key):
        self.input_queue.append(key)

    def pop(self):
        return self.input_queue.popleft() if self.input_queue else None

    def clear(self):
        self.input_queue.clear()
