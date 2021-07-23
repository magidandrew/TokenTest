from abc import ABC, abstractmethod


class AbstractAgent(ABC):
    def __init__(self, alpha: float):
        self.alpha = alpha

    @abstractmethod
    def get_block_time(self, difficulty: float):
        pass
