from abc import ABC, abstractmethod
from queue import Queue


class AbstractAgent(ABC):
    def __init__(self, alpha: float):
        self.alpha = alpha
        self.mining_queue = Queue()

    @abstractmethod
    def get_block_time(self, difficulty: float):
        pass

    def __str__(self):
        return_val = [f"alpha: {self.alpha}", f"type: {self.__class__.__name__}"]
        return ", ".join(return_val)
